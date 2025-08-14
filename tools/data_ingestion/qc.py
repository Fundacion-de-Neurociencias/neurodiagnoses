
"""
Data Quality Control (QC) Module.

This script performs a series of data quality checks on the unified patient
data to ensure its integrity before it is used for model training or inference.

Functions:
    run_qc_checks: Main function to execute all QC steps.
    check_missing_values: Reports the percentage of missing values per column.
    check_data_types: Verifies that key columns have the expected data types.
    check_value_ranges: Performs sanity checks on the ranges of specific columns.
"""

import pandas as pd
import os

# Define the path to the processed data file
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
INPUT_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'unified_patient_data.parquet')

def check_missing_values(df):
    """Reports the percentage of missing values for each column."""
    print("--- 1. Checking for Missing Values ---")
    missing_percentage = df.isnull().sum() * 100 / len(df)
    missing_report = missing_percentage[missing_percentage > 0].sort_values(ascending=False)
    if not missing_report.empty:
        print("Columns with missing values:")
        print(missing_report)
    else:
        print("No missing values found.")
    print("--------------------------------------\n")

def check_data_types(df):
    """Verifies that key columns have expected data types."""
    print("--- 2. Checking Data Types ---")
    expected_types = {
        'age': 'float',
        'years_of_education': 'int',
        'MMSE': 'int',
        'ADAS13_bl': 'float',
        'hippocampal_volume_norm': 'float',
        'cortical_thickness_avg': 'float',
        'APOE4_alleles': 'int'
    }
    
    all_correct = True
    for col, dtype in expected_types.items():
        if col in df.columns and df[col].dtype.kind not in dtype:
            print(f"Warning: Column '{col}' has type {df[col].dtype} but expected {dtype}.")
            all_correct = False
    
    if all_correct:
        print("All key numeric columns have the expected data types.")
    print("------------------------------\n")

def check_value_ranges(df):
    """Performs sanity checks on the ranges of specific columns."""
    print("--- 3. Checking Value Ranges ---")
    range_checks = {
        'age': (0, 120),
        'MMSE': (0, 30),
        'years_of_education': (0, 40),
        'APOE4_alleles': (0, 2)
    }

    all_in_range = True
    for col, (min_val, max_val) in range_checks.items():
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            if not df[col].dropna().between(min_val, max_val).all():
                print(f"Warning: Column '{col}' has values outside the expected range [{min_val}, {max_val}].")
                all_in_range = False

    if all_in_range:
        print("All key columns have values within their expected ranges.")
    print("------------------------------\n")

def check_data_privacy(df):
    """Performs a simple check for columns that might contain PII."""
    print("--- 4. Checking for Potential PII ---")
    # A simple heuristic: check for columns with identifying names
    pii_keywords = ['name', 'address', 'phone', 'email', 'patient_name']
    potential_pii_cols = []
    for col in df.columns:
        for keyword in pii_keywords:
            if keyword in col.lower():
                potential_pii_cols.append(col)
                break
    
    if potential_pii_cols:
        print(f"Warning: Found columns that may contain PII: {potential_pii_cols}")
    else:
        print("No columns with obvious PII keywords found.")
    print("-------------------------------------\
")

def run_qc_checks(file_path):
    """
    Main function to execute all QC steps on the given data file.

    Args:
        file_path (str): The absolute path to the Parquet file to check.
    """
    print(f"Running Data Quality Control checks on: {file_path}\n")
    try:
        df = pd.read_parquet(file_path)
    except FileNotFoundError:
        print(f"Error: The file was not found at {file_path}")
        print("Please run the `unify_multiomics_data.py` script first.")
        return

    check_missing_values(df)
    check_data_types(df)
    check_value_ranges(df)
    check_data_privacy(df)
    print("Data Quality Control checks complete.")

if __name__ == "__main__":
    run_qc_checks(INPUT_PATH)
