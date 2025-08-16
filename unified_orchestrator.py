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
    Integrates the new Bayesian Engine for Axis 2.
    """
    print(f"--- Running Full Pipeline for Subject ID: {patient_id} ---")
    
    # --- 1. Initialize Pipelines ---
    # axis3_pipeline = Axis3SeverityMapperPipeline() # Mantenemos esto para el futuro
    
    # --- [MODIFICACIÓN 3]: Inicializar nuestro nuevo motor bayesiano ---
    bayesian_engine = BayesianEngine(kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"))

    # --- 2. Extract data for each pipeline from the input dict ---
    patient_genetics = patient_data.get('axis1_features', {})
    # Para la prueba, definimos la evidencia del paciente directamente.
    patient_evidence_for_bayes = [
        "p-tau181",
        "Gene expression-based blood biomarker panels"
    ]
    patient_imaging_data = patient_data.get('axis3_features', {})

    # --- 3. Run Pipelines to Generate Diagnostic Components ---
    
    # --- [MODIFICACIÓN 4]: Reemplazar la llamada al pipeline antiguo del Eje 2 ---
    print("\n--- Running Axis 2: Glass-Box Bayesian Inference ---")
    mean_prob, ci = bayesian_engine.run_inference_with_uncertainty(
        patient_evidence=patient_evidence_for_bayes,
        disease="Alzheimer's Disease",
        initial_prior=0.20 # Asumimos un prior del 20%
    )
    
    # Formateamos el resultado para que sea compatible con el resto del sistema
    axis2_results = {
        "disease": "Alzheimer's Disease",
        "posterior_probability": f"{mean_prob:.2%}",
        "credibility_interval_95": f"[{ci[0]:.2%} - {ci[1]:.2%}]"
    }
    print("--- Axis 2 Inference Complete ---")
    
    # La lógica del Eje 3 se mantiene para futuras integraciones, pero la desactivamos para esta prueba
    axis3_results = {"status": "pending_integration", "details": patient_imaging_data}

    # La generación de la anotación final también se simplifica para esta prueba
    final_annotation_string = f"Bayesian analysis for AD returned a probability of {axis2_results['posterior_probability']} with a 95% CI of {axis2_results['credibility_interval_95']}."

    # --- 5. Consolidate results into a structured dictionary ---
    output = {
        "patient_id": patient_id,
        "final_report_string": final_annotation_string,
        "axis1_results": patient_genetics,
        "axis2_results": axis2_results,
        "axis3_results": axis3_results
    }
    
    return output

def main():
    """
    Main execution function for direct script execution (demonstration purposes).
    """
    print("--- Unified Orchestrator (Bayesian Engine Integrated) ---")
    
    # Usaremos un diccionario de paciente simplificado para esta prueba
    patient_data = {
        "patient_id": "ND_BAYLOR_001",
        "axis1_features": {"APOE": "e3/e4"},
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
