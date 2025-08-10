import random
from neurodiagnoses_code.axis_1.classifier import predict_etiology
from neurodiagnoses_code.axis_2.classifier import predict_probabilities as predict_axis2, CSF_FEATURES
from neurodiagnoses_code.axis_3.classifier import predict_probabilities as predict_axis3, NEURO_FEATURES

def main():
    """Main function to orchestrate the FULL 3-AXIS neurodiagnostic process."""
    print("=====================================================")
    print("===   STARTING 3-AXIS DIAGNOSTIC SIMULATION       ===")
    print("=====================================================")
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
    print("\n[INFO] Sending data to Axis 1 (Etiology) Classifier...")
    axis1_result = predict_etiology(patient_axis1_data)
    print("\n[INFO] Sending data to Axis 2 (Molecular) Classifier...")
    axis2_result = predict_axis2(patient_axis2_data)
    print("\n[INFO] Sending data to Axis 3 (Phenotype) Classifier...")
    axis3_result = predict_axis3(patient_axis3_data)
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

if __name__ == '__main__':
    main()
