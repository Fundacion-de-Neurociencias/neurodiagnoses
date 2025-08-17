import pandas as pd
from pathlib import Path
import numpy as np
import pymc as pm
import pytensor.tensor as pt
from scipy.stats import norm

class BayesianEngine:
    def __init__(self, axis1_kb_path: Path, axis2_kb_path: Path, axis3_kb_path: Path, num_simulations: int = 2000):
        # Cargamos las KBs, num_simulations ahora se usa para el muestreo de PyMC
        self.axis1_df = self._load_knowledge_base(axis1_kb_path, "Axis 1")
        self.axis2_df = self._load_knowledge_base(axis2_kb_path, "Axis 2")
        self.axis3_df = self._load_knowledge_base(axis3_kb_path, "Axis 3")
        self.num_draws = num_simulations
        print(f"INFO: PyMC Bayesian Engine initialized. MCMC draws set to {self.num_draws}.")

    def _load_knowledge_base(self, kb_path: Path, axis_name: str) -> pd.DataFrame:
        if not kb_path.exists(): raise FileNotFoundError(f"{axis_name} KB file not found at: {kb_path}")
        df = pd.read_csv(kb_path)
        # Limpiar nombres de columnas por si acaso
        df.columns = df.columns.str.strip()
        for col in ['value', 'ci_lower', 'ci_upper']:
            if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    def _get_params(self, df, biomarker_name, stat_types):
        """Extrae parámetros de la KB. Devuelve una tupla (mean, std)."""
        try:
            row = df[(df['biomarker_name'] == biomarker_name) & (df['statistic_type'].isin(stat_types))].iloc[0]
            mean = row['value']
            std = ((row['ci_upper'] - row['ci_lower']) / 3.92) if pd.notna(row['ci_upper']) else 0.15 * abs(mean)
            return mean, std if std > 0 else 0.01
        except (IndexError, ValueError):
            return None, None
            
    def _get_imaging_params(self, biomarker, cohort):
        """Extrae parámetros de media y std para neuroimagen."""
        try:
            mean_val = self.axis3_df[(self.axis3_df['biomarker_name'] == biomarker) & (self.axis3_df['statistic_type'] == 'distribution_mean') & (self.axis3_df['cohort_description'].str.contains(cohort))]['value'].iloc[0]
            std_val = self.axis3_df[(self.axis3_df['biomarker_name'] == biomarker) & (self.axis3_df['statistic_type'] == 'distribution_std') & (self.axis3_df['cohort_description'].str.contains(cohort))]['value'].iloc[0]
            return mean_val, std_val if std_val > 0 else 0.01
        except (IndexError, ValueError):
            return None, None

    def run_full_tridimensional_inference(self, patient_data: dict, disease: str, initial_prior: float):
        print("\n--- [PyMC Tridimensional Inference] ---")
        
        with pm.Model() as model:
            # 1. Definir el Prior
            prior_odds = pm.ConstantData("prior_odds", initial_prior / (1 - initial_prior))
            current_odds = prior_odds
            
            # 2. Construir el modelo evidencia por evidencia
            
            # --- Axis 1: Genetics ---
            for variant in patient_data.get('axis1', []):
                mean, std = self._get_params(self.axis1_df, variant, ['odds_ratio'])
                if mean is not None:
                    or_dist = pm.LogNormal(f'OR_{variant}', mu=np.log(mean), sigma=std/mean if mean and std else 0.1)
                    current_odds *= or_dist

            # --- Axis 2 & 3a: Biomarkers & Phenotype (Sensitivity/Specificity based) ---
            for ev_type, df, stat_types in [('axis2', self.axis2_df, ['sensitivity', 'auc']), ('axis3_phenotype', self.axis3_df, ['sensitivity', 'specificity', 'accuracy'])]:
                for biomarker in patient_data.get(ev_type, []):
                    sens_mean, sens_std = self._get_params(df, biomarker, stat_types)
                    if sens_mean is not None:
                        # Asumimos que la especificidad es similar a la sensibilidad para el PoC
                        spec_mean, spec_std = sens_mean * 1.1, sens_std * 1.2
                        
                        sens = pm.Beta(f'sens_{biomarker}', alpha=sens_mean*10, beta=(1-sens_mean)*10)
                        spec = pm.Beta(f'spec_{biomarker}', alpha=spec_mean*10, beta=(1-spec_mean)*10)
                        
                        likelihood_ratio = sens / (1 - spec)
                        current_odds *= likelihood_ratio

            # --- Axis 3b: Neuroimaging (Continuous) ---
            for biomarker, value in patient_data.get('axis3_imaging', {}).items():
                mean_d, std_d = self._get_imaging_params(biomarker, disease)
                mean_c, std_c = self._get_imaging_params(biomarker, 'Control')
                if mean_d is not None and mean_c is not None:
                    likelihood_disease = pm.logp(pm.Normal.dist(mu=mean_d, sigma=std_d), value)
                    likelihood_control = pm.logp(pm.Normal.dist(mu=mean_c, sigma=std_c), value)
                    
                    # Log Likelihood Ratio
                    log_lr = likelihood_disease - likelihood_control
                    current_odds *= pt.exp(log_lr)

            # 3. Calcular la Probabilidad Posterior Final
            posterior_prob = pm.Deterministic("posterior_prob", current_odds / (1 + current_odds))
            
            # 4. Ejecutar la Inferencia
            print("INFO: MCMC sampling started...")
            trace = pm.sample(self.num_draws, tune=1000, cores=1, progressbar=False)
            print("INFO: MCMC sampling complete.")

        # 5. Extraer y devolver los resultados
        posterior_samples = trace.posterior['posterior_prob'].values.flatten()
        mean_posterior = np.mean(posterior_samples)
        credibility_interval = np.percentile(posterior_samples, [2.5, 97.5])
        
        # (La pista de auditoría se simplifica por ahora, ya que el modelo de PyMC es la explicación en sí mismo)
        evidence_trail = ["Inference performed with PyMC model v1.0"]

        return mean_posterior, credibility_interval, evidence_trail
