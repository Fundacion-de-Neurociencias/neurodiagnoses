# tools/advanced_annotator/train_model.py
import os
import json
import pandas as pd
import xgboost as xgb
import joblib
from .run_advanced_annotation import flatten_patient_json

def create_training_dataset(database_path='patient_database'):
    """
    Loads all patient JSONs from the database, flattens them,
    and creates a training dataset (X, y).
    """
    all_features = []
    all_labels = []

    if not os.path.exists(database_path):
        print(f"Error: Database path '{database_path}' not found.")
        return None, None

    for filename in os.listdir(database_path):
        if filename.endswith(".json"):
            patient_path = os.path.join(database_path, filename)
            with open(patient_path, 'r') as f:
                patient_data = json.load(f)

            features = flatten_patient_json(patient_data)
            all_features.append(features)

            risk_score = 0
            if features.get('ADAS13_bl', 0) > 15: risk_score += 1
            if features.get('APOE4_alleles', 0) > 0: risk_score += 1
            if features.get('MMSE', 30) < 25: risk_score += 1

            label = 1 if risk_score >= 2 else 0
            all_labels.append(label)

    X = pd.DataFrame(all_features)
    y = pd.Series(all_labels)

    # --- FIX: Convert categorical text columns to numbers ---
    if 'sex' in X.columns:
        X = pd.get_dummies(X, columns=['sex'], drop_first=True, dtype=int)

    X = X.reindex(sorted(X.columns), axis=1).fillna(0)

    return X, y

def train_advanced_model():
    """Main function to train and save the advanced model."""
    print("--- Starting Advanced Model Training ---")

    X, y = create_training_dataset()
    if X is None or X.empty:
        print("Could not create a dataset. Aborting.")
        return

    print(f"✅ Training dataset created with {len(X)} samples and {len(X.columns)} features.")
    print("Training XGBoost model...")

    xgb_model = xgb.XGBClassifier(
        objective='binary:logistic',
        eval_metric='logloss',
        use_label_encoder=False,
        n_estimators=100,
        random_state=42
    )
    xgb_model.fit(X, y)

    model_path = 'models/advanced_annotator_model.joblib'
    os.makedirs('models', exist_ok=True)
    joblib.dump(xgb_model, model_path)

    print(f"✅ Advanced model trained and saved to '{model_path}'")

if __name__ == '__main__':
    train_advanced_model()