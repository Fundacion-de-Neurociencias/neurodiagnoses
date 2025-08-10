import subprocess
import random

# Import all necessary components from the modules we are about to create
from neurodiagnoses_code.axis_1.classifier import predict_etiology
from neurodiagnoses_code.axis_2.classifier import predict_probabilities as predict_axis2, CSF_FEATURES, train_model as train_axis2
from neurodiagnoses_code.axis_3.classifier import predict_probabilities as predict_axis3, NEURO_FEATURES, train_model as train_axis3
from neurodiagnoses_code.axis_2.generate_dataset import generate_data as generate_axis2_data
from neurodiagnoses_code.axis_3.generate_axis3_dataset import generate_data as generate_axis3_data

def run_simulation():
    """Main function to orchestrate the FULL 3-AXIS neurodiagnostic process."""
    print("=====================================================")
    print("===   STARTING 3-AXIS DIAGNOSTIC SIMULATION       ===")
    print("=====================================================")

    # --- Simulate Data for a Single Patient ---
    print("\n[INFO] Simulating a new patient's multi-modal data...")
    patient_axis1_data = {
        "genetics": {
            "pathogenic_variants": [],
            "disease_specific_risk": ["APOE_e4"],
            "non_specific_risk": ["APOE_e4_shared_signature"]
        }
    }
    patient_axis2_data = {protein: random.uniform(0.0, 2.5) for protein in CSF_FEATURES}
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
    if axis1_result:
        print("\n  [-- AXIS 1: ETIOLOGICAL PROFILE (Genetic Probability) --]")
        for disease, probability in sorted(axis1_result.items(), key=lambda item: item[1], reverse=True):
            if probability > 0.02:
                print(f"    - {disease:<25}: {probability:.2%}")
    if axis2_result:
        print("\n  [-- AXIS 2: MOLECULAR PROFILE (Disease Probability) --]")
        class_names = {0: 'Control (CO)', 1: 'Alzheimer (AD)', 2: 'Parkinson (PD)', 3: 'Frontotemporal (FTD)', 4: 'Cuerpos de Lewy (DLB)'}
        for class_index, probability in sorted(axis2_result.items(), key=lambda item: item[1], reverse=True):
            class_name = class_names.get(class_index, f"Unknown Class {class_index}")
            print(f"    - {class_name:<25}: {probability:.2%}")
    if axis3_result:
        print("\n  [-- AXIS 3: NEUROANATOMICAL-CLINICAL PROFILE --]")
        phenotype_names = {0: 'Tau-positive Phenotype', 1: 'TDP-43 Phenotype'}
        for class_index, probability in sorted(axis3_result.items(), key=lambda item: item[1], reverse=True):
            phenotype_name = phenotype_names.get(class_index, f"Unknown Phenotype {class_index}")
            print(f"    - {phenotype_name:<25}: {probability:.2%}")
    print("---------------------------------------------------------")

def main():
    # 1. Generate datasets
    print("--- Generating Datasets ---")
    generate_axis2_data()
    generate_axis3_data()

    # 2. Train models
    print("\n--- Training Models ---")
    train_axis2()
    train_axis3()

    # 3. Run simulation
    print("\n--- Running Simulation ---")
    run_simulation()

    # 4. Git commit
    print("\n--- Committing to Git ---")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "feat(system): Implement and integrate full 3-axis diagnostic system"])

if __name__ == "__main__":
    main()
