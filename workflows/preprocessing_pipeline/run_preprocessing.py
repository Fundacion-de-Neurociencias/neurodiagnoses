# workflows/preprocessing_pipeline/run_preprocessing.py
import pandas as pd
from dataclasses import asdict
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from tools.data_ingestion.parsers.nacc_adapter import parse_nacc_data
# Import our new regional parser
from tools.data_ingestion.parsers.imaging_parser import parse_regional_imaging_data

# --- CONFIGURATION ---
NACC_DATA_INPUT_PATH = 'data/simulated/nacc_sample_data.csv'
REGIONAL_IMAGING_INPUT_PATH = 'data/simulated/regional_neuroimaging_data.csv'
FINAL_DATASET_OUTPUT_PATH = 'data/processed/analysis_ready_dataset.parquet'

def main():
    """
    Main function to run the data preprocessing pipeline.
    It now incorporates the new regional imaging data.
    """
    print("--- Starting Central Data Preprocessing Workflow ---")
    
    nacc_cohort = parse_nacc_data(NACC_DATA_INPUT_PATH)
    
    # Enrich each patient record with the new regional data
    for record in nacc_cohort:
        patient_id_num = int(record.patient_id.split('_')[1])
        regional_data_record = parse_regional_imaging_data(patient_id_num, REGIONAL_IMAGING_INPUT_PATH)
        # Merge biomarkers from regional data into the main record
        record.biomarkers.extend(regional_data_record.biomarkers)

    if not nacc_cohort:
        print("!!! No patient records were ingested. Exiting pipeline.")
        return

    print(f"--> Total of {len(nacc_cohort)} records ingested and enriched.")

    cohort_as_dicts = [asdict(record) for record in nacc_cohort]
    final_df = pd.json_normalize(cohort_as_dicts, sep='_')
    
    print(f"--> Successfully created a unified DataFrame with shape: {final_df.shape}")
    
    os.makedirs(os.path.dirname(FINAL_DATASET_OUTPUT_PATH), exist_ok=True)
    
    print(f"--> Saving analysis-ready dataset to '{FINAL_DATASET_OUTPUT_PATH}'...")
    final_df.to_parquet(FINAL_DATASET_OUTPUT_PATH)
    
    print("--- Central Data Preprocessing Workflow Finished Successfully ---")
    print(f"\nFinal dataset now includes regional imaging data and is ready for the new Axis 3 model.")

if __name__ == '__main__':
    main()
