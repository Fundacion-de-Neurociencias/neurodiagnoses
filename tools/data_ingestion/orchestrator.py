# tools/data_ingestion/orchestrator.py
import json
import os
from datetime import datetime
from dataclasses import asdict, replace

# Add project root to path for cross-module imports
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Import parsers and the core ontology
from tools.data_ingestion.parsers.clinical_parser import parse_clinical_data
from tools.data_ingestion.parsers.imaging_parser import parse_imaging_data
from tools.data_ingestion.parsers.genomics_parser import parse_genomics_data
from tools.ontology.neuromarker import PatientRecord

def merge_records(base_record: PatientRecord, new_record: PatientRecord) -> PatientRecord:
    """Helper function to merge two PatientRecord objects."""
    # This is a simple merge strategy. More complex logic could be added here.
    base_record.biomarkers.extend(new_record.biomarkers)
    if new_record.genetics:
        # Assumes genetics data is only parsed once, but merges if called multiple times
        if not base_record.genetics:
            base_record.genetics = new_record.genetics
        else:
            base_record.genetics.disease_specific_risk.extend(new_record.genetics.disease_specific_risk)
    return base_record

def ingest_generic_patient(patient_id, clinical_csv, imaging_csv, genomics_csv, output_dir='patient_database/generic'):
    """
    Orchestrates the ingestion of a patient from multiple generic CSV sources.
    This version is refactored to work with PatientRecord objects.
    """
    print(f"--- Starting generic ingestion for patient: {patient_id} ---")

    # Initialize a master PatientRecord for this patient
    master_record = PatientRecord(
        patient_id=str(patient_id),
        metadata={
            "schema_version": "1.2-neuromarker",
            "ingestion_timestamp": datetime.now().isoformat(),
            "source_dataset": "Generic Cohort"
        }
    )

    # Call each parser and merge the results into the master record
    print(f"Parsing clinical data...")
    clinical_record = parse_clinical_data(patient_id, clinical_csv)
    master_record = merge_records(master_record, clinical_record)

    print(f"Parsing imaging data...")
    imaging_record = parse_imaging_data(patient_id, imaging_csv)
    master_record = merge_records(master_record, imaging_record)
    
    print(f"Parsing genomics data...")
    genomics_record = parse_genomics_data(patient_id, genomics_csv)
    master_record = merge_records(master_record, genomics_record)

    # Save the final, merged PatientRecord as a JSON file
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{patient_id}.json")
    
    # Use 'asdict' to convert the dataclass object to a dictionary for JSON serialization
    with open(output_path, 'w') as f:
        json.dump(asdict(master_record), f, indent=2)

    print(f"✅ Ingestion complete. Unified patient data saved to: {output_path}")
    return output_path

if __name__ == '__main__':
    # This example demonstrates the generic ingestion pipeline.
    # We will use the sample CSV files in the root directory.
    print("--- Running a demonstration of the generic ingestion orchestrator ---")
    
    # In a real scenario, these files would be located in a structured 'data/' directory
    # For this test, we assume they are in the root.
    sample_clinical_path = 'clinical_data.csv'
    sample_imaging_path = 'imaging_metrics.csv'
    sample_genomics_path = 'genomics_summary.csv'
    sample_patient_id = 'ND_001' # Assuming this ID exists in the sample files
    
    # Create dummy files if they don't exist, to make the script runnable
    if not os.path.exists(sample_clinical_path):
        pd.DataFrame([{'patient_id': 'ND_001', 'age': 75, 'MMSE': 25}]).to_csv(sample_clinical_path, index=False)
    if not os.path.exists(sample_imaging_path):
        pd.DataFrame([{'patient_id': 'ND_001', 'hippocampal_volume_norm': 4500.0}]).to_csv(sample_imaging_path, index=False)
    if not os.path.exists(sample_genomics_path):
        pd.DataFrame([{'patient_id': 'ND_001', 'APOE4_alleles': 1}]).to_csv(sample_genomics_path, index=False)

    ingest_generic_patient(
        patient_id=sample_patient_id,
        clinical_csv=sample_clinical_path,
        imaging_csv=sample_imaging_path,
        genomics_csv=sample_genomics_path
    )
