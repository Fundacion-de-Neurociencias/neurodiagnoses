# unified_orchestrator.py
# (Refactored to be the central logic hub)

import os
import sys
import json
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.tridimensional_annotation.annotator import generate_tridimensional_annotation
from tools.ml_pipelines.pipelines_axis3_severity_mapping import Axis3SeverityMapperPipeline
from tools.prob_diag.run_prob_dx import BayesianAxis2Pipeline

def main():
    """
    Main execution function. Runs all pipelines and passes results
    to the annotator to generate the final report.
    """
    print("--- Initializing Diagnostic Pipelines ---")
    bayesian_axis2_pipeline = BayesianAxis2Pipeline()
    axis3_pipeline = Axis3SeverityMapperPipeline()
    
    # Pre-flight check for Axis 3 model
    if not os.path.exists(axis3_pipeline.model_path):
        print("Training Axis 3 model as it was not found...")
        axis3_pipeline.train()
    print("-- All pipelines are ready. --")

    # --- 1. Define Sample Patient Data ---
    # This data would normally come from the ingestion pipeline
    patient_id = "ND_DEMO_001"
    patient_genetics = {"APOE_e4": 1}
    patient_imaging_data = {
        'lh_entorhinal_volume': 1980.0, 'rh_entorhinal_volume': 2010.0,
        'lh_hippocampus_volume': 3050.0, 'rh_hippocampus_volume': 3100.0,
        'lh_precuneus_thickness': 1.85, 'rh_precuneus_thickness': 1.9
    }
    # For the Bayesian engine, we need to provide the pre-classified evidence
    patient_evidence_for_bayes = {
        "pTau181_Abeta42_positive": True # Simulate that the patient is positive for this AD marker
    }

    # --- 2. Run All Pipelines ---
    print("\n--- Running All Pipelines for Subject ID: {} ---".format(patient_id))
    
    # Axis 2
    axis2_results = bayesian_axis2_pipeline.predict(patient_evidence_for_bayes)
    
    # Axis 3
    axis3_results = axis3_pipeline.predict_and_explain(patient_imaging_data)

    # --- 3. Generate Final Annotation by passing results to the formatter ---
    final_report = generate_tridimensional_annotation(
        patient_id=patient_id,
        axis1_genetics=patient_genetics,
        axis2_molecular_profile=axis2_results,
        axis3_severity_map=axis3_results
    )

    # --- 4. Print the Final Report ---
    print("\n\n================ NEURODIAGNOSES FINAL REPORT ================")
    print(f"Subject ID: {patient_id}")
    print("\n--- Tridimensional Diagnostic Annotation ---")
    print(f"  {final_report}")
    print("\n============================================================")

if __name__ == '__main__':
    main()
