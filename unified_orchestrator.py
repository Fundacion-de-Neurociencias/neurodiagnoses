# --- Unified Neurodiagnoses Orchestrator (Final Version) ---
import os
import sys
import pandas as pd
import random
import subprocess
import json # Added for API output formatting

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.probabilistic_annotation.axis_1_classifier import predict_etiology_from_analysis
from tools.ml_pipelines.pipelines_axis2_molecular import Axis2MolecularPipeline
from tools.ml_pipelines.pipelines_axis3_severity_mapping import Axis3SeverityMapperPipeline

def _run_full_diagnosis_internal(patient_id):
    """Orchestrates the full 3-axis diagnosis using all final, integrated components."""
    print(f"--- Starting Full 3-Axis Diagnosis for Patient: {patient_id} ---")

    # --- FULL GENOMICS PIPELINE ---
    print("\n[INFO] Running Full Genomics Pipeline (Build Panel -> Impute -> Analyze)...")
    subprocess.run(["python", "workflows/genomic_pipeline/1_build_panel.py"], check=True)
    subprocess.run(["python", "workflows/genomic_pipeline/2_impute_genotypes.py"], check=True)
    subprocess.run(["python", "workflows/genomic_pipeline/3_analyze_variants.py"], check=True)
    
    # --- AXIS 1: ETIOLOGY PREDICTION (using pipeline output) ---
    print("\n[INFO] Running Upgraded Axis 1 (Etiology) Prediction...")
    axis1_result = predict_etiology_from_analysis('data/processed/significant_genetic_variants.json')
    print(f"  > Axis 1 Result: {axis1_result}")

    # --- AXIS 2 & 3 PREDICTIONS (Simulated for this run) ---
    print("\n[INFO] Running Axis 2 & 3 Predictions...")
    # Simulate patient molecular data for Axis 2
    patient_molecular_data = pd.DataFrame([pd.np.random.rand(7)], columns=['GDA', 'PDE6D', 'FN1', 'SEMA4B', 'TNFSF8', 'YWHAG', 'NPTX2'])
    axis2_result = Axis2MolecularPipeline().predict(patient_molecular_data)

    # Simulate patient imaging data for Axis 3
    patient_imaging_data = {
        'lh_entorhinal_volume': 1980.0, 'rh_entorhinal_volume': 2010.0,
        'lh_hippocampus_volume': 3050.0, 'rh_hippocampus_volume': 3100.0,
        'lh_precuneus_thickness': 1.85, 'rh_precuneus_thickness': 1.9
    }
    axis3_result = Axis3SeverityMapperPipeline().predict_and_explain(patient_imaging_data)
    print(f"  > Axis 2 & 3 Predictions Complete.")

    # --- FINAL REPORT ---
    print("\n\n================ NEURODIAGNOSES FINAL REPORT ================")
    print(f"Patient ID: {patient_id}")
    print("---------------------------------------------------------\n") # Added newline for spacing

    # Format Axis 1 result
    top_genetic_finding = max(axis1_result, key=axis1_result.get)
    axis1_formatted = f"AXIS 1 (Etiology):     Top genetic finding -> {top_genetic_finding}"

    # Format Axis 2 result
    top_molecular_dx = max(axis2_result, key=axis2_result.get)
    axis2_formatted = f"AXIS 2 (Molecular):    Top Diagnosis -> {top_molecular_dx} ({axis2_result[top_molecular_dx]:.1%})"

    # Format new, rich Axis 3 result
    predicted_score = axis3_result['predicted_severity_score']
    explanation = axis3_result['key_contributing_regions']
    explanation_str = ', '.join([f"{k.replace('_volume','').replace('_thickness','')}: {v:.2f}" for k, v in explanation.items()])
    axis3_formatted = f"AXIS 3 (Phenotype):    Predicted Severity Score -> {predicted_score:.2f}\n                       Key Regions -> {explanation_str}"

    full_text_report = f"{axis1_formatted}\n{axis2_formatted}\n{axis3_formatted}"

    print(full_text_report)
    print("============================================================\n") # Added newline for spacing

    return {
        "patient_id": patient_id,
        "tridimensional_summary": full_text_report,
        "final_probabilistic_diagnosis": list(axis1_result.items()), # Example: convert dict to list of tuples
        "axis1_details": axis1_result,
        "axis2_details": axis2_result,
        "axis3_details": axis3_result
    }

def run_full_diagnosis_for_api(patient_id):
    """
    Wrapper function for API calls to run the full diagnosis.
    Returns a structured dictionary.
    """
    return _run_full_diagnosis_internal(patient_id)


if __name__ == '__main__':
    sample_patient_id = 1001
    
    print("--- Pre-flight check: Ensuring all models are trained ---")
    # Note: These checks are simplified. In a real system, model training
    # would be part of a separate MLOps pipeline.
    if not os.path.exists('models/axis2_molecular_model.joblib'):
      Axis2MolecularPipeline().train_and_evaluate()
    if not os.path.exists('models/axis3_severity_model.joblib'):
      Axis3SeverityMapperPipeline().train()
    
    # Run the diagnosis and print the structured output
    result = _run_full_diagnosis_internal(patient_id=sample_patient_id)
    print("\n--- Structured API Output Example ---")
    print(json.dumps(result, indent=2))
