import pandas as pd
from pathlib import Path
import numpy as np

class BayesianEngine:
    def __init__(self, axis2_kb_path: Path, axis1_kb_path: Path, num_simulations: int = 10000):
        # Carga de múltiples bases de conocimiento
        self.axis2_df = self._load_knowledge_base(axis2_kb_path, "Axis 2")
        self.axis1_df = self._load_knowledge_base(axis1_kb_path, "Axis 1")
        self.num_simulations = num_simulations
        print(f"INFO: Engine initialized for {self.num_simulations} simulations.")

    def _load_knowledge_base(self, kb_path: Path, axis_name: str) -> pd.DataFrame:
        if not kb_path.exists():
            raise FileNotFoundError(f"{axis_name} KB file not found at: {kb_path}")
        print(f"INFO: Loading {axis_name} KB from {kb_path}...")
        df = pd.read_csv(kb_path)
        for col in ['value', 'ci_lower', 'ci_upper']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        print(f"SUCCESS: {axis_name} Knowledge Base loaded.")
        return df

    def _get_axis2_distribution(self, biomarker: str, disease: str):
        row = self.axis2_df[
            (self.axis2_df['biomarker_name'] == biomarker) &
            (self.axis2_df['primary_disease'].str.contains(disease, case=False))
        ].iloc[0]
        mean = row['value']
        std = ((row['ci_upper'] - row['ci_lower']) / 4.0) if pd.notna(row['ci_upper']) else 0.05
        return mean, std

    def _get_axis1_odds_ratio(self, variant_id: str, disease: str) -> float:
        """Finds the Odds Ratio for a given genetic variant."""
        row = self.axis1_df[
            (self.axis1_df['biomarker_name'] == variant_id) &
            (self.axis1_df['primary_disease'].str.contains(disease, case=False))
        ]
        if row.empty:
            raise ValueError(f"Odds Ratio not found for variant '{variant_id}'")
        return row.iloc[0]['value']

    def update_belief_with_likelihood(self, prior, sensitivity, specificity):
        false_positive_rate = 1 - specificity
        p_evidence = (sensitivity * prior) + (false_positive_rate * (1 - prior))
        return (sensitivity * prior) / p_evidence if p_evidence > 0 else 0.0
    
    def update_belief_with_odds_ratio(self, prior, odds_ratio):
        """Updates a prior probability using an Odds Ratio."""
        prior_odds = prior / (1 - prior)
        posterior_odds = prior_odds * odds_ratio
        posterior_prob = posterior_odds / (1 + posterior_odds)
        return posterior_prob

    def run_full_inference(self, axis1_evidence: list, axis2_evidence: list, disease: str, initial_prior: float):
        print("\n--- [Full Tridimensional Inference Scenario (Axis 1 & 2)] ---")
        print(f"Initial Belief (Prior) for {disease}: {initial_prior:.2%}")
        print(f"Patient Evidence (Axis 1 - Genetics): {axis1_evidence}")
        print(f"Patient Evidence (Axis 2 - Molecular): {axis2_evidence}")
        print("----------------------------------------------------------")

        current_prob = initial_prior
        
        # --- Procesar Evidencia del Eje 1 ---
        print("\n--- Processing Axis 1 Evidence (Genetics) ---")
        for variant in axis1_evidence:
            try:
                odds_ratio = self._get_axis1_odds_ratio(variant, disease)
                print(f"  - Found Evidence: Odds Ratio for {variant} is {odds_ratio:.2f}")
                new_prob = self.update_belief_with_odds_ratio(current_prob, odds_ratio)
                print(f"  - Belief Updated: {current_prob:.2%} -> {new_prob:.2%}")
                current_prob = new_prob
            except ValueError as e:
                print(f"  - WARNING: Could not process genetic evidence for '{variant}'. Reason: {e}")
        
        # --- Procesar Evidencia del Eje 2 (con Incertidumbre) ---
        print("\n--- Processing Axis 2 Evidence (Molecular) ---")
        final_posteriors = []
        for i in range(self.num_simulations):
            sim_prob = current_prob # Empezamos cada simulación desde el prior actualizado por la genética
            
            for biomarker in axis2_evidence:
                try:
                    sens_mean, sens_std = self._get_axis2_distribution(biomarker, disease)
                    spec_mean, spec_std = (sens_mean * 1.1, 0.05) # Placeholder para especificidad
                    
                    sampled_sens = np.clip(np.random.normal(sens_mean, sens_std), 0.01, 0.99)
                    sampled_spec = np.clip(np.random.normal(spec_mean, spec_std), 0.01, 0.99)
                    
                    sim_prob = self.update_belief_with_likelihood(sim_prob, sampled_sens, sampled_spec)
                except (IndexError, ValueError):
                    continue
            final_posteriors.append(sim_prob)

        mean_posterior = np.mean(final_posteriors)
        credibility_interval = np.percentile(final_posteriors, [2.5, 97.5])

        print("\n--- [Final Inference Result] ---")
        print(f"Final Posterior Probability (Mean): {mean_posterior:.2%}")
        print(f"95% Credibility Interval: [{credibility_interval[0]:.2%} - {credibility_interval[1]:.2%}]")
        print("--------------------------------")
        return mean_posterior, credibility_interval

if __name__ == "__main__":
    engine = BayesianEngine(
        axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
        axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv")
    )
    
    # Paciente con evidencia genética y molecular
    patient_axis1 = ["rs6695033"] # OR de 2.71
    patient_axis2 = ["p-tau181"]  # AUC de 0.74

    engine.run_full_inference(
        axis1_evidence=patient_axis1,
        axis2_evidence=patient_axis2,
        disease="Alzheimer's Disease",
        initial_prior=0.10 # Un prior más bajo, de un paciente más joven por ejemplo
    )