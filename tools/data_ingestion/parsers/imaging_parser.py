# tools/data_ingestion/parsers/imaging_parser.py
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from tools.ontology.neuromarker import PatientRecord, Biomarker, BiomarkerCategory

def parse_imaging_data(patient_id, csv_path) -> PatientRecord:
    """
    Parses an imaging metrics CSV and returns a standardized PatientRecord object.
    """
    record = PatientRecord(patient_id=patient_id, metadata={})
    try:
        df = pd.read_csv(csv_path)
        patient_data = df[df['patient_id'] == patient_id]
        if patient_data.empty:
            return record

        if 'hippocampal_volume_norm' in patient_data.columns:
            record.add_biomarker("Hippocampal Volume (Norm)", float(patient_data['hippocampal_volume_norm'].iloc[0]), "mm^3", BiomarkerCategory.NEUROIMAGING)
        if 'cortical_thickness_avg' in patient_data.columns:
            record.add_biomarker("Cortical Thickness (Avg)", float(patient_data['cortical_thickness_avg'].iloc[0]), "mm", BiomarkerCategory.NEUROIMAGING)
            
        return record
    except Exception as e:
        print(f"Warning in imaging_parser for patient {patient_id}: {e}")
        return record
