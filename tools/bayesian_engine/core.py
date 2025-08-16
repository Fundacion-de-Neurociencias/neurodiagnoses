import pandas as pd
from pathlib import Path

class BayesianEngine:
    """
    A simple Bayesian inference engine that updates beliefs based on evidence
    from a structured knowledge base.
    """
    def __init__(self, kb_path: Path):
        self.kb_df = self._load_knowledge_base(kb_path)

    def _load_knowledge_base(self, kb_path: Path) -> pd.DataFrame:
        """Loads a knowledge base CSV file into a pandas DataFrame."""
        if not kb_path.exists():
            raise FileNotFoundError(f"Knowledge base file not found at: {kb_path}")
        print(f"INFO: Loading Knowledge Base from {kb_path}...")
        df = pd.read_csv(kb_path)
        print("SUCCESS: Knowledge Base loaded.")
        return df

    def _get_likelihoods(self, biomarker: str, disease: str) -> (float, float):
        """
        Finds the likelihoods (sensitivity and 1 - specificity) for a biomarker.
        """
        # For this PoC, we are primarily using AUC as a proxy for sensitivity.
        # A more advanced KB would distinguish these explicitly.
        # We will also use a placeholder for specificity if not found.
        
        stat_types = ['sensitivity', 'auc', 'c-index']
        
        # Find Sensitivity P(Positive|Disease)
        sens_row = self.kb_df[
            (self.kb_df['biomarker_name'] == biomarker) &
            (self.kb_df['statistic_type'].isin(stat_types)) &
            (self.kb_df['primary_disease'] == disease)
        ]
        if sens_row.empty:
            raise ValueError(f"Sensitivity/AUC not found for biomarker '{biomarker}' and disease '{disease}'")
        sensitivity = sens_row.iloc[0]['value']

        # Find Specificity P(Negative|No Disease) and derive False Positive Rate
        spec_row = self.kb_df[
            (self.kb_df['biomarker_name'] == biomarker) &
            (self.kb_df['statistic_type'] == 'specificity') &
            (self.kb_df['primary_disease'] == disease)
        ]
        
        # If specificity is missing, we'll estimate a plausible value for this PoC.
        # Let's assume specificity is similar to sensitivity if not specified.
        specificity = spec_row.iloc[0]['value'] if not spec_row.empty else (sensitivity * 1.1) # Placeholder
        specificity = min(specificity, 0.99) # Cap specificity at 99%
        
        false_positive_rate = 1 - specificity
        return sensitivity, false_positive_rate

    def update_belief(self, prior_prob: float, sensitivity: float, false_positive_rate: float) -> float:
        """
        Calculates the posterior probability using Bayes' theorem for a positive test result.
        """
        # P(Evidence) = P(E|Disease)*P(Disease) + P(E|No Disease)*P(No Disease)
        p_evidence = (sensitivity * prior_prob) + (false_positive_rate * (1 - prior_prob))
        if p_evidence == 0:
            return 0.0
        
        # Bayes' Theorem: P(Disease|Evidence) = [P(E|Disease) * P(Disease)] / P(Evidence)
        posterior_prob = (sensitivity * prior_prob) / p_evidence
        return posterior_prob

    def run_multi_evidence_inference(self, patient_evidence: list, disease: str, initial_prior: float):
        """
        Runs inference for a patient with multiple pieces of evidence.
        """
        print("n--- [Multi-Evidence Inference Scenario] ---")
        print(f"Initial Belief (Prior) for {disease}: {initial_prior:.2f}")
        print(f"Patient has {len(patient_evidence)} pieces of positive evidence: {patient_evidence}")
        print("------------------------------------------")

        current_prob = initial_prior
        
        for i, biomarker in enumerate(patient_evidence):
            print(f"nProcessing Evidence {i+1}: '{biomarker}'")
            try:
                sensitivity, fpr = self._get_likelihoods(biomarker, disease)
                print(f"  - Found Likelihoods -> Sensitivity: {sensitivity:.2f}, FPR: {fpr:.2f}")
                
                new_prob = self.update_belief(current_prob, sensitivity, fpr)
                print(f"  - Belief Updated: {current_prob:.2f} -> {new_prob:.2f}")
                current_prob = new_prob
                
            except ValueError as e:
                print(f"  - WARNING: Could not process evidence for '{biomarker}'. Reason: {e}")
                continue

        print("n--- [Final Inference Result] ---")
        print(f"Final Posterior Probability for {disease}: {current_prob:.2f}")
        print(f"Conclusion: After considering all evidence, the belief in the diagnosis of {disease} has shifted from {int(initial_prior*100)}% to {int(current_prob*100)}%.")
        print("--------------------------------")
        return current_prob


if __name__ == "__main__":
    # Initialize the engine with our knowledge base
    engine = BayesianEngine(kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"))

    # Define a patient with multiple positive biomarkers
    patient_data = [
        "p-tau181",
        "Gene expression-based blood biomarker panels",
        "NfL"
    ]

    # Run the inference
    engine.run_multi_evidence_inference(
        patient_evidence=patient_data,
        disease="Alzheimer's Disease",
        initial_prior=0.20 # Start with a 20% initial suspicion
    )