"""
Disease-Specific Model Training and Registry with Model Cards.

This script trains a classification model for a specific disease cohort,
saves the model to a structured directory, and generates a metadata
Model Card for transparency and governance.

Functions:
    train_disease_specific_model: Main function for the training process.
"""

import pandas as pd
import os
import joblib
import json
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Define paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
MODEL_REGISTRY_DIR = os.path.join(PROJECT_ROOT, 'models')

def train_disease_specific_model(data_dir, model_dir, diagnosis_code):
    """
    Loads data, creates a target, trains a model, and saves it along with a
    metadata model card.
    """
    print(f"--- Starting model training for [{diagnosis_code}] ---")
    
    # --- 1. Load Disease-Specific Data ---
    input_filename = f"featured_data_{diagnosis_code}.parquet"
    input_path = os.path.join(data_dir, input_filename)
    try:
        df = pd.read_parquet(input_path)
    except FileNotFoundError:
        print(f"Error: Data file not found at {input_path}. Run feature engineering first.")
        return

    # --- 2. Create Synthetic Target Variable ('risk_group') ---
    df['risk_group'] = (df['MMSE'] < 25).astype(int)
    print(f"Created synthetic target 'risk_group' for {diagnosis_code}.")

    # --- 3. Define Features (X) and Target (y) ---
    features = df.drop(columns=['patient_id', 'other_variants', 'diagnosis', 'risk_group'])
    target = df['risk_group']

    # --- 4. Train the Classifier ---
    print(f"Training Logistic Regression model on {len(features)} samples...")
    model = LogisticRegression(random_state=42)
    model.fit(features, target)
    print("Model training complete.")

    # --- 5. Save the Trained Model to the Registry ---
    output_model_dir = os.path.join(model_dir, diagnosis_code)
    os.makedirs(output_model_dir, exist_ok=True)
    model_path = os.path.join(output_model_dir, 'screening_model.joblib')
    joblib.dump(model, model_path)
    print(f"Trained model saved to registry: {model_path}")

    # --- 6. Generate and Save Model Card ---
    # Calculate accuracy on the training data (for demonstration)
    train_accuracy = accuracy_score(target, model.predict(features))

    model_card = {
        "model_name": f"{diagnosis_code} Screening Panel",
        "model_version": "1.0",
        "diagnosis_code": diagnosis_code,
        "trained_at": datetime.now().isoformat(),
        "model_path": model_path,
        "training_data_path": input_path,
        "model_type": "Logistic Regression",
        "performance_metrics": {
            "training_accuracy": f"{train_accuracy:.2f}"
        },
        "intended_use": "To provide a preliminary risk assessment for a specific neurodegenerative disorder. Not for final clinical diagnosis.",
        "limitations": "Trained on a very small, synthetic dataset. Not suitable for clinical use without extensive validation."
    }
    card_path = os.path.join(output_model_dir, 'screening_model_card.json')
    with open(card_path, 'w') as f:
        json.dump(model_card, f, indent=4)
    print(f"Model Card saved to: {card_path}")
    print("----------------------------------------------------")
    print()

if __name__ == "__main__":
    diagnoses_to_process = ['AD', 'FTD']
    for diag in diagnoses_to_process:
        train_disease_specific_model(DATA_DIR, MODEL_REGISTRY_DIR, diag)
