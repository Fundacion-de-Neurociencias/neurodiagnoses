# --- Unified Neurodiagnoses Orchestrator ---
import os
import sys
import pandas as pd
import random

# Add project root for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.ml_pipelines.pipelines_axis2_molecular import Axis2MolecularPipeline
from tools.ml_pipelines.pipelines_axis3_pathology import Axis3PathologyPipeline
from models.meta_classifier.final_diagnostic_model import MetaClassifier

def run_full_diagnosis(patient_id):
    """Orchestrates the full 3-axis diagnosis and uses the MetaClassifier for the final report."""
    print(f"--- Starting Full 3-Axis Diagnosis for Patient: {patient_id} ---")

    # --- AXES PREDICTION ---
    print("\n[INFO] Running all individual axis pipelines...")
    # For this PoC, we'll continue to use placeholder/simulated outputs.
    axis1_result = "Predicted Genotype: C9orf72 (Placeholder)"
    axis2_result = Axis2MolecularPipeline().predict(pd.DataFrame([{'patient_id': patient_id}])) # Pass a dummy DataFrame
    axis3_result = Axis3PathologyPipeline().predict(patient_id)
    print("  > All axis predictions complete.")

    # --- META-CLASSIFICATION ---
    print("\n[INFO] Generating final report with Meta-Classifier...")
    meta_classifier = MetaClassifier(axis1_result, axis2_result, axis3_result)
    final_probabilities = meta_classifier.get_final_probabilities()
    tridimensional_summary = meta_classifier.get_tridimensional_summary()
    print("  > Final diagnosis generated.")

    # --- DISPLAY FINAL UNIFIED REPORT ---
    print("\n\n================ NEURODIAGNOSES FINAL REPORT ================")
    print(f"  Patient ID: {patient_id}")
    print("\n--- 1. Tridimensional Summary ---")
    print(f"  {tridimensional_summary}")
    
    print("\n--- 2. Final Probabilistic Diagnosis ---")
    for disease, probability in sorted(final_probabilities.items(), key=lambda item: item[1], reverse=True):
        print(f"  - {disease:<25}: {probability:.2%}")

    print("============================================================")

if __name__ == '__main__':
    sample_patient_id = 4101131
    
    print("--- Pre-flight check: Ensuring Axis 2 model is trained ---")
    axis2_pipeline = Axis2MolecularPipeline()
    if not os.path.exists(axis2_pipeline.model_path):
      axis2_pipeline.train_and_evaluate()
    
    run_full_diagnosis(patient_id=sample_patient_id)