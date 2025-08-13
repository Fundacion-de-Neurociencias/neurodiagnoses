# tools/data_ingestion/parsers/nacc_adapter.py
import os

# Add project root to path for cross-module imports
import sys
from typing import List

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from tools.ontology.neuromarker import BiomarkerCategory, GeneticData, PatientRecord


def parse_nacc_data(csv_path: str) -> List[PatientRecord]:
    """
    Parses a NACC-like CSV file and converts each patient row into a
    standardized PatientRecord object using the Neuromarker ontology.

    Args:
        csv_path (str): The path to the NACC data CSV file.

    Returns:
        A list of PatientRecord objects.
    """
    print(f"--- Parsing NACC data from: {csv_path} ---")
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"ERROR: NACC data file not found at {csv_path}")
        return []

    patient_records = []
    for _, row in df.iterrows():
        patient_id = f"NACC_{row['participant_id']}"

        # Create the base record
        record = PatientRecord(
            patient_id=patient_id,
            metadata={"source_dataset": "NACC", "schema_version": "1.2-neuromarker"},
        )

        # Add biomarkers using the ontology
        record.add_biomarker(
            "Age", row["age"], "years", BiomarkerCategory.CLINICAL_PHENOTYPIC
        )
        record.add_biomarker(
            "Sex",
            "Female" if row["sex"] == "F" else "Male",
            "category",
            BiomarkerCategory.CLINICAL_PHENOTYPIC,
        )
        record.add_biomarker(
            "MMSE", row["MMSE"], "score", BiomarkerCategory.CLINICAL_PHENOTYPIC
        )
        record.add_biomarker("GFAP", row["GFAP"], "pg/mL", BiomarkerCategory.FLUID)
        record.add_biomarker("NfL", row["NfL"], "pg/mL", BiomarkerCategory.FLUID)
        record.add_biomarker("pTau", row["ptau"], "pg/mL", BiomarkerCategory.FLUID)
        record.add_biomarker("Abeta42", row["abeta"], "pg/mL", BiomarkerCategory.FLUID)
        record.add_biomarker(
            "Hippocampal Volume",
            row["hippocampal_vol"],
            "mm^3",
            BiomarkerCategory.NEUROIMAGING,
        )

        # Add genetic data
        record.genetics = GeneticData()
        if row["apoe4"] > 0:
            record.genetics.key_markers["APOE4"] = f"APOE_e{int(row['apoe4'])}"

        patient_records.append(record)

    print(f"--> Successfully parsed {len(patient_records)} patient records.")
    return patient_records
