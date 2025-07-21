# tools/data_generator.py
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
import joblib

def generate_and_train(n_patients=200, model_dir='models', data_dir='data'):
    """
    Generates synthetic data, trains a model, and saves both.
    """
    # --- 1. Generate Synthetic Data (same as before) ---
    print(f"Generating synthetic data for {n_patients} patients...")
    archetypes = {
        'Healthy-Control': {
            'n': int(n_patients * 0.4), 'age': (50, 75), 'MMSE': (28, 30),
            'hippocampal_volume': (4.0, 5.0), 'cortical_thickness': (2.5, 3.0),
            'ventricular_volume': (20, 30), 'label': 'no significant findings'
        },
        'Early-AD': {
            'n': int(n_patients * 0.4), 'age': (65, 85), 'MMSE': (21, 27),
            'hippocampal_volume': (2.8, 3.8), 'cortical_thickness': (1.8, 2.4),
            'ventricular_volume': (35, 50),
            'label': 'right hippocampus: memory deficits; parietal lobe: visuospatial impairment (?)'
        },
        'Advanced-AD': {
            'n': int(n_patients * 0.2), 'age': (70, 90), 'MMSE': (15, 20),
            'hippocampal_volume': (2.0, 2.7), 'cortical_thickness': (1.4, 1.9),
            'ventricular_volume': (55, 75),
            'label': 'prefrontal cortex: executive dysfunction; temporal lobe: language deficits'
        }
    }
    all_patients = []
    for _, params in archetypes.items():
        data = {
            'age': np.random.randint(params['age'][0], params['age'][1], params['n']),
            'MMSE': np.random.randint(params['MMSE'][0], params['MMSE'][1], params['n']),
            'hippocampal_volume': np.round(np.random.uniform(params['hippocampal_volume'][0], params['hippocampal_volume'][1], params['n']), 2),
            'cortical_thickness': np.round(np.random.uniform(params['cortical_thickness'][0], params['cortical_thickness'][1], params['n']), 2),
            'ventricular_volume': np.round(np.random.uniform(params['ventricular_volume'][0], params['ventricular_volume'][1], params['n']), 2),
            'phenotype': [params['label']] * params['n']
        }
        all_patients.append(pd.DataFrame(data))
    df = pd.concat(all_patients).sample(frac=1).reset_index(drop=True)
    if not os.path.exists(data_dir): os.makedirs(data_dir)
    data_path = os.path.join(data_dir, 'synthetic_patient_data_axis3.csv')
    df.to_csv(data_path, index=False)
    print(f"✅ Synthetic data saved to '{data_path}'")

    # --- 2. Train and Save the Model (NEW) ---
    print("Training model on generated data...")
    X = df.drop('phenotype', axis=1)
    y = df['phenotype']
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    model_path = os.path.join(model_dir, 'axis3_model.joblib')
    joblib.dump(model, model_path)
    print(f"✅ Model trained and saved to '{model_path}'")

if __name__ == "__main__":
    generate_and_train()