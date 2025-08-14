# -*- coding: utf-8 -*-
"""
Batch Annotation Runner (Functional Version)

This script processes a list of patient IDs from a given dataset,
runs the full Neurodiagnoses pipeline for each, and saves the structured
JSON output required for the EvoLearns clinical validation dashboard.
"""

import os
import sys
import json
import pandas as pd
from tqdm import tqdm

# Ensure the project root is in the path to find our modules
# This needs to point to the root from the 'workflows' directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our newly refactored, importable pipeline function
from unified_orchestrator import run_full_pipeline

def load_full_patient_data(patient_id, full_dataset_path):
    """
    This is a helper function to simulate loading a single patient's complete
    data from a larger file, which is needed by the pipeline.
    In a real scenario, this would query a database or a master file.
    For now, it loads a generic sample file for demonstration.
    """
    # TODO: Replace this with logic to load real data for a specific patient
    # from the Cornblath dataset parquet file.
    sample_data_path = 'data/sample_patient_full.json'
    with open(sample_data_path, 'r') as f:
        data = json.load(f)
    data['patient_id'] = patient_id # Overwrite with the current patient_id
    return data

def process_batch(patient_list_csv, full_dataset_path, output_dir):
    """
    Processes a CSV of patient IDs, runs the pipeline for each, and saves the output.
    """
    os.makedirs(output_dir, exist_ok=True)
    try:
        patient_df = pd.read_csv(patient_list_csv)
    except FileNotFoundError:
        print(f"ERROR: Patient list file not found at {patient_list_csv}")
        return
    
    print(f"Starting batch processing for {len(patient_df)} patients...")
    
    for patient_id in tqdm(patient_df['patient_id']):
        # Load the full data for the current patient
        patient_data = load_full_patient_data(patient_id, full_dataset_path)

        # Run the actual pipeline from the orchestrator for this patient
        structured_output = run_full_pipeline(patient_id, patient_data)
        
        output_filename = os.path.join(output_dir, f"{patient_id}_annotation.json")
        with open(output_filename, 'w') as f:
            json.dump(structured_output, f, indent=2)
            
    print(f"nBatch processing complete. {len(patient_df)} JSON files generated in '{output_dir}'.")

if __name__ == "__main__":
    # Define the source of patient IDs and the output directory
    patient_list_file = "data/cornblath_patient_ids.csv"
    output_directory = "data/outputs_for_evolearns"
    full_dataset_file = "data/processed/unified_patient_data.parquet" # Placeholder for now

    # Create a dummy patient list if it doesn't exist, for testing.
    if not os.path.exists(patient_list_file):
        print(f"Creating dummy patient list at '{patient_list_file}' for demonstration.")
        pd.DataFrame({
            'patient_id': [f"CORNBLATH_{i:03d}" for i in range(1, 51)]
        }).to_csv(patient_list_file, index=False)
    
    process_batch(patient_list_file, full_dataset_file, output_directory)

