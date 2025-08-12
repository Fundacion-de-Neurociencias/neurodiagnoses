# --- Unified Neurodiagnoses Orchestrator (Final Version) ---
import os
import sys
import pandas as pd
import random
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.probabilistic_annotation.axis_1_classifier import predict_etiology_from_analysis
from tools.ml_pipelines.pipelines_axis2_molecular import Axis2MolecularPipeline
from tools.ml_pipelines.pipelines_axis3_severity_mapping import Axis3SeverityMapperPipeline

def run_full_diagnosis(patient_id):
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
    axis2_result = Axis2MolecularPipeline().predict(pd.DataFrame([{'patient_id': patient_id}]))
    axis3_result = Axis3SeverityMapperPipeline().predict_and_explain({'lh_entorhinal_volume': 2000}) # Simplified input
    print(f"  > Axis 2 & 3 Predictions Complete.")

    print("\n\n================ NEURODIAGNOSES FINAL REPORT ================")
    print(f"Patient ID: {patient_id}")
    print("---------------------------------------------------------")
    print(f"AXIS 1 (Etiology):     Top genetic finding -> {max(axis1_result, key=axis1_result.get)}")
    print(f"AXIS 2 (Molecular):    Top Diagnosis -> {max(axis2_result, key=axis2_result.get)}")
    print(f"AXIS 3 (Phenotype):    Predicted Severity Score -> {axis3_result['predicted_severity_score']:.2f}")
    print("============================================================")

if __name__ == '__main__':
    run_full_diagnosis(patient_id=1001)