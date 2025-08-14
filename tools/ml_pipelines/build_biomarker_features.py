"""
Disease-Specific Feature Engineering for Biomarker Modeling.

This script takes the unified multi-disease data and prepares it for machine
learning. It applies feature engineering logic that is specific to each
diagnostic group (e.g., AD, FTD).

Functions:
    create_disease_specific_features: Loads, filters, processes, and saves data.
"""

import pandas as pd
import os

# Define paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
INPUT_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'unified_patient_data.parquet')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')


def create_disease_specific_features(input_path, output_dir, diagnosis_code):
    """
    Loads unified data, filters for a specific diagnosis, and runs tailored
    feature engineering for that cohort.

    Args:
        input_path (str): Path to the unified Parquet file.
        output_dir (str): Directory to save the output feature file.
        diagnosis_code (str): The diagnosis to process (e.g., 'AD', 'FTD').

    Returns:
        pd.DataFrame: The feature-engineered DataFrame for the cohort.
    """
    print(f"--- Starting feature engineering for [{diagnosis_code}] ---")

    try:
        df = pd.read_parquet(input_path)
    except FileNotFoundError:
        print(f"Error: The file was not found at {input_path}. Run unification first.")
        return None

    # 1. Filter for the specific disease cohort
    df_cohort = df[df['diagnosis'] == diagnosis_code].copy()
    if df_cohort.empty:
        print(f"No data found for diagnosis code: {diagnosis_code}")
        return None

    # 2. Define base and disease-specific features
    base_features = [
        'patient_id', 'age', 'sex', 'years_of_education', 'MMSE',
        'hippocampal_volume_norm', 'cortical_thickness_avg', 'APOE4_alleles',
        'other_variants', 'diagnosis'
    ]
    
    disease_specific_features = []
    if diagnosis_code == 'AD':
        disease_specific_features = ['ADAS13_bl']
    elif diagnosis_code == 'FTD':
        disease_specific_features = ['CDR-SB']
    
    all_feature_cols = base_features + disease_specific_features
    
    # Select only columns that exist in the dataframe
    df_featured = df_cohort[[col for col in all_feature_cols if col in df_cohort.columns]].copy()
    print(f"Selected {len(df_featured.columns)} columns for {diagnosis_code} model.")

    # 3. Handle missing data
    df_featured.loc[:, 'other_variants'] = df_featured['other_variants'].fillna('None')
    print("Filled missing values.")

    # 4. Encode categorical variables
    df_featured = pd.get_dummies(df_featured, columns=['sex'], drop_first=True, dtype=int)
    print("Encoded categorical variables.")

    # --- Save Processed Data ---
    output_filename = f"featured_data_{diagnosis_code}.parquet"
    output_path = os.path.join(output_dir, output_filename)
    os.makedirs(output_dir, exist_ok=True)
    df_featured.to_parquet(output_path, index=False)
    print(f"Feature-engineered data saved to: {output_path}")

    # --- Display Summary ---
    print(f"\n--- Featured DataFrame Summary for {diagnosis_code} ---")
    df_featured.info()
    print(df_featured.head())
    print("----------------------------------------------------")
    print() # Add a newline for spacing

    return df_featured

if __name__ == "__main__":
    # Run the process for all desired diagnostic groups
    diagnoses_to_process = ['AD', 'FTD']
    for diag in diagnoses_to_process:
        create_disease_specific_features(INPUT_PATH, OUTPUT_DIR, diag)
