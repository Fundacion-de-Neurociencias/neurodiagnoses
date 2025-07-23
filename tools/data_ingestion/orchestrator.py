# tools/advanced_annotator/run_advanced_annotation.py
import json
import os
import pandas as pd
import joblib

def flatten_patient_json(patient_data):
    """
    Extracts and flattens all available features from a patient JSON object
    into a single dictionary (a feature vector).
    """
    features = {}
    if patient_data.get("clinical_data"):
        clinical = patient_data["clinical_data"]
        if clinical.get("demographics"):
            features.update(clinical["demographics"])
        if clinical.get("cognitive_tests"):
            for test in clinical["cognitive_tests"]:
                if "test_name" in test and "score" in test:
                    features[test["test_name"]] = test["score"]
    if patient_data.get("genetic_data"):
        genetic = patient_data["genetic_data"]
        if genetic.get("key_markers"):
            features.update(genetic["key_markers"])
        if genetic.get("variant_summary"):
            features["variant_summary_count"] = len(genetic["variant_summary"])
    if patient_data.get("imaging_data"):
        imaging = patient_data["imaging_data"]
        if imaging.get("derived_metrics"):
            features.update(imaging["derived_metrics"])
    return features

def run_pipeline(patient_json_path):
    """
    Main function to run the advanced annotation pipeline.
    It now loads a model, predicts, and formats a full annotation.
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
    print("✅ Features extracted and flattened.")

    # 3. Load the pre-trained advanced model
    model_path = 'models/advanced_annotator_model.joblib'
    try:
        model = joblib.load(model_path)
        print(f"✅ Advanced model loaded from '{model_path}'.")
    except FileNotFoundError:
        print(f"Error: Model not found at '{model_path}'. Please run the training script.")
        return

    # 4. Prepare data for prediction
    # The model expects a DataFrame with columns in a specific order.
    df_for_prediction = pd.DataFrame([feature_vector])

    # We must align the columns with the training data (sorted alphabetically)
    # First, get the feature names the model was trained on
    model_features = model.get_booster().feature_names
    df_for_prediction = df_for_prediction.reindex(columns=model_features).fillna(0)

    # 5. Make a prediction
    prediction = model.predict(df_for_prediction)[0]
    prediction_label = "High_Risk_Profile" if prediction == 1 else "Low_Risk_Profile"
    print(f"✅ Prediction complete: {prediction_label}")

    # 6. Format the final 3-axis annotation
    axis1 = f"Etiology based on clinical data (APOE4: {feature_vector.get('APOE4_alleles', 'N/A')})"
    axis2_and_3 = f"Multi-modal AI prediction: {prediction_label} (based on {len(feature_vector)} features)"

    timestamp = datetime.now().strftime('%Y-%m-%d')
    full_annotation = f"[{timestamp}]: {axis1} / {axis2_and_3}"

    print("\n--- FINAL ADVANCED ANNOTATION ---")
    print(full_annotation)
    print("-----------------------------------")

if __name__ == '__main__':
    patient_file = 'patient_database/ND_001.json'
    run_pipeline(patient_json_path=patient_file)