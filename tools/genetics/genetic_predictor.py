

import pickle
import sys

# Load trained model
MODEL_PATH = "tools/genetics/genetic_risk_predictor.pkl"

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    print(f"❌ ERROR: Model file not found at {MODEL_PATH}")
    sys.exit(1)

def predict_variant_carrier(
    age_onset, family_members_affected, early_onset_in_family,
    parent_affected, apoe_e4_status, clinical_diagnosis
):
    """
    Predict probability of carrying a pathogenic variant.

    Parameters:
    - age_onset (int): Age at symptom onset
    - family_members_affected (int): Number of affected relatives
    - early_onset_in_family (0/1): Any early onset in family? (1=yes, 0=no)
    - parent_affected (0/1): Parent affected? (1=yes, 0=no)
    - apoe_e4_status (0/1): APOE ε4 carrier? (1=yes, 0=no)
    - clinical_diagnosis (str): One of [AD, FTD, VaD, PDD]

    Returns:
    - probability (float): Probability of being a variant carrier
    """
    # Encode clinical diagnosis
    diagnosis_mapping = {"AD": 0, "FTD": 1, "VaD": 2, "PDD": 3}
    diagnosis_encoded = diagnosis_mapping.get(clinical_diagnosis.upper(), None)
    if diagnosis_encoded is None:
        raise ValueError("Invalid clinical_diagnosis. Must be one of: AD, FTD, VaD, PDD.")

    # Build feature vector
    X = [[
        age_onset,
        family_members_affected,
        early_onset_in_family,
        parent_affected,
        apoe_e4_status,
        diagnosis_encoded
    ]]

    # Predict
    prob = model.predict_proba(X)[0][1]  # Probability of being a carrier
    return prob

def cli():
    print("\n Neurodiagnoses: Genetic Risk Predictor (Etiological Axis)")
    try:
        age_onset = int(input("Enter age at symptom onset: "))
        family_members_affected = int(input("Number of family members affected: "))
        early_onset_in_family = int(input("Any early onset in family? (1=yes, 0=no): "))
        parent_affected = int(input("Is a parent affected? (1=yes, 0=no): "))
        apoe_e4_status = int(input("APOE ε4 carrier? (1=yes, 0=no): "))
        clinical_diagnosis = input("Clinical diagnosis (AD, FTD, VaD, PDD): ").strip().upper()

        probability = predict_variant_carrier(
            age_onset,
            family_members_affected,
            early_onset_in_family,
            parent_e4_status,
            clinical_diagnosis
        )

        print(f"\n✅ Estimated probability of carrying a pathogenic variant: {probability:.2%}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    cli()

