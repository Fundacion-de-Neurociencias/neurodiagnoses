import pandas as pd
from pathlib import Path
import numpy as np
from scipy.stats import norm

class BayesianEngine:
    def __init__(self, axis1_kb_path: Path, axis2_kb_path: Path, axis3_kb_path: Path, num_simulations: int = 2000):
        self.axis1_df = self._load_knowledge_base(axis1_kb_path, "Axis 1")
        self.axis2_df = self._load_knowledge_base(axis2_kb_path, "Axis 2")
        self.axis3_df = self._load_knowledge_base(axis3_kb_path, "Axis 3")
        self.num_simulations = num_simulations

    def _load_knowledge_base(self, kb_path: Path, axis_name: str) -> pd.DataFrame:
        if not kb_path.exists(): raise FileNotFoundError(f"{axis_name} KB not found: {kb_path}")
        df = pd.read_csv(kb_path, keep_default_na=False)
        df.columns = df.columns.str.strip()
        for col in ['value', 'ci_lower', 'ci_upper']:
            if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    def _get_dist_params(self, df, biomarker, disease_hypothesis, stat_types):
        # --- [LÓGICA DE ESPECIFICIDAD v3.0] ---
        rows = df[(df['biomarker_name'] == biomarker) & (df['statistic_type'].isin(stat_types))]
        if rows.empty: return None, None, None, None

        # Intenta encontrar una coincidencia directa primero
        specific_match = rows[rows['primary_disease'].str.contains(disease_hypothesis, case=False, na=False)]
        
        if not specific_match.empty:
            # ¡Coincidencia perfecta! La evidencia aplica directamente a esta enfermedad.
            row = specific_match.iloc[0]
            mean = row['value']
            std = ((row['ci_upper'] - row['ci_lower']) / 3.92) if pd.notna(row.get('ci_upper')) and row.get('ci_upper', 0) > row.get('ci_lower', 0) else 0.15 * abs(mean)
            return mean, std if std > 0 else 0.01, row.get('source_snippet', ''), row.get('statistic_type')
        else:
            # No hay coincidencia directa. Esta evidencia NO es específica para esta enfermedad.
            # Su valor para esta hipótesis es "neutral".
            # Para OR/LR, el valor neutral es 1.0. Para AUC/Sensibilidad, es 0.5.
            row = rows.iloc[0] # Cogemos la primera que haya para tener el snippet
            stat_type = row.get('statistic_type')
            
            if stat_type == 'odds_ratio':
                # Un OR de 1 no cambia la probabilidad.
                return 1.0, 0.01, row.get('source_snippet', ''), stat_type
            else: # sensitivity, auc, etc.
                # Un AUC de 0.5 es azar. No aporta información.
                return 0.5, 0.01, row.get('source_snippet', ''), stat_type

    def _get_axis3_imaging_params(self, biomarker, cohort):
        try:
            mean_val = self.axis3_df[(self.axis3_df['biomarker_name'] == biomarker) & (self.axis3_df['statistic_type'] == 'distribution_mean') & (self.axis3_df['cohort_description'].str.contains(cohort))]['value'].iloc[0]
            std_val = self.axis3_df[(self.axis3_df['biomarker_name'] == biomarker) & (self.axis3_df['statistic_type'] == 'distribution_std') & (self.axis3_df['cohort_description'].str.contains(cohort))]['value'].iloc[0]
            return mean_val, std_val if std_val > 0 else 0.01
        except (IndexError, ValueError): return None, None

    def update_belief_with_likelihood_ratio(self, prior, lr):
        if lr is None or lr <= 0: return prior
        prior_odds = prior / (1 - prior); posterior_odds = prior_odds * lr
        return posterior_odds / (1 + posterior_odds)

    def run_differential_diagnosis(self, patient_data: dict, diseases_to_evaluate: list, initial_prior: float):
        # (El resto del código es idéntico, ya que el cambio de lógica está encapsulado en _get_dist_params)
        all_results = []
        for disease in diseases_to_evaluate:
            final_posteriors, evidence_trail = [], []
            for i in range(self.num_simulations):
                current_prob = initial_prior
                for ev_type, df, stat_types in [('axis1', self.axis1_df, ['odds_ratio']), ('axis2', self.axis2_df, ['sensitivity', 'auc']), ('axis3_phenotype', self.axis3_df, ['sensitivity', 'specificity', 'accuracy'])]:
                    for biomarker in patient_data.get(ev_type, []):
                        mean, std, snippet, stat_type = self._get_dist_params(df, biomarker, disease, stat_types)
                        if mean is None: continue
                        if i == 0:
                            evidence_trail.append(f"[{ev_type.upper()}] {biomarker} ({stat_type}={mean:.2f}): {snippet}")
                        val = np.random.normal(mean, std)
                        lr = val if ev_type == 'axis1' else (val / (1 - np.clip(np.random.normal(val * 0.85, 0.05), 0.01, 0.99)))
                        current_prob = self.update_belief_with_likelihood_ratio(current_prob, lr)
                for biomarker, value in patient_data.get('axis3_imaging', {}).items():
                    mean_d, std_d = self._get_axis3_imaging_params(biomarker, disease); mean_c, std_c = self._get_axis3_imaging_params(biomarker, 'Control')
                    if mean_d is not None and mean_c is not None:
                        if i == 0: evidence_trail.append(f"[IMAGING] {biomarker}={value}mm³: ADNI Dataset")
                        lr = norm.pdf(value, mean_d, std_d) / norm.pdf(value, mean_c, std_c) if norm.pdf(value, mean_c, std_c) > 0 else 1
                        current_prob = self.update_belief_with_likelihood_ratio(current_prob, lr)
                final_posteriors.append(current_prob)
            all_results.append({"disease": disease, "posterior_probability": np.mean(final_posteriors), "credibility_interval": np.percentile(final_posteriors, [2.5, 97.5]), "evidence_trail": list(set(evidence_trail))})
        
        total_prob = sum(res['posterior_probability'] for res in all_results)
        if total_prob > 0:
            for res in all_results: res['posterior_probability'] /= total_prob
        
        return sorted(all_results, key=lambda x: x['posterior_probability'], reverse=True)
