#!/bin/bash
set -e
set -x

# --- PASO 1: Instalar SciPy para cálculos de distribuciones de probabilidad ---
pip install -q scipy

# --- PASO 2: Reemplazar el motor bayesiano con la versión TRIDIMENSIONAL ---
echo "INFO: Upgrading Bayesian Engine to be fully tridimensional (Axes 1, 2, and 3)..."
cat <<'EOF' > tools/bayesian_engine/core.py
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
        std = ((row['ci_upper'] - row['ci_lower']) / 4.0) if pd.notna(row['ci_upper']) else 0.1 * abs(mean)
        return mean, std, row.get('source_snippet', '')

    def _get_axis3_dist_params(self, biomarker, cohort):
        mean_row = self.axis3_df[(self.axis3_df['biomarker_name'] == biomarker) & (self.axis3_df['statistic_type'] == 'distribution_mean') & (self.axis3_df['cohort_description'].str.contains(cohort))].iloc[0]
        std_row = self.axis3_df[(self.axis3_df['biomarker_name'] == biomarker) & (self.axis3_df['statistic_type'] == 'distribution_std') & (self.axis3_df['cohort_description'].str.contains(cohort))].iloc[0]
        return mean_row['value'], std_row['value']

    def update_belief_with_odds_ratio(self, prior, odds_ratio):
        prior_odds = prior / (1 - prior)
        posterior_odds = prior_odds * odds_ratio
        return posterior_odds / (1 + posterior_odds)

    def update_belief_with_likelihood_ratio(self, prior, likelihood_ratio):
        prior_odds = prior / (1 - prior)
        posterior_odds = prior_odds * likelihood_ratio
        return posterior_odds / (1 + posterior_odds)

    def run_full_tridimensional_inference(self, patient_data: dict, disease: str, initial_prior: float):
        print(f"\nn--- [Full Tridimensional Inference for {disease}] ---")
        final_posteriors = []
        evidence_trail = []
        
        for i in range(self.num_simulations):
            current_prob = initial_prior
            
            # --- Axis 1: Genetics (Odds Ratio) ---
            for variant in patient_data.get('axis1', []):
                try:
                    mean, std, snippet = self._get_dist_params(self.axis1_df, variant, disease, ['odds_ratio'])
                    if i == 0: evidence_trail.append(f"[Axis 1: {variant}] {snippet}")
                    sampled_or = np.clip(np.random.normal(mean, std), 0.1, 20.0)
                    current_prob = self.update_belief_with_odds_ratio(current_prob, sampled_or)
                except (ValueError, IndexError): continue

            # --- Axis 2: Molecular (Sensitivity/Specificity) ---
            for biomarker in patient_data.get('axis2', []):
                try:
                    sens_mean, sens_std, snippet = self._get_dist_params(self.axis2_df, biomarker, disease, ['sensitivity', 'auc', 'c-index'])
                    if i == 0: evidence_trail.append(f"[Axis 2: {biomarker}] {snippet}")
                    spec_mean, spec_std = (sens_mean * 1.1, 0.05)
                    
                    sampled_sens = np.clip(np.random.normal(sens_mean, sens_std), 0.01, 0.99)
                    sampled_spec = np.clip(np.random.normal(spec_mean, spec_std), 0.01, 0.99)
                    
                    # Para un biomarcador positivo, el Likelihood Ratio es Sensibilidad / (1 - Especificidad)
                    lr = sampled_sens / (1 - sampled_spec)
                    current_prob = self.update_belief_with_likelihood_ratio(current_prob, lr)
                except (IndexError, ValueError): continue

            # --- Axis 3: Neuroimaging (Continuous Variable) ---
            for biomarker, value in patient_data.get('axis3', {}).items():
                try:
                    mean_disease, std_disease = self._get_axis3_dist_params(biomarker, disease)
                    mean_control, std_control = self._get_axis3_dist_params(biomarker, 'Control')
                    if i == 0: evidence_trail.append(f"[Axis 3: {biomarker}] ADNI Cortical Thickness Dataset")

                    # Calculamos el Likelihood Ratio usando la PDF de la distribución normal
                    # P(Evidence | Disease) / P(Evidence | No Disease)
                    likelihood_disease = norm.pdf(value, mean_disease, std_disease)
                    likelihood_control = norm.pdf(value, mean_control, std_control)
                    
                    if likelihood_control == 0: continue # Evitar división por cero
                    lr = likelihood_disease / likelihood_control
                    current_prob = self.update_belief_with_likelihood_ratio(current_prob, lr)
                except (IndexError, ValueError): continue

            final_posteriors.append(current_prob)
            
        mean_posterior = np.mean(final_posteriors)
        credibility_interval = np.percentile(final_posteriors, [2.5, 97.5])

        print(f"Final Posterior Probability (Mean): {mean_posterior:.2%}")
        print(f"95% Credibility Interval: [{credibility_interval[0]:.2%} - {credibility_interval[1]:.2%}]")
        return mean_posterior, credibility_interval, evidence_trail

if __name__ == "__main__":
    engine = BayesianEngine(
        axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
        axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
        axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv")
    )
    
    # Paciente completo con evidencia de los 3 ejes
    patient = {
        'axis1': ["rs4474465"],                            # Genética: OR de 1.44
        'axis2': ["p-tau181"],                             # Molecular: AUC de 0.74
        'axis3': {'HippocampusVolume_mm3': 3100}          # Neuroimagen: Volumen bajo (el grupo AD tenía media 3175)
    }

    engine.run_full_tridimensional_inference(
        patient_data=patient,
        disease="Alzheimer's Disease",
        initial_prior=0.10
    )
EOF

# --- PASO 3: Ejecutar el motor TRIDIMENSIONAL ---
echo "INFO: Executing the final, Tridimensional Bayesian Engine..."
python tools/bayesian_engine/core.py
