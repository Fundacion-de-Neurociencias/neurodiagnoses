# -*- coding: utf-8 -*-
"""
Neurodiagnoses: Probabilistic Diagnostic Engine (Axis 2)

This module implements a simple Bayesian inference engine to calculate
disease probabilities based on biomarker evidence. It uses pre-defined
priors and likelihoods from reference data tables.
"""

import json
import argparse
import itertools
import pandas as pd

# --- Constants ---
PRIORS_CSV = "data/reference/axis2_priors.csv"
LIKES_CSV = "data/reference/axis2_likelihoods.csv"

# --- Core Functions ---
def load_knowledge_base():
    """Loads the prior probabilities and likelihood data from CSV files."""
    try:
        priors = pd.read_csv(PRIORS_CSV).set_index('label')
        likelihoods = pd.read_csv(LIKES_CSV)
        return priors, likelihoods
    except FileNotFoundError as e:
        print(f"ERROR: Knowledge base file not found. {e}")
        return None, None

def odds(p):
    """Converts probability to odds."""
    return p / (1 - p + 1e-9)

def prob(o):
    """Converts odds to probability."""
    return o / (1 + o)

def get_likelihood_ratio(is_positive, sens, spec):
    """Calculates the Likelihood Ratio (LR+ or LR-)."""
    if is_positive:
        # LR+ = sensitivity / (1 - specificity)
        return sens / (1 - spec + 1e-9)
    else:
        # LR- = (1 - sensitivity) / specificity
        return (1 - sens) / (spec + 1e-9)

def calculate_posteriors(patient_evidence, priors, likelihoods):
    """
    Calculates the posterior probabilities for each diagnosis.
    
    Args:
        patient_evidence (dict): A dictionary of patient biomarker values.
        priors (pd.DataFrame): DataFrame of prior probabilities.
        likelihoods (pd.DataFrame): DataFrame of biomarker likelihoods.

    Returns:
        dict: A dictionary of posterior probabilities for each label.
    """
    # Initialize posterior odds with prior odds
    posterior_odds = priors['prior'].apply(odds).to_dict()

    # NOTE: This is a simplified example using a single piece of evidence.
    # A full implementation would loop through all available patient evidence.
    
    # Example: Check for pTau/Abeta42 evidence
    evidence_key = 'pTau181_Abeta42_positive'
    patient_value = patient_evidence.get('PTAU_over_ABETA')
    
    if patient_value is not None:
        # For now, we assume the cutoff is known and the value is pre-classified as positive/negative.
        # This part will need to be expanded to handle cutoffs dynamically.
        is_evidence_positive = patient_evidence.get('PTAU_over_ABETA_POSITIVE', False)
        
        # Update odds for each diagnosis based on this evidence
        for label in posterior_odds:
            # Find the sens/spec for this evidence and this label
            like_row = likelihoods[
                (likelihoods['evidence'] == evidence_key) & (likelihoods['label'] == label)
            ]
            
            if not like_row.empty:
                sens = like_row.iloc[0]['sens']
                spec = like_row.iloc[0]['spec']
                lr = get_likelihood_ratio(is_evidence_positive, sens, spec)
                posterior_odds[label] *= lr

    # Convert final odds back to probabilities
    posteriors = {label: prob(o) for label, o in posterior_odds.items()}
    return posteriors

def main():
    """Main function to run the probabilistic diagnosis from CLI."""
    parser = argparse.ArgumentParser(description="Run probabilistic diagnosis for a patient.")
    parser.add_argument("--patient_evidence", required=True, help="JSON string or file path with patient evidence.")
    args = parser.parse_args()

    # Load patient evidence from JSON string or file
    try:
        if os.path.exists(args.patient_evidence):
            with open(args.patient_evidence, 'r') as f:
                patient_data = json.load(f)
        else:
            patient_data = json.loads(args.patient_evidence)
    except Exception as e:
        print(f"Error loading patient evidence: {e}")
        return

    # Load knowledge base
    priors, likelihoods = load_knowledge_base()
    if priors is None:
        return

    # Calculate posterior probabilities
    posteriors = calculate_posteriors(patient_data, priors, likelihoods)
    
    # Rank and print results
    ranked_posteriors = sorted(posteriors.items(), key=lambda item: item[1], reverse=True)

    print("\n--- Probabilistic Diagnosis (Axis 2 - Bayesian Engine) ---")
    for label, probability in ranked_posteriors:
        print(f"- {label}: {probability:.4f}")

if __name__ == "__main__":
    main()
