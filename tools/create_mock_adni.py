# tools/create_mock_adni.py
import pandas as pd
import numpy as np
import os

def create_mock_adni_data(n_patients=500, output_filename="df_clean (2).csv"):
    """
    Creates a mock ADNI dataset with the features required by the pTau notebook.
    """
    print(f"Generating mock ADNI data for {n_patients} patients...")

    # Define archetypes based on what we know the model needs
    archetypes = {
        'Control-Like': {
            'n': int(n_patients * 0.6),
            'ADAS13_bl': (5, 15), 'AGE': (60, 75), 'APOE4': [0, 1],
            'Hippocampus': (3.5, 4.5), 'Ventricles': (25, 40), 'pTau_positivity': 0
        },
        'Patient-Like': {
            'n': int(n_patients * 0.4),
            'ADAS13_bl': (12, 25), 'AGE': (68, 85), 'APOE4': [1, 2],
            'Hippocampus': (2.5, 3.6), 'Ventricles': (40, 65), 'pTau_positivity': 1
        }
    }

    all_subjects = []
    for _, params in archetypes.items():
        data = {
            'ADAS13_bl': np.round(np.random.uniform(params['ADAS13_bl'][0], params['ADAS13_bl'][1], params['n']), 1),
            'APOE4': np.random.choice(params['APOE4'], params['n']),
            'AGE': np.round(np.random.uniform(params['AGE'][0], params['AGE'][1], params['n']), 1),
            'Hippocampus': np.round(np.random.uniform(params['Hippocampus'][0], params['Hippocampus'][1], params['n']), 2),
            'Ventricles': np.round(np.random.uniform(params['Ventricles'][0], params['Ventricles'][1], params['n']), 2),
            # Add other columns the notebook might expect, even if just with dummy values
            'RID': np.random.randint(1000, 6000, params['n']),
            'PTGENDER': np.random.choice(['Male', 'Female'], params['n']),
            'PTEDUCAT': np.random.randint(12, 20, params['n']),
            'pTau_positivity': [params['pTau_positivity']] * params['n'] # Our target variable
        }
        all_subjects.append(pd.DataFrame(data))

    df = pd.concat(all_subjects).sample(frac=1).reset_index(drop=True)

    # Save the file in the specific directory the notebook expects
    output_dir = 'tools/ml_pipelines/src/modeling/adni_csf_prediction'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) # Should exist, but good practice
    
    output_path = os.path.join(output_dir, output_filename)
    df.to_csv(output_path, index=False)
    
    print(f"✅ Mock ADNI data successfully saved to '{output_path}'")

if __name__ == "__main__":
    create_mock_adni_data()