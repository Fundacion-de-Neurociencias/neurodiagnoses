# tools/data_ingestion/parsers/cornblath_adapter.py
import pandas as pd
import os

def parse_cornblath_patient(patient_id, data_dir='data/cornblath'):
    """
    Parses the Cornblath et al. dataset files for a specific patient
    and maps the data to the Neurodiagnoses JSON schema v1.1.
    """
    try:
        # Load the required CSV files
        pathology_df = pd.read_csv(os.path.join(data_dir, 'pathology_matrix.csv'))
        clinical_df = pd.read_csv(os.path.join(data_dir, 'clinical_data.csv'))
        genetic_df = pd.read_csv(os.path.join(data_dir, 'genetic_data.csv'))
    except FileNotFoundError as e:
        print(f"Error: A required data file is missing from '{data_dir}'. Details: {e}")
        return None

    # --- Find the patient in each dataframe ---
    pathology_data = pathology_df[pathology_df['projid'] == patient_id]
    clinical_data = clinical_df[clinical_df['projid'] == patient_id]
    genetic_data = genetic_df[genetic_df['projid'] == patient_id]

    if clinical_data.empty:
        print(f"Error: Patient ID {patient_id} not found in clinical_data.csv.")
        return None

    # --- Build the JSON object ---
    patient_json = {}

    # 1. Clinical Data
    patient_json['clinical_data'] = {
        'demographics': {
            'age': int(clinical_data['age_death'].iloc[0]),
            'sex': 'Male' if int(clinical_data['sex'].iloc[0]) == 1 else 'Female',
            'years_of_education': int(clinical_data['educ'].iloc[0])
        },
        'cognitive_tests': [
            {"test_name": "MMSE_last", "score": int(clinical_data['cts_mmse30_last'].iloc[0])}
        ]
    }

    # 2. Genetic Data
    if not genetic_data.empty:
        patient_json['genetic_data'] = {
            'key_markers': {
                'APOE4_alleles': int(genetic_data['apoe_genotype'].iloc[0])
            }
        }

    # 3. Neuropathology Data (New Schema Section)
    if not pathology_data.empty:
        patient_json['neuropathology_data'] = {
            'pathology_scores': pathology_data.drop(columns=['projid']).to_dict('records')[0]
        }
        
    return patient_json


if __name__ == '__main__':
    # Example usage: Parse a specific patient from the dataset
    # Make sure you have downloaded the CSVs into 'data/cornblath/'
    
    # Let's pick a sample patient ID from the dataset
    sample_patient_id = 4101131 
    
    parsed_patient = parse_cornblath_patient(patient_id=sample_patient_id)
    
    if parsed_patient:
        import json
        print("--- Parsed Cornblath Patient Data ---")
        print(json.dumps(parsed_patient, indent=2))