# unified_orchestrator.py
# This script is the main entry point for generating a tridimensional diagnosis.
# (Refactored to integrate the Bayesian Axis 2 Pipeline)

import os
import sys
import json

# Add project root to path for cross-module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.tridimensional_annotation.annotator import generate_tridimensional_annotation
# The old XGBoost pipeline is kept for reference but can be removed later.
# from tools.ml_pipelines.pipelines_axis2_molecular import Axis2MolecularPipeline
from tools.ml_pipelines.pipelines_axis3_severity_mapping import Axis3SeverityMapperPipeline
# Import the new, clean, class-based Bayesian engine
from tools.prob_diag.run_prob_dx import BayesianAxis2Pipeline

def main():
    """
    Main execution function. Ensures models are ready and then runs the
    tridimensional annotation for a sample patient, using the Bayesian
    engine for Axis 2.
    """
    # --- 1. Pre-flight Checks & Pipeline Initialization ---
    print("--- Initializing Diagnostic Pipelines ---")
    
    # Instantiate the new Bayesian Pipeline for Axis 2
    bayesian_axis2_pipeline = BayesianAxis2Pipeline()
    
    # The Axis 3 pipeline remains as before
    axis3_pipeline = Axis3SeverityMapperPipeline()
    if not os.path.exists(axis3_pipeline.model_path):
        print("Training Axis 3 model as it was not found...")
        axis3_pipeline.train()

    # The check for the old Axis 2 model is now disabled
    # if not os.path.exists('models/axis2_molecular_model.joblib'):
    #   Axis2MolecularPipeline().train_and_evaluate()
        
    print("-- All pipelines are ready. --")

    # --- 2. Load Sample Patient Data ---
    # This data will be the input for our pipelines
    patient_data_path = 'data/sample_patient.json'
    print(f"\nLoading sample patient data from '{patient_data_path}'...")
    with open(patient_data_path, 'r') as f:
        patient_data = json.load(f)

    # --- 3. Run Pipelines to Generate Diagnostic Components ---
    
    # Run Bayesian Engine for Axis 2 Probabilistic Diagnosis
    print("\n-- Running Bayesian Engine (Axis 2) --")
    # The patient_evidence should contain pre-calculated boolean flags for each evidence
    # Example: {'pTau181_Abeta42_positive': True}
    # This logic will need to be expanded in a future step.
    # For now, we simulate a simple evidence dictionary.
    patient_evidence_for_bayes = {
        "pTau181_Abeta42_positive": True 
    }
    bayesian_posteriors = bayesian_axis2_pipeline.predict(patient_evidence_for_bayes)

    # The main tridimensional annotation still runs, but its Axis 2 component
    # should be considered legacy.
    # TODO: Integrate the bayesian_posteriors directly into the final annotation object.
    annotation = generate_tridimensional_annotation(patient_id="ND_DEMO_001")
    
    # --- 4. Print the Final Consolidated Report ---
    print("\n\n================ NEURODIAGNOSES FINAL REPORT ================")
    print(f"Subject ID: ND_DEMO_001")
    
    print("\n--- Probabilistic Diagnostic Annotation (Axis 2 - Bayesian Engine) ---")
    if bayesian_posteriors:
        ranked_bayesian_posteriors = sorted(bayesian_posteriors.items(), key=lambda item: item[1], reverse=True)
        for label, probability in ranked_bayesian_posteriors:
            print(f"  - {label}: {probability:.4f}")
    else:
        print("  - Bayesian analysis could not be completed.")

    print("\n--- Legacy Tridimensional Annotation ---")
    print(f"  {annotation}")
    
    print("\n============================================================")

if __name__ == '__main__':
    main()