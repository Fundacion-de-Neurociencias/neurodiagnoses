# -*- coding: utf-8 -*-
"""
Neurodiagnoses: Probabilistic Diagnostic Engine (Axis 2) - Class-based Refactor

This module implements a simple Bayesian inference engine to calculate
disease probabilities based on biomarker evidence. It uses pre-defined
priors and likelihoods from reference data tables.
"""

import argparse
import json
import os
import sys

import pandas as pd

# Add project root to path for cross-module imports
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))


class BayesianAxis2Pipeline:
    """
    A self-contained pipeline for running the Axis 2 Bayesian diagnosis.
    It loads a knowledge base and calculates posterior probabilities for a patient.
    """

    def __init__(
        self,
        priors_path="data/reference/axis2_priors.csv",
        likes_path="data/reference/axis2_likelihoods.csv",
    ):
        """Initializes the pipeline by loading the knowledge base."""
        self.priors_path = priors_path
        self.likes_path = likes_path
        self.priors, self.likelihoods = self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Loads the prior probabilities and likelihood data from CSV files."""
        try:
            priors = pd.read_csv(self.priors_path).set_index("label")
            likelihoods = pd.read_csv(self.likes_path)
            print("Bayesian knowledge base loaded successfully.")
            return priors, likelihoods
        except FileNotFoundError as e:
            print(f"ERROR: Knowledge base file not found. {e}")
            return None, None

    def _odds(self, p):
        """Converts probability to odds."""
        return p / (1 - p + 1e-9)

    def _prob(self, o):
        """Converts odds to probability."""
        return o / (1 + o)

    def _get_likelihood_ratio(self, is_positive, sens, spec):
        """Calculates the Likelihood Ratio (LR+ or LR-)."""
        if is_positive:
            # LR+ = sensitivity / (1 - specificity)
            return sens / (1 - spec + 1e-9)
        else:
            # LR- = (1 - sensitivity) / specificity
            return (1 - sens) / (spec + 1e-9)

    def predict(self, patient_evidence: dict):
        """
        Calculates the posterior probabilities for each diagnosis for a given patient.

        Args:
            patient_evidence (dict): A dictionary of patient biomarker values.
                                     Example: {'PTAU_over_ABETA': 0.07, 'PTAU_over_ABETA_POSITIVE': True}

        Returns:
            dict: A dictionary of posterior probabilities for each label, or None if error.
        """
        if self.priors is None or self.likelihoods is None:
            print("ERROR: Cannot predict without a valid knowledge base.")
            return None

        posterior_odds = self.priors["prior"].apply(self._odds).to_dict()

        # Iterate through all evidence in the likelihoods table
        for _, evidence_row in self.likelihoods.iterrows():
            evidence_name = evidence_row["evidence"]  # e.g., 'pTau181_Abeta42_positive'
            label = evidence_row["label"]
            sens = evidence_row["sens"]
            spec = evidence_row["spec"]

            # Check if the patient has this evidence (pre-classified as positive/negative)
            if evidence_name in patient_evidence:
                is_evidence_positive = patient_evidence[evidence_name]
                lr = self._get_likelihood_ratio(is_evidence_positive, sens, spec)

                # Update the odds for the specific label this likelihood applies to
                if label in posterior_odds:
                    posterior_odds[label] *= lr

        # Convert final odds back to probabilities
        posteriors = {label: self._prob(o) for label, o in posterior_odds.items()}
        return posteriors


def main():
    """Main function to run the probabilistic diagnosis from CLI for testing."""
    parser = argparse.ArgumentParser(
        description="Run probabilistic diagnosis for a patient."
    )
    parser.add_argument(
        "--patient_evidence",
        required=True,
        help="JSON string or file path with patient evidence.",
    )
    args = parser.parse_args()

    try:
        if os.path.exists(args.patient_evidence):
            with open(args.patient_evidence, "r") as f:
                patient_data = json.load(f)
        else:
            patient_data = json.loads(args.patient_evidence)
    except Exception as e:
        print(f"Error loading patient evidence: {e}")
        return

    # Instantiate and run the pipeline
    pipeline = BayesianAxis2Pipeline()
    posteriors = pipeline.predict(patient_data)

    if posteriors:
        ranked_posteriors = sorted(
            posteriors.items(), key=lambda item: item[1], reverse=True
        )
        print("\n--- Probabilistic Diagnosis (Axis 2 - Bayesian Engine) ---")
        for label, probability in ranked_posteriors:
            print(f"- {label}: {probability:.4f}")


if __name__ == "__main__":
    main()
