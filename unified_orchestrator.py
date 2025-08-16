# unified_orchestrator.py
# Main entry point for generating a tridimensional diagnosis.
# (Final version, fully integrated with the Tridimensional Bayesian Engine)

import os
import sys
import json
from pathlib import Path

# Ensure local modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.bayesian_engine.core import BayesianEngine

# --- Singleton Pattern for Lazy Loading ---
_bayesian_engine_instance = None

def get_engine():
    """Singleton factory to load the Bayesian Engine only once."""
    global _bayesian_engine_instance
    if _bayesian_engine_instance is None:
        print('INFO: Lazily loading Bayesian Engine and all KBs in Orchestrator...')
        _bayesian_engine_instance = BayesianEngine(
            axis1_kb_path=Path('data/knowledge_base/axis1_likelihoods.csv'),
            axis2_kb_path=Path('data/knowledge_base/axis2_likelihoods.csv'),
            axis3_kb_path=Path('data/knowledge_base/axis3_likelihoods.csv')
        )
        print('SUCCESS: Engine loaded and cached for future requests in Orchestrator.')
    return _bayesian_engine_instance


def run_full_pipeline(patient_id: str, patient_data: dict, initial_prior: float = 0.20) -> dict:
    """
    Runs the full diagnostic pipeline for a single patient, integrating the
    tridimensional Bayesian Engine.
    """
    print(f"--- Running Full Pipeline for Subject ID: {patient_id} ---")
    
    bayesian_engine = get_engine() # Ensures lazy loading

    # Extract evidence from the patient_data dictionary
    axis1_evidence = [v for k, v in patient_data.get("axis1_features", {}).items()]
    axis2_evidence = [k for k, v in patient_data.get("axis2_features", {}).items() if v == "positive"]
    # For Axis 3, we expect a dict of biomarker:value pairs
    axis3_evidence = patient_data.get("axis3_features", {})

    print("\nn--- Running Tridimensional Glass-Box Bayesian Inference ---")
    
    # Call the correct, final inference method
    mean_prob, ci, evidence_trail = bayesian_engine.run_full_tridimensional_inference(
        patient_data={'axis1': axis1_evidence, 'axis2': axis2_evidence, 'axis3': axis3_evidence},
        disease="Alzheimer's Disease",
        initial_prior=initial_prior
    )
    
    # Format results
    axis_results = {
        "disease": "Alzheimer's Disease",
        "posterior_probability": f"{mean_prob:.2%}",
        "credibility_interval_95": f"[{ci[0]:.2%} - {ci[1]:.2%}]"
    }
    print("--- Tridimensional Inference Complete ---")

    final_annotation_string = f"Bayesian analysis for AD returned a probability of {axis_results['posterior_probability']} with a 95% CI of {axis_results['credibility_interval_95']}."

    # Consolidate final output dictionary
    output = {
        "patient_id": patient_id,
        "final_report_string": final_annotation_string,
        "axis1_results_input": patient_data.get("axis1_features"),
        "axis2_results_input": patient_data.get("axis2_features"),
        "axis3_results_input": patient_data.get("axis3_features"),
        "bayesian_results": axis_results,
        "evidence_trail": evidence_trail
    }
    
    return output

def main():
    """
    Main execution function for direct script execution (demonstration purposes).
    """
    print("--- Unified Orchestrator (Final Tridimensional Version) ---")
    
    # A complete patient dictionary, mirroring what the UI would send
    full_patient = {
        "patient_id": "ND_TRIDIM_001",
        "axis1_features": {"main_snp": "rs4474465"},
        "axis2_features": {"p-tau181": "positive"},
        "axis3_features": {'HippocampusVolume_mm3': 3100}
    }

    # Run the main pipeline logic
    final_output = run_full_pipeline(full_patient.get("patient_id"), full_patient, initial_prior=0.10)
    
    # Print the structured final report
    print("\n\n================ NEURODIAGNOSES FINAL REPORT ================")
    print(json.dumps(final_output, indent=2))
    print("============================================================")


if __name__ == '__main__':
    main()
