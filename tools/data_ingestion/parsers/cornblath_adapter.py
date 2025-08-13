# tools/data_ingestion/parsers/cornblath_adapter.py
import os

# Add project root to path for cross-module imports
import sys

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from tools.ontology.neuromarker import BiomarkerCategory, GeneticData, PatientRecord


def parse_cornblath_patient(patient_id, metadata, data_dir="data/cornblath"):
    """
    Parses the Cornblath et al. dataset and maps the data to a PatientRecord object.
    This version is refactored to use the Neuromarker ontology.
    """
    try:
        pathology_df = pd.read_csv(
            os.path.join(data_dir, "cornblath/pathology_matrix.csv")
        )
        clinical_df = pd.read_csv(os.path.join(data_dir, "clinical_data.csv"))
        genetic_df = pd.read_csv(os.path.join(data_dir, "genomics_summary.csv"))
    except FileNotFoundError as e:
        print(f"Error: A required data file is missing. Details: {e}")
        return None

    clinical_data = clinical_df[clinical_df["projid"] == patient_id]
    if clinical_data.empty:
        print(f"Error: Patient ID {patient_id} not found in clinical_data.csv.")
        return None

    # --- Build the PatientRecord object ---
    record = PatientRecord(patient_id=str(patient_id), metadata=metadata)

    # 1. Clinical Data & Biomarkers
    # The original script put these in a 'clinical_data' dict. We'll add them as biomarkers.
    record.add_biomarker(
        name="age_at_death",
        value=int(clinical_data["age_death"].iloc[0]),
        unit="years",
        category=BiomarkerCategory.CLINICAL_PHENOTYPIC,
    )
    record.add_biomarker(
        name="education",
        value=int(clinical_data["educ"].iloc[0]),
        unit="years",
        category=BiomarkerCategory.CLINICAL_PHENOTYPIC,
    )
    record.add_biomarker(
        name="MMSE_last",
        value=int(clinical_data["cts_mmse30_last"].iloc[0]),
        unit="points",
        category=BiomarkerCategory.CLINICAL_PHENOTYPIC,
    )

    # 2. Genetic Data
    genetic_data = genetic_df[genetic_df["projid"] == patient_id]
    if not genetic_data.empty:
        record.genetic_data = GeneticData(
            key_markers={"APOE_alleles": int(genetic_data["apoe_genotype"].iloc[0])}
        )

    # 3. Neuropathology Data
    pathology_data = pathology_df[pathology_df["projid"] == patient_id]
    if not pathology_data.empty:
        record.neuropathology_data = pathology_data.drop(columns=["projid"]).to_dict(
            "records"
        )[0]

    return record


if __name__ == "__main__":
    # Example usage requires the orchestrator to pass metadata
    print("This script is a module and should be called by an orchestrator.")
    print("To test, run 'tools/data_ingestion/orchestrator.py'")
