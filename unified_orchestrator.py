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

def run_full_diagnosis_for_api(patient_id: int) -> dict:
    """
    Orchestrates the diagnosis and returns the report as a dictionary for API use.
    """
    # --- AXES PREDICTION ---
    axis1_result = "Predicted Genotype: C9orf72 (Placeholder)"
    axis2_result = Axis2MolecularPipeline().predict(pd.DataFrame([{'patient_id': patient_id}]))
    axis3_result = Axis3PathologyPipeline().predict(patient_id)

    # --- META-CLASSIFICATION ---
    meta_classifier = MetaClassifier(axis1_result, axis2_result, axis3_result)
    final_probabilities = meta_classifier.get_final_probabilities()
    tridimensional_summary = meta_classifier.get_tridimensional_summary()

    # --- FORMAT REPORT ---
    report = {
        "tridimensional_summary": tridimensional_summary,
        "final_probabilistic_diagnosis": sorted(final_probabilities.items(), key=lambda item: item[1], reverse=True)
    }
    return report

# This part below is for when the script is run directly from the command line
def cli_runner():
    sample_patient_id = 4101131
    
    print("--- Pre-flight check: Ensuring Axis 2 model is trained ---")
    axis2_pipeline = Axis2MolecularPipeline()
    if not os.path.exists(axis2_pipeline.model_path):
      axis2_pipeline.train_and_evaluate()
    
    print(f"--- Starting Full 3-Axis Diagnosis for Patient: {sample_patient_id} ---")
    final_report = run_full_diagnosis_for_api(sample_patient_id)

    print("\n\n================ NEURODIAGNOSES FINAL REPORT ================")
    print(f"  Patient ID: {sample_patient_id}")
    print("\n--- 1. Tridimensional Summary ---")
    print(f"  {final_report['tridimensional_summary']}")
    print("\n--- 2. Final Probabilistic Diagnosis ---")
    for disease, probability in final_report['final_probabilistic_diagnosis']:
        print(f"  - {disease:<25}: {probability:.2%}")
    print("\n============================================================")

if __name__ == '__main__':
    cli_runner()