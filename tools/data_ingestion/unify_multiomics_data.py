"""
Unified Multi-omics Data Ingestion Module for Multiple NDDs.

This script is the first step in the diagnostic pipeline. It reads data from
multiple disease cohorts (e.g., AD, FTD), adds a 'diagnosis' label, and
unifies them with other data modalities (imaging, genomics) into a single
patient-centric DataFrame. The result is saved in Parquet format.

Functions:
    unify_multi_disease_data: Loads, merges, and saves the multi-omics data.
"""

import pandas as pd
import os

# Define absolute paths for input files relative to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
AD_CLINICAL_PATH = os.path.join(PROJECT_ROOT, 'clinical_data.csv')
FTD_CLINICAL_PATH = os.path.join(PROJECT_ROOT, 'ftd_clinical_data.csv')
IMAGING_DATA_PATH = os.path.join(PROJECT_ROOT, 'imaging_metrics.csv')
GENOMICS_DATA_PATH = os.path.join(PROJECT_ROOT, 'genomics_summary.csv')

# Define the output path for the processed data
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
OUTPUT_PATH = os.path.join(PROCESSED_DATA_DIR, 'unified_patient_data.parquet')

def unify_multi_disease_data():
    """
    Loads data from multiple disease cohorts, adds diagnosis labels,
    concatenates them, merges with other modalities, and saves the result.

    Returns:
        pd.DataFrame: The unified DataFrame containing all patient data.
    """
    print("Starting multi-disease data unification process...")

    # --- Load Data and Add Diagnosis Label ---
    try:
        ad_df = pd.read_csv(AD_CLINICAL_PATH)
        ad_df['diagnosis'] = 'AD'

        ftd_df = pd.read_csv(FTD_CLINICAL_PATH)
        ftd_df['diagnosis'] = 'FTD'

        imaging_df = pd.read_csv(IMAGING_DATA_PATH)
        genomics_df = pd.read_csv(GENOMICS_DATA_PATH)
        print("Successfully loaded all source CSV files.")
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure all source CSV files exist.")
        return None

    # --- Concatenate Clinical Cohorts ---
    # This handles different columns between cohorts (e.g., ADAS13 vs CDR-SB)
    combined_clinical_df = pd.concat([ad_df, ftd_df], ignore_index=True)
    print("Successfully combined AD and FTD clinical cohorts.")

    # --- Merge with Other Modalities ---
    merged_df = pd.merge(combined_clinical_df, imaging_df, on='patient_id', how='left')
    unified_df = pd.merge(merged_df, genomics_df, on='patient_id', how='left')
    print("Successfully merged all data sources.")

    # --- Save Processed Data ---
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    unified_df.to_parquet(OUTPUT_PATH, index=False)
    print(f"Unified data saved to: {OUTPUT_PATH}")

    # --- Display Summary ---
    print("\n--- Unified DataFrame Summary ---")
    unified_df.info()
    print("\n--- Unified Data Sample ---")
    print(unified_df.head())
    print(unified_df.tail())
    print("\n---------------------------")

    return unified_df

if __name__ == "__main__":
    unify_multi_disease_data()
