#!/bin/bash
# Gemini Script to implement Axis 1, update the main orchestrator, run, and consolidate.
set -e

echo "--> STEP 1: Scaffolding Axis 1 (Etiology) module..."
mkdir -p neurodiagnoses_code/axis_1

# Create the rules-based classifier for Axis 1.
# Logic and comments are in English as requested.
cat <<EOF > neurodiagnoses_code/axis_1/classifier.py
import numpy as np

# --- GENETIC VARIANT KNOWLEDGE BASE ---
# This data is based on the user-provided specification.

PATHOGENIC_MAP = {
    "PSEN1": "AD", "PSEN2": "AD", "APP": "AD", # Autosomal Dominant Alzheimer's
    "HTT": "Huntington's",
    "GRN": "FTD", "MAPT": "FTD", "C9orf72": "FTD/ALS"
}

SPECIFIC_RISK_MAP = {
    "APOE_e4": {"disease": "AD", "multiplier": 1.5} # Increases AD probability
}

NON_SPECIFIC_RISK_MAP = {
    "APOE_e4_shared_signature": {"diseases": ["AD", "PD", "FTD"], "boost": 0.1} # Small boost to several NDDs
}

# Define the primary classes our system diagnoses
DISEASE_CLASSES = ['AD', 'PD', 'FTD', 'DLB', 'CO', "Huntington's", 'FTD/ALS']

def predict_etiology(patient_genetics: dict) -> dict:
    """
    Predicts disease probabilities based on a rules-engine for genetic variants.

    This function implements the logic for the Axis 1 (Etiology) classifier.
    It adjusts probabilities based on pathogenic, specific risk, and non-specific risk variants.

    Args:
        patient_genetics (dict): A dictionary with the patient's genetic profile.
            Expected format: {"genetics": {"pathogenic_variants": [...], "disease_specific_risk": [...], ...}}

    Returns:
        A dictionary mapping disease labels to their calculated probabilities.
    """
    # Start with a baseline, low-confidence probability for all classes
    probabilities = {disease: 1.0 / len(DISEASE_CLASSES) for disease in DISEASE_CLASSES}

    genetics = patient_genetics.get("genetics", {})
    
    # 1. Process Pathogenic Variants (Highest Impact)
    for variant in genetics.get("pathogenic_variants", []):
        variant_gene = variant.split('_')[0] # e.g., "PSEN1_p.A431E" -> "PSEN1"
        if variant_gene in PATHOGENIC_MAP:
            disease = PATHOGENIC_MAP[variant_gene]
            # Set a near-deterministic probability for the causative disease
            for d in probabilities:
                probabilities[d] = 0.01 # Set a low baseline for others
            probabilities[disease] = 1.0 - (0.01 * (len(DISEASE_CLASSES) - 1))
            # If a pathogenic variant is found, its impact overrides others, so we can stop.
            return probabilities

    # 2. Process Specific Risk Polymorphisms
    for variant in genetics.get("disease_specific_risk", []):
        if variant in SPECIFIC_RISK_MAP:
            risk_info = SPECIFIC_RISK_MAP[variant]
            disease = risk_info["disease"]
            multiplier = risk_info["multiplier"]
            if disease in probabilities:
                probabilities[disease] *= multiplier

    # 3. Process Non-Specific Risk Polymorphisms
    for variant in genetics.get("non_specific_risk", []):
        if variant in NON_SPECIFIC_RISK_MAP:
            risk_info = NON_SPECIFIC_RISK_MAP[variant]
            for disease in risk_info["diseases"]:
                if disease in probabilities:
                    probabilities[disease] += risk_info["boost"]

    # 4. Normalize probabilities to sum to 1.0
    total_prob = sum(probabilities.values())
    if total_prob > 0:
        for disease in probabilities:
            probabilities[disease] /= total_prob
    
    return probabilities

EOF
echo "--> Axis 1 module created."


echo -e "\n--> STEP 2: Updating 'run_neurodiagnosis.py' to be a full 3-axis orchestrator..."
cat <<EOF > run_neurodiagnosis.py
import random
from neurodiagnoses_code.axis_1.classifier import predict_etiology
from neurodiagnoses_code.axis_2.classifier import predict_probabilities as predict_axis2, CSF_FEATURES
from neurodiagnoses_code.axis_3.classifier import predict_probabilities as predict_axis3, NEURO_FEATURES

def main():
    """Main function to orchestrate the FULL 3-AXIS neurodiagnostic process."""
    print("=====================================================")
    print("===   STARTING 3-AXIS DIAGNOSTIC SIMULATION       ===")
    print("=====================================================")

    # --- Simulate Data for a Single Patient ---
    print("\n[INFO] Simulating a new patient's multi-modal data...")
    # Axis 1 Data (Genetics) - Example for a patient with APOE e4 risk
    patient_axis1_data = {
        "genetics": {
            "pathogenic_variants": [],
            "disease_specific_risk": ["APOE_e4"],
            "non_specific_risk": ["APOE_e4_shared_signature"]
        }
    }
    # Axis 2 Data (Proteomics)
    patient_axis2_data = {protein: random.uniform(0.0, 2.5) for protein in CSF_FEATURES}
    # Axis 3 Data (Neuroimaging)
    patient_axis3_data = {feature: random.uniform(0.0, 1.5) for feature in NEURO_FEATURES}
    print("  > Patient data simulation complete.")

    # --- Run Predictions for all three axes ---
    print("\n[INFO] Sending data to Axis 1 (Etiology) Classifier...")
    axis1_result = predict_etiology(patient_axis1_data)
    print("\n[INFO] Sending data to Axis 2 (Molecular) Classifier...")
    axis2_result = predict_axis2(patient_axis2_data)
    print("\n[INFO] Sending data to Axis 3 (Phenotype) Classifier...")
    axis3_result = predict_axis3(patient_axis3_data)

    # --- Display Combined Results ---
    print("\n\n----------------- FINAL 3-AXIS REPORT -----------------")
    # Display Axis 1 Results
    if axis1_result:
        print("\n  [-- AXIS 1: ETIOLOGICAL PROFILE (Genetic Probability) --]")
        for disease, probability in sorted(axis1_result.items(), key=lambda item: item[1], reverse=True):
            if probability > 0.02: # Only show relevant probabilities
                print(f"    - {disease:<25}: {probability:.2%}")
    # Display Axis 2 Results
    if axis2_result:
        print("\n  [-- AXIS 2: MOLECULAR PROFILE (Disease Probability) --]")
        class_names = {0: 'Control (CO)', 1: 'Alzheimer (AD)', 2: 'Parkinson (PD)', 3: 'Frontotemporal (FTD)', 4: 'Cuerpos de Lewy (DLB)'}
        for class_index, probability in sorted(axis2_result.items(), key=lambda item: item[1], reverse=True):
            class_name = class_names.get(class_index, f"Unknown Class {class_index}")
            print(f"    - {class_name:<25}: {probability:.2%}")
    # Display Axis 3 Results
    if axis3_result:
        print("\n  [-- AXIS 3: NEUROANATOMICAL-CLINICAL PROFILE --]")
        phenotype_names = {0: 'Tau-positive Phenotype', 1: 'TDP-43 Phenotype'}
        for class_index, probability in sorted(axis3_result.items(), key=lambda item: item[1], reverse=True):
            phenotype_name = phenotype_names.get(class_index, f"Unknown Phenotype {class_index}")
            print(f"    - {phenotype_name:<25}: {probability:.2%}")
    print("---------------------------------------------------------")

if __name__ == '__main__':
    main()
EOF

echo "--> Main script updated to 3 axes."


echo -e "\n--> STEP 3: Executing the full 3-axis diagnostic script..."
# Re-train models to ensure they exist before running the main script
python neurodiagnoses_code/axis_2/classifier.py
python neurodiagnoses_code/axis_3/classifier.py
# Run the main orchestrator
python run_neurodiagnosis.py


echo -e "\n--> STEP 4: Consolidating all work on the 3 axes to GitHub..."
git add .
git commit -m "feat(ia): Implement rules-based Axis 1 and 3-axis report" -m "
- Implements the Axis 1 (Etiology) classifier as a rules-based engine based on genetic variant specification.
- The main 'run_neurodiagnosis.py' script is now a full 3-axis orchestrator, calling the classifiers for all three axes.
- The final output is a comprehensive diagnostic report showing probabilities from the genetic, molecular, and neuroanatomical profiles.
"
git push

echo -e "\n--> SCRIPT FINALIZADO. Prototipo de 3 ejes completado y sincronizado."
