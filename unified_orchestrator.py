import os, sys, json
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tools.bayesian_engine.core import BayesianEngine

_engine_instance = None
def get_engine():
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = BayesianEngine(
            axis1_kb_path=Path('data/knowledge_base/axis1_likelihoods.csv'),
            axis2_kb_path=Path('data/knowledge_base/axis2_likelihoods.csv'),
            axis3_kb_path=Path('data/knowledge_base/axis3_likelihoods.csv')
        )
    return _engine_instance

def run_full_pipeline(patient_id: str, patient_data: dict, diseases_to_evaluate: list, initial_prior: float) -> dict:
    engine = get_engine()
    results = engine.run_differential_diagnosis(
        patient_data=patient_data,
        diseases_to_evaluate=diseases_to_evaluate,
        initial_prior=initial_prior
    )
    return { "patient_id": patient_id, "differential_diagnosis": results }