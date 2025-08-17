import pandas as pd
from pathlib import Path
import numpy as np
from scipy.stats import norm

class BayesianEngine:
    def __init__(self, axis1_kb_path: Path, axis2_kb_path: Path, axis3_kb_path: Path, num_simulations: int = 10000):
        self.axis1_df = self._load_knowledge_base(axis1_kb_path, "Axis 1")
        self.axis2_df = self._load_knowledge_base(axis2_kb_path, "Axis 2")
        self.axis3_df = self._load_knowledge_base(axis3_kb_path, "Axis 3")
        self.num_simulations = num_simulations

    def _load_knowledge_base(self, kb_path: Path, axis_name: str) -> pd.DataFrame:
        if not kb_path.exists(): raise FileNotFoundError(f"{axis_name} KB file not found at: {kb_path}")
        df = pd.read_csv(kb_path)
        for col in ['value', 'ci_lower', 'ci_upper']:
            if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    def _get_dist_params(self, df, biomarker, disease, stat_types):
        row = df[(df['biomarker_name'] == biomarker) & (df['statistic_type'].isin(stat_types)) & (df['primary_disease'].str.contains(disease, case=False, na=False))].iloc[0]
        mean = row['value']
        std = ((row['ci_upper'] - row['ci_lower']) / 3.92) if pd.notna(row['ci_upper']) else 0.15 * abs(mean)
        return mean, std if std > 0 else 0.01, row.get('source_snippet', '')

    def _get_axis3_imaging_params(self, biomarker, cohort):
        mean_row = self.axis3_df[(self.axis3_df['biomarker_name'] == biomarker) & (self.axis3_df['statistic_type'] == 'distribution_mean') & (self.axis3_df['cohort_description'].str.contains(cohort))].iloc[0]
        std_row = self.axis3_df[(self.axis3_df['biomarker_name'] == biomarker) & (self.axis3_df['statistic_type'] == 'distribution_std') & (self.axis3_df['cohort_description'].str.contains(cohort))].iloc[0]
        return mean_row['value'], std_row['value']

    def update_belief_with_likelihood_ratio(self, prior, lr):
        prior_odds = prior / (1 - prior); posterior_odds = prior_odds * lr
        return posterior_odds / (1 + posterior_odds)

    def run_full_tridimensional_inference(self, patient_data: dict, disease: str, initial_prior: float):
        final_posteriors, evidence_trail = [], []
        
        for i in range(self.num_simulations):
            current_prob = initial_prior
            
            # --- Axis 1: Genetics ---
            for biomarker in patient_data.get('axis1', []):
                try:
                    mean, std, snippet = self._get_dist_params(self.axis1_df, biomarker, disease, ['odds_ratio'])
                    if i == 0: evidence_trail.append(f"[Axis 1: {biomarker}] {snippet}")
                    lr = np.clip(np.random.normal(mean, std), 0.1, 20.0) # Odds Ratio is a Likelihood Ratio
                    current_prob = self.update_belief_with_likelihood_ratio(current_prob, lr)
                except (IndexError, ValueError): continue

            # --- Axis 2: Molecular ---
            for biomarker in patient_data.get('axis2', []):
                try:
                    sens_mean, sens_std, snippet = self._get_dist_params(self.axis2_df, biomarker, disease, ['sensitivity', 'auc', 'c-index'])
                    if i == 0: evidence_trail.append(f"[Axis 2: {biomarker}] {snippet}")
                    spec_mean, spec_std = (sens_mean * 1.1, 0.05)
                    sampled_sens = np.clip(np.random.normal(sens_mean, sens_std), 0.01, 0.99)
                    sampled_spec = np.clip(np.random.normal(spec_mean, spec_std), 0.01, 0.99)
                    lr = sampled_sens / (1 - sampled_spec)
                    current_prob = self.update_belief_with_likelihood_ratio(current_prob, lr)
                except (IndexError, ValueError): continue

            # --- Axis 3: Clinical Phenotype (Criteria & Signs) ---
            for biomarker in patient_data.get('axis3_phenotype', []):
                try:
                    sens_mean, sens_std, snippet = self._get_dist_params(self.axis3_df, biomarker, disease, ['sensitivity', 'specificity', 'accuracy'])
                    if i == 0: evidence_trail.append(f"[Axis 3 Pheno: {biomarker}] {snippet}")
                    spec_mean, spec_std = (sens_mean * 1.1, 0.05)
                    sampled_sens = np.clip(np.random.normal(sens_mean, sens_std), 0.01, 0.99)
                    sampled_spec = np.clip(np.random.normal(spec_mean, spec_std), 0.01, 0.99)
                    lr = sampled_sens / (1 - sampled_spec)
                    current_prob = self.update_belief_with_likelihood_ratio(current_prob, lr)
                except (IndexError, ValueError): continue

            # --- Axis 3: Neuroimaging ---
            for biomarker, value in patient_data.get('axis3_imaging', {}).items():
                try:
                    mean_d, std_d = self._get_axis3_imaging_params(biomarker, disease)
                    mean_c, std_c = self._get_axis3_imaging_params(biomarker, 'Control')
                    if i == 0: evidence_trail.append(f"[Axis 3 Image: {biomarker}] ADNI Dataset")
                    likelihood_disease = norm.pdf(value, mean_d, std_d)
                    likelihood_control = norm.pdf(value, mean_c, std_c)
                    if likelihood_control > 0:
                        lr = likelihood_disease / likelihood_control
                        current_prob = self.update_belief_with_likelihood_ratio(current_prob, lr)
                except (IndexError, ValueError): continue
            
            final_posteriors.append(current_prob)
            
        mean_posterior = np.mean(final_posteriors)
        credibility_interval = np.percentile(final_posteriors, [2.5, 97.5])
        return mean_posterior, credibility_interval, list(set(evidence_trail))