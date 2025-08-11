# --- Unified Neurodiagnoses Orchestrator ---
import os
import sys
import json
import pandas as pd
import random
from dataclasses import asdict

# --- DEFINITIVE FIX FOR ModuleNotFoundError ---
# Add the project's root directory to Python's path.
# This ensures that Python can find the 'tools' module.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# ----------------------------------------------

# Now, the imports will work.
from tools.phenotype_to_genotype.model import PhenotypeEmbedder
from tools.ml_pipelines.pipelines_axis2_molecular import Axis2MolecularPipeline
from tools.ml_pipelines.pipelines_axis3_pathology import Axis3PathologyPipeline
from tools.data_ingestion.parsers.vascular_parser import parse_vascular_data

def run_full_diagnosis(patient_id):
    """Orchestrates the full 3-axis diagnosis for a given patient ID."""
    print(f"--- Starting Full 3-Axis Diagnosis for Patient: {patient_id} ---")

    print("\n[INFO] Running Axis 1 (Phenotype-to-Genotype) Prediction...")
    axis1_result = "Predicted Genotype: C9orf72 (Placeholder - Model Not Trained)"
    print(f"  > Axis 1 Result: {axis1_result}")

    print("\n[INFO] Running Axis 2 (Molecular Profile) Prediction...")
    axis2_pipeline = Axis2MolecularPipeline()
    axis2_result = axis2_pipeline.predict(patient_id)
    print(f"  > Axis 2 Result: {axis2_result}")

    print("\n[INFO] Running Axis 3 (Neuropathology & Vascular) Prediction...")
    axis3_pathology_pipeline = Axis3PathologyPipeline()
    axis3_pathology_result = axis3_pathology_pipeline.predict(patient_id)
    axis3_vascular_result = parse_vascular_data(patient_id)
    print(f"  > Axis 3 Pathology Result: {axis3_pathology_result}")
    print(f"  > Axis 3 Vascular Result: {axis3_vascular_result}")

    print("\n\n================ NEURODIAGNOSES FINAL REPORT ================")
    print(f"Patient ID: {patient_id}")
    print("---------------------------------------------------------")
    print(f"AXIS 1 (Etiology):     {axis1_result}")
    print(f"AXIS 2 (Molecular):    {axis2_result}")
    print(f"AXIS 3 (Phenotype):    {axis3_pathology_result}")
    if axis3_vascular_result:
        vascular_details = ', '.join([f"{k}: {v}" for k, v in axis3_vascular_result['vascular_profile'].items()])
        print(f"                       Vascular Profile -> {vascular_details}")
    print("============================================================")

if __name__ == '__main__':
    sample_patient_id = 0
    
    print("--- Pre-flight check: Ensuring Axis 2 model is trained ---")
    axis2_pipeline = Axis2MolecularPipeline()
    if not os.path.exists(axis2_pipeline.model_path):
      axis2_pipeline.train()
    
    run_full_diagnosis(patient_id=sample_patient_id)
