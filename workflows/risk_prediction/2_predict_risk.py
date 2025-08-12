# workflows/risk_prediction/2_predict_risk.py
import pandas as pd
import joblib
import os
import math

# --- CONFIGURATION ---
MODEL_PATH = 'models/risk_prediction/phs_model.joblib'

def predict_risk(subject_genetic_data: dict):
    """
    Predicts the age-associated disease risk for an asymptomatic individual
    using a pre-trained Polygenic Hazard Score (PHS) model.

    Args:
        subject_genetic_data (dict): A dictionary containing the subject's
                                     genotypes for the variants in the model.

    Returns:
        A dictionary containing the calculated risk score and an interpretation.
    """
    print(f"--- Starting PHS Risk Prediction ---")
    
    try:
        model = joblib.load(MODEL_PATH)
        print(f"--> Loaded PHS model from '{MODEL_PATH}'")
    except FileNotFoundError:
        print(f"ERROR: PHS model not found at '{MODEL_PATH}'.")
        print("Please run '1_train_phs_model.py' first.")
        return None

    # Calculate the Polygenic Hazard Score (PHS)
    # This is calculated as the sum of (variant_genotype * hazard_ratio)
    hazard_score = 0
    for variant, hazard_ratio in model['hazard_ratios'].items():
        if variant in subject_genetic_data:
            # The formula is score = sum(beta_i * genotype_i)
            # log(hazard_ratio) gives us the coefficient (beta)
            hazard_score += math.log(hazard_ratio) * subject_genetic_data[variant]
    
    # An exponentiated score gives the overall hazard ratio relative to the baseline
    overall_hazard_ratio = math.exp(hazard_score)

    # Provide a clinical interpretation
    interpretation = "No significant increased risk detected."
    if overall_hazard_ratio > 1.5:
        interpretation = f"Significantly increased risk detected (Hazard Ratio: {overall_hazard_ratio:.2f})."
    elif overall_hazard_ratio > 1.1:
        interpretation = f"Slightly increased risk detected (Hazard Ratio: {overall_hazard_ratio:.2f})."

    result = {
        "polygenic_hazard_score": hazard_score,
        "relative_hazard_ratio": overall_hazard_ratio,
        "interpretation": interpretation
    }
    
    print("--> Risk prediction complete.")
    return result

if __name__ == '__main__':
    # --- Simulate genetic data for a new, asymptomatic subject ---
    # This subject has one APOE_e4 allele and one other risk variant.
    new_subject = {
        'APOE_e4': 1,
        'variant_rs123': 0,
        'variant_rs456': 0,
        'variant_rs789': 1
    }
    
    print(f"--- Running prediction for a sample subject with data: ---\n{new_subject}\n")
    
    prediction_result = predict_risk(new_subject)
    
    if prediction_result:
        import json
        print("\n--- PHS Prediction Report ---")
        print(json.dumps(prediction_result, indent=2))
        print("---------------------------")
