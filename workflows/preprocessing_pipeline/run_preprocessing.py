# workflows/preprocessing_pipeline/run_preprocessing.py
import pandas as pd
from dataclasses import asdict, is_dataclass
import os
import sys
from enum import Enum

# Add project root to path for cross-module imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Import the necessary data adapter
from tools.data_ingestion.parsers.nacc_adapter import parse_nacc_data
from tools.ontology.neuromarker import PatientRecord, Biomarker, BiomarkerCategory

# --- CONFIGURATION ---
# Define input and output paths
NACC_DATA_INPUT_PATH = 'data/simulated/nacc_sample_data.csv'
FINAL_DATASET_OUTPUT_PATH = 'data/processed/analysis_ready_dataset.parquet'

def dataclass_to_dict(obj):
    """
    Recursively converts dataclass instances to dictionaries,
    handling Enum types by converting them to their string values.
    Also handles nested lists and dictionaries.
    """
    if is_dataclass(obj):
        return {field.name: dataclass_to_dict(getattr(obj, field.name))
                for field in obj.__dataclass_fields__.values()}
    elif isinstance(obj, Enum):
        return obj.value  # Convert Enum to its value (string)
    elif isinstance(obj, list):
        return [dataclass_to_dict(elem) for elem in obj]
    elif isinstance(obj, dict):
        return {k: dataclass_to_dict(v) for k, v in obj.items()}
    else:
        return obj

def main():
    """
    Main function to run the entire data preprocessing pipeline.
    It calls all available data adapters and merges their outputs into a
    single, analysis-ready dataset.
    """
    print("--- Starting Central Data Preprocessing Workflow ---")
    
    # In the future, we would call all adapters here:
    # adni_cohort = parse_adni_data(...)
    # ppmi_cohort = parse_ppmi_data(...)
    
    # For now, we only call the NACC adapter
    print(f"--> Ingesting data from NACC adapter using '{NACC_DATA_INPUT_PATH}'...")
    nacc_cohort = parse_nacc_data(NACC_DATA_INPUT_PATH)
    
    # Combine all cohorts into a single list of PatientRecord objects
    full_cohort = nacc_cohort # In future: adni_cohort + ppmi_cohort + ...
    
    if not full_cohort:
        print("!!! No patient records were ingested. Exiting pipeline.")
        return

    print(f"--> Total of {len(full_cohort)} records ingested.")

    # Prepare data for DataFrame creation
    patient_data_for_df = []
    biomarker_data_for_df = []

    for record in full_cohort:
        # Extract patient metadata and genetic data
        patient_dict = {
            'patient_id': record.patient_id,
            'schema_version': record.metadata.get('schema_version'),
            'ingestion_timestamp': record.metadata.get('ingestion_timestamp'),
            'source_dataset': record.metadata.get('source_dataset'),
            'genetic_key_markers': record.genetic_data.key_markers if record.genetic_data else None
        }
        patient_data_for_df.append(patient_dict)

        # Extract and flatten biomarkers
        for biomarker in record.biomarkers:
            biomarker_dict = {
                'patient_id': record.patient_id,
                'biomarker_name': biomarker.name,
                'biomarker_value': str(biomarker.value),
                'biomarker_unit': biomarker.unit,
                'biomarker_category': biomarker.category.value # Ensure enum is string
            }
            biomarker_data_for_df.append(biomarker_dict)

    # Create DataFrames
    patients_df = pd.DataFrame(patient_data_for_df)
    biomarkers_df = pd.DataFrame(biomarker_data_for_df)

    # Merge DataFrames
    # This will create a wide format where each biomarker is a column
    # For now, we'll keep it simple and just merge on patient_id
    # A more advanced approach would pivot biomarkers_df
    final_df = pd.merge(patients_df, biomarkers_df, on='patient_id', how='left')
    
    print(f"--> Successfully created a unified DataFrame with shape: {final_df.shape}")
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(FINAL_DATASET_OUTPUT_PATH), exist_ok=True)
    
    # Save the final DataFrame to Parquet format for efficiency
    print(f"--> Saving analysis-ready dataset to '{FINAL_DATASET_OUTPUT_PATH}'...")
    final_df.to_parquet(FINAL_DATASET_OUTPUT_PATH)
    
    print("--- Central Data Preprocessing Workflow Finished Successfully ---")
    print(f"\nFinal dataset is ready for model training at: {FINAL_DATASET_OUTPUT_PATH}")

if __name__ == '__main__':
    main()