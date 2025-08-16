# unified_orchestrator.py
# Main entry point for generating a tridimensional diagnosis.
# (Refactored to integrate the new Glass-Box Bayesian Engine)

import os
import sys
import json
from pathlib import Path

# Ensure local modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- [MODIFICACIÓN 1]: Imports Antiguos (Comentados/Eliminados) ---
# from tools.tridimensional_annotation.annotator import generate_tridimensional_annotation
# from tools.ml_pipelines.pipelines_axis3_severity_mapping import Axis3SeverityMapperPipeline
# from tools.prob_diag.run_prob_dx import BayesianAxis2Pipeline

# --- [MODIFICACIÓN 2]: Imports Nuevos ---
from tools.bayesian_engine.core import BayesianEngine

def run_full_pipeline(patient_id: str, patient_data: dict) -> dict:
    """
    Runs the full diagnostic pipeline for a single patient and returns the results.
    Integrates the new Bayesian Engine and its explainability trail.
    """
    print(f"--- Running Full Pipeline for Subject ID: {patient_id} ---")
    bayesian_engine = BayesianEngine(
        axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
        axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv")
    )
    patient_genetics = patient_data.get("axis1_features", {})
    patient_molecular = patient_data.get("axis2_features", {})
    patient_phenotype = patient_data.get("axis3_features", {})
    # Transform patient data into lists of evidence strings for the engine
    # This logic will become more sophisticated in the future
    axis1_evidence_list = [v for k, v in patient_genetics.items() if k == "main_snp"]
    axis2_evidence_list = [k for k, v in patient_molecular.items() if v == "positive"]

    print("\n--- Running Axis 1 & 2: Glass-Box Bayesian Inference ---")
    mean_prob, ci, evidence_trail = bayesian_engine.run_full_inference(
        axis1_evidence=axis1_evidence_list,
        axis2_evidence=axis2_evidence_list,
        disease="Alzheimer's Disease",
        initial_prior=0.20
    )
    axis2_results = {
        "disease": "Alzheimer's Disease",
        "posterior_probability": f"{mean_prob:.2%}",
        "credibility_interval_95": f"[{ci[0]:.2%} - {ci[1]:.2%}]"
    }
    print("--- Axis 1 & 2 Inference Complete ---")
    axis3_results = {"status": "pending_integration", "details": patient_phenotype}
    final_annotation_string = f"Bayesian analysis for AD returned a probability of {axis2_results['posterior_probability']} with a 95% CI of {axis2_results['credibility_interval_95']}."
    output = {
        "patient_id": patient_id,
        "final_report_string": final_annotation_string,
        "axis1_results": patient_genetics,
        "axis2_results": axis2_results,
        "axis3_results": axis3_results,
        "evidence_trail": evidence_trail
    }
    return output

def main():
    """
    Main execution function for direct script execution (demonstration purposes).
    """
    print("--- Unified Orchestrator (Bayesian Engine Integrated) ---")
    
    # Usaremos un diccionario de paciente simplificado para esta prueba
    patient_data = {
        "patient_id": "ND_EXPLAIN_001",
        "axis1_features": {"main_snp": "rs6695033"},
        "axis2_features": {"p-tau181": "positive"},
        "axis3_features": {"hippocampal_volume": "low"}
    }
    
    patient_id = patient_data.get("patient_id")

    # Run the main pipeline logic
    final_output = run_full_pipeline(patient_id, patient_data)
    
    # Print the final formatted report string
    print("\n\n================ NEURODIAGNOSES FINAL REPORT ================")
    print(f"Subject ID: {final_output['patient_id']}")
    print("\n--- Tridimensional Diagnostic Annotation ---")
    print(f"  {final_output['final_report_string']}")
    print("\n--- Structured Output ---")
    print(json.dumps(final_output, indent=2))
    print("============================================================")


if __name__ == '__main__':
    main()
