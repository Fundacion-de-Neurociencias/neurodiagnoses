# unified_orchestrator.py
# This script is the main entry point for generating a tridimensional diagnosis.

import os
# Add project root to path for cross-module imports
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.tridimensional_annotation.annotator import generate_tridimensional_annotation
from tools.ml_pipelines.pipelines_axis2_molecular import Axis2MolecularPipeline
from tools.ml_pipelines.pipelines_axis3_severity_mapping import Axis3SeverityMapperPipeline

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
    print("--- All models are ready. ---")

    # 2. Generate the annotation
    annotation = generate_tridimensional_annotation(patient_id="ND_DEMO_001")
    
    # 3. Print the final report
    print("\n\n================ NEURODIAGNOSES FINAL REPORT ================")
    print(f"Subject ID: ND_DEMO_001")
    print("\n--- Tridimensional Diagnostic Annotation ---")
    print(f"  {annotation}")
    print("\n============================================================")

if __name__ == '__main__':
    main()