# tools/data_ingestion/parsers/clinical_parser.py
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from tools.ontology.neuromarker import PatientRecord, Biomarker, BiomarkerCategory

def parse_clinical_data(patient_id, csv_path) -> PatientRecord:
    """
    Parses a clinical data CSV and returns a standardized PatientRecord object.
    """
    record = PatientRecord(patient_id=patient_id, metadata={})
    try:
        df = pd.read_csv(csv_path)
        patient_data = df[df['patient_id'] == patient_id]
        if patient_data.empty:
            return record

        # Add biomarkers using the ontology
        if 'age' in patient_data.columns:
            record.add_biomarker("Age", float(patient_data['age'].iloc[0]), "years", BiomarkerCategory.CLINICAL_PHENOTYPIC)
        if 'sex' in patient_data.columns:
            record.add_biomarker("Sex", str(patient_data['sex'].iloc[0]), "category", BiomarkerCategory.CLINICAL_PHENOTYPIC)
        if 'MMSE' in patient_data.columns:
            record.add_biomarker("MMSE", int(patient_data['MMSE'].iloc[0]), "score", BiomarkerCategory.CLINICAL_PHENOTYPIC)
        if 'ADAS13_bl' in patient_data.columns:
            record.add_biomarker("ADAS13_bl", float(patient_data['ADAS13_bl'].iloc[0]), "score", BiomarkerCategory.CLINICAL_PHENOTYPIC)
        
        return record
    except Exception as e:
        print(f"Warning in clinical_parser for patient {patient_id}: {e}")
        return record # Return an empty record on failure
