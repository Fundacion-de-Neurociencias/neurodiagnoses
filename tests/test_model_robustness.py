"""
Test for Model Adversarial Robustness.

This script contains tests to evaluate the stability of trained models when faced
with small, clinically plausible perturbations to input data.
"""

import pytest
import joblib
import pandas as pd
import os

# Define paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODEL_REGISTRY_DIR = os.path.join(PROJECT_ROOT, 'models')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')


@pytest.fixture
def ad_model_and_data():
    """Pytest fixture to load the AD model and data."""
    diagnosis_code = 'AD'
    model_path = os.path.join(MODEL_REGISTRY_DIR, diagnosis_code, 'screening_model.joblib')
    data_path = os.path.join(DATA_DIR, f'featured_data_{diagnosis_code}.parquet')
    
    model = joblib.load(model_path)
    df = pd.read_parquet(data_path)
    
    return model, df


def test_prediction_stability_on_age_perturbation(ad_model_and_data):
    """
    Tests if the model's prediction remains stable after a small change in age.
    
    A robust model should not change its prediction for a minor, clinically
    insignificant change in a single feature.
    """
    model, df = ad_model_and_data
    
    # Select a single patient (e.g., the first one)
    patient_data = df.head(1)
    features = patient_data.drop(columns=['patient_id', 'other_variants', 'diagnosis'])
    
    # 1. Get the original prediction
    original_prediction = model.predict(features)[0]
    
    # 2. Create perturbed data
    perturbed_features = features.copy()
    original_age = perturbed_features['age'].iloc[0]
    perturbed_features['age'] = original_age + 1 # Increase age by 1 year
    
    # 3. Get the new prediction
    perturbed_prediction = model.predict(perturbed_features)[0]
    
    # 4. Assert that the prediction has not changed
    print(f"\nOriginal prediction (age {original_age}): {original_prediction}")
    print(f"Perturbed prediction (age {original_age + 1}): {perturbed_prediction}")
    
    assert original_prediction == perturbed_prediction, \
        f"Prediction flipped from {original_prediction} to {perturbed_prediction} after a minor age change."

