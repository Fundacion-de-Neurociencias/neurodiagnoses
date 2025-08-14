# unified_orchestrator.py
# Main entry point for generating a tridimensional diagnosis.
# (Refactored for modular, reusable pipeline execution)

import os
import sys
import json
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.tridimensional_annotation.annotator import generate_tridimensional_annotation
from tools.ml_pipelines.pipelines_axis3_severity_mapping import Axis3SeverityMapperPipeline
from tools.prob_diag.run_prob_dx import BayesianAxis2Pipeline

def run_full_pipeline(patient_id: str, patient_data: dict) -> dict:
    """
    Runs the full diagnostic pipeline for a single patient and returns the results.

    This function is designed to be imported and used by other modules.

    Args:
        patient_id (str): The identifier for the patient.
        patient_data (dict): A dictionary containing patient data structured by axes.
                             e.g., {'axis1_features': {...}, 'axis2_features': {...}}

    Returns:
        dict: A dictionary containing the final report and structured results.
    """
    print(f"--- Running Full Pipeline for Subject ID: {patient_id} ---")
    
    # --- 1. Initialize Pipelines ---
    bayesian_axis2_pipeline = BayesianAxis2Pipeline()
    axis3_pipeline = Axis3SeverityMapperPipeline()
    
    # Pre-flight check for Axis 3 model (can be commented out if models are pre-trained)
    if not os.path.exists(axis3_pipeline.model_path):
        print(f"Training Axis 3 model (model not found at {axis3_pipeline.model_path})...")
        axis3_pipeline.train()

    # --- 2. Extract data for each pipeline from the input dict ---
    patient_genetics = patient_data.get('axis1_features', {})
    patient_evidence_for_bayes = patient_data.get('axis2_features', {})
    patient_imaging_data = patient_data.get('axis3_features', {})

    # --- 3. Run Pipelines to Generate Diagnostic Components ---
    axis2_results = bayesian_axis2_pipeline.predict(patient_evidence_for_bayes)
    axis3_results = axis3_pipeline.predict_and_explain(patient_imaging_data)

    # --- 4. Generate Final Annotation by passing results to the formatter ---
    final_annotation_string = generate_tridimensional_annotation(
        patient_id=patient_id,
        axis1_genetics=patient_genetics,
        axis2_molecular_profile=axis2_results,
        axis3_severity_map=axis3_results
    )

    # --- 5. Consolidate results into a structured dictionary ---
    output = {
        "patient_id": patient_id,
        "final_report_string": final_annotation_string,
        "axis1_results": patient_genetics,
        "axis2_results": axis2_results,
        "axis3_results": axis3_results
    }
    
    return output

def main():
    """
    Main execution function for direct script execution (demonstration purposes).
    """
    print("--- Unified Orchestrator (Demonstration Mode) ---")
    
    # Load a single sample patient for the demo
    patient_data_path = 'data/sample_patient_full.json'
    print(f"nLoading sample patient data from '{patient_data_path}'...")
    with open(patient_data_path, 'r') as f:
        patient_data = json.load(f)
    
    patient_id = patient_data.get("patient_id", "ND_DEMO_001")

    # Run the main pipeline logic
    final_output = run_full_pipeline(patient_id, patient_data)
    
    # Print the final formatted report string
    print("nn================ NEURODIAGNOSES FINAL REPORT ================")
    print(f"Subject ID: {final_output['patient_id']}")
    print("n--- Tridimensional Diagnostic Annotation ---")
    print(f"  {final_output['final_report_string']}")
    print("n============================================================")


if __name__ == '__main__':
    main()
