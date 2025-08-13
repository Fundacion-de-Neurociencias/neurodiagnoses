# unified_orchestrator.py
# This script is the main entry point for generating a tridimensional diagnosis.

import os
# Add project root to path for cross-module imports
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.tridimensional_annotation.annotator import generate_tridimensional_annotation
from tools.ml_pipelines.pipelines_axis2_molecular import Axis2MolecularPipeline
from tools.ml_pipelines.pipelines_axis3_severity_mapping import Axis3SeverityMapperPipeline
from tools.prob_diag.run_prob_dx import load_knowledge_base, calculate_posteriors
import json

def main():
    """
    Main execution function. Ensures models are trained and then runs the
    tridimensional annotation for a sample patient.
    """
    # 1. Pre-flight check to ensure required models are trained
    print("--- Pre-flight check: Ensuring all models are trained ---")
    if not os.path.exists('models/axis2_molecular_model.joblib'):
      Axis2MolecularPipeline().train_and_evaluate()
    if not os.path.exists('models/axis3_severity_model.joblib'):
      Axis3SeverityMapperPipeline().train()
    print("-- All models are ready. --")

    # Load patient data for Bayesian engine
    patient_data_path = 'data/sample_patient.json'
    with open(patient_data_path, 'r') as f:
        patient_data = json.load(f)

    # Run Bayesian Engine
    print("\n-- Running Bayesian Engine (Axis 2) --")
    priors, likelihoods = load_knowledge_base()
    if priors is None:
        print("Error loading knowledge base for Bayesian engine. Skipping Bayesian analysis.")
        bayesian_posteriors = {}
    else:
        bayesian_posteriors = calculate_posteriors(patient_data['axis2_features'], priors, likelihoods)
        ranked_bayesian_posteriors = sorted(bayesian_posteriors.items(), key=lambda item: item[1], reverse=True)
        print("Bayesian Probabilities:")
        for label, probability in ranked_bayesian_posteriors:
            print(f"  - {label}: {probability:.4f}")

    # 2. Generate the annotation
    annotation = generate_tridimensional_annotation(patient_id="ND_DEMO_001")
    
    # 3. Print the final report
    print("\n\n================ NEURODIAGNOSES FINAL REPORT ================")
    print(f"Subject ID: ND_DEMO_001")
    print("\n--- Tridimensional Diagnostic Annotation ---")
    print(f"  {annotation}")
    if bayesian_posteriors:
        print("\n--- Probabilistic Diagnostic Annotation (Bayesian Engine) ---")
        for label, probability in ranked_bayesian_posteriors:
            print(f"  - {label}: {probability:.4f}")

    print("\n============================================================")

if __name__ == '__main__':
    main()
