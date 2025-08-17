import os, sys, json
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print("unified_orchestrator.py sys.path:", sys.path)
from tools.bayesian_engine.core import BayesianEngine

_bayesian_engine_instance = None
def get_engine():
    global _bayesian_engine_instance
    if _bayesian_engine_instance is None:
        _bayesian_engine_instance = BayesianEngine(
            axis1_kb_path=Path('data/knowledge_base/axis1_likelihoods.csv'),
            axis2_kb_path=Path('data/knowledge_base/axis2_likelihoods.csv'),
            axis3_kb_path=Path('data/knowledge_base/axis3_likelihoods.csv')
        )
    return _bayesian_engine_instance

def run_full_pipeline(patient_id: str, patient_data: dict, initial_prior: float = 0.20) -> dict:
    bayesian_engine = get_engine()
    # Mapeamos los datos de entrada de la UI a los que espera el motor
    engine_patient_data = {
        'axis1': [v for k, v in patient_data.get("axis1_features", {}).items()],
        'axis2': [k for k, v in patient_data.get("axis2_features", {}).items() if v == "positive"],
        'axis3_phenotype': [k for k,v in patient_data.get("axis3_features", {}).items() if isinstance(v, str) and v == "positive"],
        'axis3_imaging': {k:v for k,v in patient_data.get("axis3_features", {}).items() if isinstance(v, (int, float))}
    }
    
    mean_prob, ci, evidence_trail = bayesian_engine.run_full_tridimensional_inference(
        patient_data=engine_patient_data,
        disease="Alzheimer's Disease",
        initial_prior=initial_prior
    )
    
    bayesian_results = {"disease": "Alzheimer's Disease", "posterior_probability": f"{mean_prob:.2%}", "credibility_interval_95": f"[{ci[0]:.2%} - {ci[1]:.2%}]"}
    final_annotation_string = f"Bayesian analysis for AD returned a probability of {bayesian_results['posterior_probability']} with a 95% CI of {bayesian_results['credibility_interval_95']}."
    
    return {
        "patient_id": patient_id, "final_report_string": final_annotation_string,
        "bayesian_results": bayesian_results, "evidence_trail": evidence_trail
    }