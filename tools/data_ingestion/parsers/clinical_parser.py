# tools/data_ingestion/parsers/clinical_parser.py
import pandas as pd

def parse_clinical_data(patient_id, csv_path):
    """
    Parses a clinical data CSV and extracts information for a specific patient.
    It's designed to be flexible and handle missing columns gracefully.
    """
    try:
        df = pd.read_csv(csv_path)
        patient_data = df[df['patient_id'] == patient_id]

        if patient_data.empty:
            return None

        output = {}
        
        # Demographics
        demographics = {}
        if 'age' in patient_data.columns: demographics['age'] = float(patient_data['age'].iloc[0])
        if 'sex' in patient_data.columns: demographics['sex'] = str(patient_data['sex'].iloc[0])
        if 'years_of_education' in patient_data.columns: demographics['years_of_education'] = int(patient_data['years_of_education'].iloc[0])
        if demographics: output['demographics'] = demographics

        # Cognitive Tests (as a flexible list)
        cognitive_tests = []
        if 'MMSE' in patient_data.columns:
            cognitive_tests.append({"test_name": "MMSE", "score": int(patient_data['MMSE'].iloc[0])})
        if 'ADAS13_bl' in patient_data.columns:
            cognitive_tests.append({"test_name": "ADAS13_bl", "score": float(patient_data['ADAS13_bl'].iloc[0])})
        if cognitive_tests: output['cognitive_tests'] = cognitive_tests
        
        return output

    except FileNotFoundError:
        print(f"Warning: Clinical data file not found at {csv_path}")
        return None
    except Exception as e:
        print(f"An error occurred in clinical_parser: {e}")
        return None

if __name__ == '__main__':
    test_patient_id = 'ND_001'
    test_csv_path = '../../clinical_data.csv'
    
    parsed_data = parse_clinical_data(test_patient_id, test_csv_path)
    
    if parsed_data:
        import json
        print(json.dumps(parsed_data, indent=2))
