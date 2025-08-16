import pandas as pd
from pathlib import Path
import numpy as np

class BayesianEngine:
    def __init__(self, axis1_kb_path: Path, axis2_kb_path: Path, num_simulations: int = 10000):
        self.axis1_df = self._load_knowledge_base(axis1_kb_path, "Axis 1")
        self.axis2_df = self._load_knowledge_base(axis2_kb_path, "Axis 2")
        self.num_simulations = num_simulations

    def _load_knowledge_base(self, kb_path: Path, axis_name: str) -> pd.DataFrame:
        if not kb_path.exists(): raise FileNotFoundError(f"{axis_name} KB file not found at: {kb_path}")
        df = pd.read_csv(kb_path)
        for col in ['value', 'ci_lower', 'ci_upper']:
            if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    def _get_distribution_params(self, df: pd.DataFrame, biomarker: str, disease: str, stat_types: list):
        """Helper to get distribution parameters (mean, std) for any evidence."""
        row = df[
            (df['biomarker_name'] == biomarker) &
            (df['statistic_type'].isin(stat_types)) &
            (df['primary_disease'].str.contains(disease, case=False, na=False))
        ].iloc[0]
        mean = row['value']
        std = ((row['ci_upper'] - row['ci_lower']) / 4.0) if pd.notna(row['ci_upper']) else 0.1 * abs(mean) # Estimate std as 10% of mean if CI is missing
        return mean, std, row['source_snippet']

    def update_belief_with_likelihood(self, prior, sensitivity, specificity):
        # ... (código sin cambios)
        false_positive_rate = 1 - specificity
        p_evidence = (sensitivity * prior) + (false_positive_rate * (1 - prior))
        return (sensitivity * prior) / p_evidence if p_evidence > 0 else 0.0

    def update_belief_with_odds_ratio(self, prior, odds_ratio):
        # ... (código sin cambios)
        prior_odds = prior / (1 - prior)
        posterior_odds = prior_odds * odds_ratio
        return posterior_odds / (1 + posterior_odds)

    def run_full_inference(self, axis1_evidence: list, axis2_evidence: list, disease: str, initial_prior: float):
        print("\n--- [Full Tridimensional Inference with Full Uncertainty] ---")
        final_posteriors = []
        evidence_trail = []
        
        # --- [MEJORA]: El bucle de Monte Carlo ahora engloba TODOS los ejes ---
        for i in range(self.num_simulations):
            current_prob = initial_prior
            
            # --- Procesa Eje 1 con Incertidumbre ---
            for variant in axis1_evidence:
                try:
                    or_mean, or_std, snippet = self._get_distribution_params(self.axis1_df, variant, disease, ['odds_ratio'])
                    if i == 0: evidence_trail.append(f"[Axis 1] {snippet}") # Add to trail only once
                    
                    sampled_or = np.random.normal(or_mean, or_std)
                    sampled_or = np.clip(sampled_or, 0.1, 20.0) # Clamp to reasonable values
                    current_prob = self.update_belief_with_odds_ratio(current_prob, sampled_or)
                except (ValueError, IndexError):
                    continue

            # --- Procesa Eje 2 con Incertidumbre ---
            for biomarker in axis2_evidence:
                try:
                    sens_mean, sens_std, snippet = self._get_distribution_params(self.axis2_df, biomarker, disease, ['sensitivity', 'auc', 'c-index'])
                    if i == 0: evidence_trail.append(f"[Axis 2] {snippet}")
                    
                    # Placeholder para especificidad
                    spec_mean, spec_std = (sens_mean * 1.1, 0.05)
                    
                    sampled_sens = np.clip(np.random.normal(sens_mean, sens_std), 0.01, 0.99)
                    sampled_spec = np.clip(np.random.normal(spec_mean, spec_std), 0.01, 0.99)
                    current_prob = self.update_belief_with_likelihood(current_prob, sampled_sens, sampled_spec)
                except (IndexError, ValueError):
                    continue

            final_posteriors.append(current_prob)
            
        mean_posterior = np.mean(final_posteriors)
        credibility_interval = np.percentile(final_posteriors, [2.5, 97.5])

        print(f"Final Posterior Probability (Mean): {mean_posterior:.2%}")
        print(f"95% Credibility Interval: [{credibility_interval[0]:.2%} - {credibility_interval[1]:.2%}]")
        return mean_posterior, credibility_interval, evidence_trail

if __name__ == "__main__":
    # Esta sección queda para pruebas directas, la UI usará el orquestador
    pass
