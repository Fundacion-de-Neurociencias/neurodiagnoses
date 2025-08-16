import pandas as pd
from pathlib import Path
import numpy as np
from scipy.stats import norm
class BayesianEngine:
    def __init__(self, axis1_kb_path: Path, axis2_kb_path: Path, axis3_kb_path: Path, num_simulations: int = 10000):
        self.axis1_df = self._load_knowledge_base(axis1_kb_path, "Axis 1"); self.axis2_df = self._load_knowledge_base(axis2_kb_path, "Axis 2"); self.axis3_df = self._load_knowledge_base(axis3_kb_path, "Axis 3"); self.num_simulations = num_simulations
    def _load_knowledge_base(self, kb_path: Path, axis_name: str) -> pd.DataFrame:
        if not kb_path.exists(): raise FileNotFoundError(f"{axis_name} KB not found: {kb_path}")
        df = pd.read_csv(kb_path)
        for col in ['value', 'ci_lower', 'ci_upper']:
            if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    def _get_dist_params(self, df, biomarker, disease, stat_types):
        row = df[(df['biomarker_name'] == biomarker) & (df['statistic_type'].isin(stat_types)) & (df['primary_disease'].str.contains(disease, case=False, na=False))]
        if row.empty:
            raise ValueError(f"No data found for biomarker '{biomarker}' and disease '{disease}' with stat_types {stat_types}")
        row = row.iloc[0]
        
        mean = row['value']
        std = 0.0 # Default standard deviation
        
        # Try to calculate std from CI if available
        if pd.notna(row.get('ci_upper')) and pd.notna(row.get('ci_lower')):
            std = (row['ci_upper'] - row['ci_lower']) / 4.0
        elif row.get('statistic_type') == 'distribution_std': # If std is directly provided
            std = row['value']
        else: # Fallback if no CI or direct std, use a heuristic
            std = 0.1 * abs(mean) if mean != 0 else 0.1

        return mean, std, row.get('source_snippet', '')
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
            for ev_type, df, stat_types in [('axis1', self.axis1_df, ['odds_ratio']), ('axis2', self.axis2_df, ['sensitivity', 'auc']), ('axis3_phenotype', self.axis3_df, ['sensitivity', 'specificity', 'accuracy'])]:
                for biomarker in patient_data.get(ev_type, []):
                    try:
                        mean, std, snippet = self._get_dist_params(df, biomarker, disease, stat_types)
                        if i == 0: evidence_trail.append(f"[{ev_type.upper()}: {biomarker}] {snippet}")
                        if ev_type == 'axis1':
                            lr = np.clip(np.random.normal(mean, std), 0.1, 20.0)
                        else:
                            sens = np.clip(np.random.normal(mean, std), 0.01, 0.99); spec = np.clip(np.random.normal(mean*1.1, 0.05), 0.01, 0.99); lr = sens / (1 - spec)
                        current_prob = self.update_belief_with_likelihood_ratio(current_prob, lr)
                    except (IndexError, ValueError): continue
            for biomarker, value in patient_data.get('axis3_imaging', {}).items():
                try:
                    mean_d, std_d = self._get_axis3_imaging_params(biomarker, disease); mean_c, std_c = self._get_axis3_imaging_params(biomarker, 'Control')
                    if i == 0: evidence_trail.append(f"[Axis 3 Image: {biomarker}] ADNI Dataset")
                    lr = norm.pdf(value, mean_d, std_d) / norm.pdf(value, mean_c, std_c) if norm.pdf(value, mean_c, std_c) > 0 else 1
                    current_prob = self.update_belief_with_likelihood_ratio(current_prob, lr)
                except (IndexError, ValueError): continue
            final_posteriors.append(current_prob)
        mean_posterior = np.mean(final_posteriors); credibility_interval = np.percentile(final_posteriors, [2.5, 97.5])
        return mean_posterior, credibility_interval, evidence_trail
