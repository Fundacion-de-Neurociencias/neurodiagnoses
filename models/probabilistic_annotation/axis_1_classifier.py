# models/probabilistic_annotation/axis_1_classifier.py
import numpy as np
import json
import os

# This knowledge base remains the same
PATHOGENIC_MAP = {
    "PSEN1": "AD", "PSEN2": "AD", "APP": "AD",
    "HTT": "Huntington's",
    "GRN": "FTD", "MAPT": "FTD", "C9orf72": "FTD/ALS"
}
SPECIFIC_RISK_MAP = {
    "APOE_e4": {"disease": "AD", "multiplier": 1.5}
}
DISEASE_CLASSES = ['AD', 'PD', 'FTD', 'DLB', 'CO', "Huntington's", 'FTD/ALS']

def predict_etiology_from_analysis(analysis_file: str) -> dict:
    """
    Predicts disease probabilities from a structured JSON of significant genetic variants.
    This is the upgraded Axis 1 classifier.
    """
    try:
        with open(analysis_file, 'r') as f:
            genetics = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Genetic analysis file not found at {analysis_file}")
        return {d: 1.0/len(DISEASE_CLASSES) for d in DISEASE_CLASSES}

    probabilities = {disease: 1.0 / len(DISEASE_CLASSES) for disease in DISEASE_CLASSES}

    # Process pathogenic variants first (highest impact)
    for variant in genetics.get("pathogenic_variants", []):
        variant_gene = variant.split('_')[0]
        if variant_gene in PATHOGENIC_MAP:
            disease = PATHOGENIC_MAP[variant_gene]
            for d in probabilities: probabilities[d] = 0.01
            probabilities[disease] = 1.0 - (0.01 * (len(DISEASE_CLASSES) - 1))
            return probabilities # Return immediately if pathogenic is found

    # Process specific risk polymorphisms
    for variant in genetics.get("disease_specific_risk", []):
        if variant in SPECIFIC_RISK_MAP:
            risk_info = SPECIFIC_RISK_MAP[variant]
            probabilities[risk_info["disease"]] *= risk_info["multiplier"]

    # In a real model, imputed_significant_variants would also adjust probabilities
    
    # Normalize probabilities to sum to 1.0
    total_prob = sum(probabilities.values())
    if total_prob > 0:
        for disease in probabilities:
            probabilities[disease] /= total_prob
    
    return probabilities