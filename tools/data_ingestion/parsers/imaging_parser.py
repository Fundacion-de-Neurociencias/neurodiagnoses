# tools/data_ingestion/parsers/imaging_parser.py
import os
import sys

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from tools.ontology.neuromarker import BiomarkerCategory, PatientRecord


def parse_regional_imaging_data(patient_id, csv_path) -> PatientRecord:
    """
    Parses a regional neuroimaging metrics CSV and returns a standardized
    PatientRecord object, adding each region as a separate biomarker.
    """
    record = PatientRecord(patient_id=patient_id, metadata={})
    try:
        df = pd.read_csv(csv_path)
        patient_data = df[df["patient_id"] == patient_id]
        if patient_data.empty:
            return record

        # Iterate through all columns except the patient ID
        for col_name in patient_data.columns:
            if col_name != "patient_id":
                value = patient_data[col_name].iloc[0]
                unit = "mm^3" if "volume" in col_name else "mm"

                record.add_biomarker(
                    name=col_name,
                    value=float(value),
                    unit=unit,
                    category=BiomarkerCategory.NEUROIMAGING,
                )
        return record
    except Exception as e:
        print(f"Warning in imaging_parser for patient {patient_id}: {e}")
        return record
