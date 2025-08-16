import pandas as pd
from pathlib import Path
import numpy as np

class BayesianEngine:
    """
    A Bayesian inference engine that updates beliefs and quantifies uncertainty
    using Monte Carlo simulation.
    """
    def __init__(self, kb_path: Path, num_simulations: int = 10000):
        self.kb_df = self._load_knowledge_base(kb_path)
        self.num_simulations = num_simulations
        print(f"INFO: Engine initialized for {self.num_simulations} Monte Carlo simulations.")

    def _load_knowledge_base(self, kb_path: Path) -> pd.DataFrame:
        """Loads and prepares the knowledge base DataFrame."""
        if not kb_path.exists():
            raise FileNotFoundError(f"Knowledge base file not found at: {kb_path}")
        print(f"INFO: Loading Knowledge Base from {kb_path}...")
        df = pd.read_csv(kb_path)
        # Convert relevant columns to numeric, coercing errors to NaN
        for col in ['value', 'ci_lower', 'ci_upper']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        print("SUCCESS: Knowledge Base loaded.")
        return df

    def _get_evidence_distribution(self, biomarker: str, disease: str) -> (tuple, tuple):
        """
        Finds the parameters for the probability distributions of sensitivity and specificity.
        Returns ((sens_mean, sens_std), (spec_mean, spec_std))
        """
        # Find Sensitivity (or AUC/c-index as proxy)
        sens_row = self.kb_df[
            (self.kb_df['biomarker_name'] == biomarker) &
            (self.kb_df['statistic_type'].isin(['sensitivity', 'auc', 'c-index'])) &
            (self.kb_df['primary_disease'] == disease)
        ].iloc[0]
        
        sens_mean = sens_row['value']
        # Estimate std from 95% CI: std ≈ (upper - lower) / 3.92 (approx. 4)
        sens_std = ((sens_row['ci_upper'] - sens_row['ci_lower']) / 4.0) if pd.notna(sens_row['ci_upper']) else 0.05

        # Find Specificity
        spec_row = self.kb_df[
            (self.kb_df['biomarker_name'] == biomarker) &
            (self.kb_df['statistic_type'] == 'specificity') &
            (self.kb_df['primary_disease'] == disease)
        ]
        
        if not spec_row.empty:
            spec_mean = spec_row.iloc[0]['value']
            spec_std = ((spec_row.iloc[0]['ci_upper'] - spec_row.iloc[0]['ci_lower']) / 4.0) if pd.notna(spec_row.iloc[0]['ci_upper']) else 0.05
        else:
            # Estimate a plausible specificity if missing
            spec_mean = min(sens_mean * 1.1, 0.99)
            spec_std = 0.05
            
        return (sens_mean, sens_std), (spec_mean, spec_std)

    def _update_belief(self, prior: float, sensitivity: float, specificity: float) -> float:
        """Applies Bayes' theorem for a positive test result."""
        false_positive_rate = 1 - specificity
        p_evidence = (sensitivity * prior) + (false_positive_rate * (1 - prior))
        return (sensitivity * prior) / p_evidence if p_evidence > 0 else 0.0

    def run_inference_with_uncertainty(self, patient_evidence: list, disease: str, initial_prior: float):
        """
        Runs the full Monte Carlo simulation for a patient.
        """
        print("n--- [Inference with Uncertainty Quantification] ---")
        print(f"Initial Belief (Prior) for {disease}: {initial_prior:.2f}")
        print(f"Patient has positive evidence for: {patient_evidence}")
        print("-------------------------------------------------")
        
        final_posteriors = []

        for i in range(self.num_simulations):
            current_prob = initial_prior
            
            for biomarker in patient_evidence:
                try:
                    (sens_mean, sens_std), (spec_mean, spec_std) = self._get_evidence_distribution(biomarker, disease)
                    
                    # Sample from the distributions
                    sampled_sens = np.random.normal(sens_mean, sens_std)
                    sampled_spec = np.random.normal(spec_mean, spec_std)
                    
                    # Clamp values to a valid probability range [0.01, 0.99]
                    sampled_sens = np.clip(sampled_sens, 0.01, 0.99)
                    sampled_spec = np.clip(sampled_spec, 0.01, 0.99)
                    
                    current_prob = self._update_belief(current_prob, sampled_sens, sampled_spec)
                    
                except (IndexError, ValueError):
                    # If a biomarker is not found, we skip it for this simulation run
                    continue
            
            final_posteriors.append(current_prob)

        # Analyze the distribution of final probabilities
        mean_posterior = np.mean(final_posteriors)
        credibility_interval = np.percentile(final_posteriors, [2.5, 97.5])

        print("n--- [Final Inference Result] ---")
        print(f"Posterior Probability (Mean): {mean_posterior:.2%}")
        print(f"95% Credibility Interval: [{credibility_interval[0]:.2%} - {credibility_interval[1]:.2%}]")
        print("--------------------------------")
        return mean_posterior, credibility_interval

if __name__ == "__main__":
    engine = BayesianEngine(
        kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
        num_simulations=10000
    )

    patient_data = [
        "p-tau181",
        # We only use one piece of evidence for this PoC because only one in our KB has a full CI
        # Adding more would use the estimated std, which is fine, but this is a cleaner demo.
    ]

    engine.run_inference_with_uncertainty(
        patient_evidence=patient_data,
        disease="Alzheimer's Disease",
        initial_prior=0.20
    )
