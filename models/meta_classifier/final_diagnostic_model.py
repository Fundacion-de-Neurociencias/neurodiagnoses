# models/meta_classifier/final_diagnostic_model.py
import numpy as np

# --- CONFIGURATION ---
# Define weights for each axis. Genetic findings (Axis 1) are given high importance.
AXIS_WEIGHTS = {
    'axis1': 0.5, # Etiology
    'axis2': 0.3, # Molecular
    'axis3': 0.2  # Phenotype. Its influence is more complex, here simplified.
}

# Mapping from Axis 2/3 numerical classes to disease/phenotype strings
# This should be centralized in the ontology in a future refactor.
AXIS2_CLASS_MAP = {0: 'CO', 1: 'AD', 2: 'PD', 3: 'FTD', 4: 'DLB'}
AXIS3_CLASS_MAP = {0: 'Tau-positive', 1: 'TDP-43'}

class MetaClassifier:
    """
    The central brain of Neurodiagnoses. It takes the outputs from the three
    individual axes and produces a final, unified diagnostic report.
    """
    def __init__(self, axis1_result, axis2_result, axis3_result):
        self.axis1 = axis1_result
        self.axis2 = axis2_result
        self.axis3 = axis3_result

    def get_final_probabilities(self) -> dict:
        """
        Combines probabilities from the three axes using a weighted average.
        This implements the logic for probabilistic diagnosis of co-pathologies.
        """
        # For this PoC, we primarily weigh Axis 1 (genetics) and Axis 2 (molecular).
        # A more advanced version would use a trained model to find optimal weights.
        
        # Initialize a dictionary to hold the combined weighted scores
        combined_scores = {disease: 0.0 for disease in AXIS2_CLASS_MAP.values()}

        # Add weighted scores from Axis 1 (simulated for now)
        # We simulate a simple mapping from the text result to a probability vector.
        if "C9orf72" in self.axis1:
            combined_scores['FTD'] += 1.0 * AXIS_WEIGHTS['axis1']
        
        # Add weighted scores from Axis 2 (Molecular)
        if self.axis2 and isinstance(self.axis2, dict):
            for disease, prob in self.axis2.items():
                if disease in combined_scores:
                    combined_scores[disease] += prob * AXIS_WEIGHTS['axis2']
        
        # Normalize the final probabilities to sum to 1.0 for a ranked list
        total_score = sum(combined_scores.values())
        if total_score > 0:
            final_probabilities = {d: s / total_score for d, s in combined_scores.items()}
        else: # Fallback if no scores were generated
            final_probabilities = {d: 1.0 / len(combined_scores) for d in combined_scores}
            
        return final_probabilities

    def get_tridimensional_summary(self) -> str:
        """
        Generates a human-readable tridimensional diagnostic summary.
        """
        # Find the top finding for each axis
        etiology_summary = self.axis1 if self.axis1 else "Etiology Undetermined"
        
        molecular_summary = "Molecular Profile: " + (max(self.axis2, key=self.axis2.get) if self.axis2 and isinstance(self.axis2, dict) else "Undetermined")

        phenotype_summary = "Phenotype: " + (self.axis3 if self.axis3 else "Undetermined")

        summary = f"{etiology_summary} | {molecular_summary} | {phenotype_summary}"
        return summary
