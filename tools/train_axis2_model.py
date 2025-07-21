# tools/train_axis2_model.py
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_and_save_ptau_model(n_patients=200, model_dir='models'):
    """
    Generates synthetic data for pTau prediction, trains a model, and saves it.
    """
    print(f"Generating synthetic data for pTau model ({n_patients} patients)...")

    # Define archetypes for pTau Negative and Positive cases
    archetypes = {
        'pTau_Negative': {
            'n': int(n_patients * 0.6),
            'ADAS13_bl': (5, 15),
            'AGE': (60, 75),
            'APOE4': [0, 1],
            'Hippocampus': (3.5, 4.5),
            'Ventricles': (25, 40),
            'target': 0 # pTau-
        },
        'pTau_Positive': {
            'n': int(n_patients * 0.4),
            'ADAS13_bl': (12, 25),
            'AGE': (68, 85),
            'APOE4': [1, 2],
            'Hippocampus': (2.5, 3.6),
            'Ventricles': (40, 65),
            'target': 1 # pTau+
        }
    }

    all_patients = []
    for _, params in archetypes.items():
        data = {
            'ADAS13_bl': np.round(np.random.uniform(params['ADAS13_bl'][0], params['ADAS13_bl'][1], params['n']), 1),
            'APOE4': np.random.choice(params['APOE4'], params['n']),
            'AGE': np.round(np.random.uniform(params['AGE'][0], params['AGE'][1], params['n']), 1),
            'Hippocampus': np.round(np.random.uniform(params['Hippocampus'][0], params['Hippocampus'][1], params['n']), 2),
            'Ventricles': np.round(np.random.uniform(params['Ventricles'][0], params['Ventricles'][1], params['n']), 2),
            'pTau_positivity': [params['target']] * params['n']
        }
        all_patients.append(pd.DataFrame(data))

    # Combine, shuffle, and create final DataFrame
    df = pd.concat(all_patients).sample(frac=1).reset_index(drop=True)

    # Separate features (X) and target (y)
    X = df.drop('pTau_positivity', axis=1)
    y = df['pTau_positivity']

    # Train the Random Forest model
    print("Training pTau prediction model...")
    model = RandomForestClassifier(n_estimators=50, random_state=42, class_weight='balanced')
    model.fit(X, y)

    # Ensure the models directory exists
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Save the trained model
    model_path = os.path.join(model_dir, 'axis2_ptau_model.joblib')
    joblib.dump(model, model_path)

    print(f"✅ pTau model successfully trained and saved to '{model_path}'")

if __name__ == "__main__":
    train_and_save_ptau_model()