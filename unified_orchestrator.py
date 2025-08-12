# --- Unified Neurodiagnoses Orchestrator (Final Version) ---
import os
import sys
import pandas as pd
import random
import json

# Add project root for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all final components
from tools.phenotype_to_genotype.model import PhenotypeEmbedder
from tools.ml_pipelines.pipelines_axis2_molecular import Axis2MolecularPipeline
from tools.ml_pipelines.pipelines_axis3_severity_mapping import Axis3SeverityMapperPipeline # <-- NEW, ADVANCED AXIS 3

def run_full_diagnosis(patient_id):
    """
    Orchestrates the full 3-axis diagnosis using all final, integrated components.
    """
    print(f"--- Starting Full 3-Axis Diagnosis for Patient: {patient_id} ---")

    # --- SIMULATE PATIENT DATA ---
    # In a real system, this would come from the data ingestion pipeline.
    patient_molecular_data = pd.DataFrame([pd.np.random.rand(7)], columns=['GDA', 'PDE6D', 'FN1', 'SEMA4B', 'TNFSF8', 'YWHAG', 'NPTX2'])
    patient_imaging_data = {
        'lh_entorhinal_volume': 1980.0, 'rh_entorhinal_volume': 2010.0,
        'lh_hippocampus_volume': 3050.0, 'rh_hippocampus_volume': 3100.0,
        'lh_precuneus_thickness': 1.85, 'rh_precuneus_thickness': 1.9
    }
    
    # --- AXIS 1: ETIOLOGY PREDICTION (Placeholder) ---
    print("\n[INFO] Running Axis 1 (Phenotype-to-Genotype) Prediction...")
    axis1_result = "Predicted Genotype: C9orf72 (Placeholder - Model Not Trained)"
    print(f"  > Axis 1 Result: {axis1_result}")

    # --- AXIS 2: MOLECULAR PREDICTION ---
    print("\n[INFO] Running Axis 2 (Molecular Profile) Prediction...")
    axis2_pipeline = Axis2MolecularPipeline()
    axis2_result = axis2_pipeline.predict(patient_molecular_data)
    print(f"  > Axis 2 Result: {axis2_result}")

    # --- AXIS 3: SEVERITY MAPPING (New Advanced Version) ---
    print("\n[INFO] Running Axis 3 (Neurodegenerative Severity Mapping)...")
    axis3_pipeline = Axis3SeverityMapperPipeline()
    axis3_result = axis3_pipeline.predict_and_explain(patient_imaging_data)
    print(f"  > Axis 3 Result: {axis3_result}")


    # --- FINAL REPORT ---
    print("\n\n================ NEURODIAGNOSES FINAL REPORT ================")
    print(f"Patient ID: {patient_id}")
    print("---------------------------------------------------------")
    print(f"AXIS 1 (Etiology):     {axis1_result}")
    
    # Format Axis 2 result
    top_molecular_dx = max(axis2_result, key=axis2_result.get)
    print(f"AXIS 2 (Molecular):    Top Diagnosis -> {top_molecular_dx} ({axis2_result[top_molecular_dx]:.1%})")

    # Format new, rich Axis 3 result
    predicted_score = axis3_result['predicted_severity_score']
    explanation = axis3_result['key_contributing_regions']
    explanation_str = ', '.join([f"{k.replace('_volume','').replace('_thickness','')} ({v:.2f})" for k, v in explanation.items()])
    
    print(f"AXIS 3 (Phenotype):    Predicted Severity Score -> {predicted_score:.2f}")
    print(f"                       Key Regions -> {explanation_str}")
    print("============================================================")


if __name__ == '__main__':
    sample_patient_id = 4101131
    
    print("--- Pre-flight check: Ensuring all models are trained ---")
    if not os.path.exists('models/axis2_molecular_model.joblib'):
      Axis2MolecularPipeline().train_and_evaluate()
    if not os.path.exists('models/axis3_severity_model.joblib'):
      Axis3SeverityMapperPipeline().train()
    
    run_full_diagnosis(patient_id=sample_patient_id)
