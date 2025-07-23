# tools/advanced_annotator/run_advanced_annotation.py
import json
import os

def flatten_patient_json(patient_data):
    """
    Extracts and flattens all available features from a patient JSON object
    into a single dictionary (a feature vector).
    """
    features = {}

    # Extract clinical data
    if patient_data.get("clinical_data"):
        clinical = patient_data["clinical_data"]
        if clinical.get("demographics"):
            features.update(clinical["demographics"])
        
        # Flexibly extract cognitive test scores
        if clinical.get("cognitive_tests"):
            for test in clinical["cognitive_tests"]:
                if "test_name" in test and "score" in test:
                    features[test["test_name"]] = test["score"]

    # Extract genetic data
    if patient_data.get("genetic_data"):
        genetic = patient_data["genetic_data"]
        if genetic.get("key_markers"):
            features.update(genetic["key_markers"])
        
        # Add a count of other significant variants
        if genetic.get("variant_summary"):
            features["variant_summary_count"] = len(genetic["variant_summary"])

    # Extract imaging data
    if patient_data.get("imaging_data"):
        imaging = patient_data["imaging_data"]
        if imaging.get("derived_metrics"):
            features.update(imaging["derived_metrics"])
            
    return features

def run_pipeline(patient_json_path):
    """
    Main function to run the advanced annotation pipeline.
    For now, it loads, flattens, and prints the feature vector.
    """
    print(f"--- Running Advanced Annotation Pipeline for {patient_json_path} ---")
    
    # 1. Load patient JSON
    try:
        with open(patient_json_path, 'r') as f:
            patient_data = json.load(f)
        print("✅ Patient JSON loaded successfully.")
    except FileNotFoundError:
        print(f"Error: Patient file not found at {patient_json_path}")
        return

    # 2. Extract and flatten features
    feature_vector = flatten_patient_json(patient_data)
    print("✅ Features extracted and flattened:")
    
    # Pretty-print the resulting feature vector
    print(json.dumps(feature_vector, indent=2))
    
    # (Future steps: 3. Load Model, 4. Predict, 5. Format Annotation)
    
    print("\n--- Pipeline finished ---")


if __name__ == '__main__':
    # Example of how to run the pipeline on the patient we ingested
    patient_file = 'patient_database/ND_001.json'
    run_pipeline(patient_json_path=patient_file)