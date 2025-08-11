# tools/data_ingestion/parsers/genomics_parser.py
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from tools.ontology.neuromarker import PatientRecord, GeneticData

def parse_genomics_data(patient_id, csv_path) -> PatientRecord:
    """
    Parses a genomics summary CSV and returns a standardized PatientRecord object.
    """
    record = PatientRecord(patient_id=patient_id, metadata={})
    record.genetics = GeneticData() # Initialize the genetics dataclass
    try:
        df = pd.read_csv(csv_path)
        patient_data = df[df['patient_id'] == patient_id]
        if patient_data.empty:
            return record

        if 'APOE4_alleles' in patient_data.columns:
             # This is a key marker, but also a risk allele. We store it in the genetics object.
            record.genetics.disease_specific_risk.append(f"APOE_e{int(patient_data['APOE4_alleles'].iloc[0])}")
            
        return record
    except Exception as e:
        print(f"Warning in genomics_parser for patient {patient_id}: {e}")
        return record
