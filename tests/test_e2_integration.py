import sys
from pathlib import Path
import pprint
sys.path.append(str(Path(__file__).parent.parent.absolute()))
from tools.bayesian_engine.core import BayesianEngine

def run_test():
    print("--- [INICIO] Prueba de Integración del Eje 2 ---")
    engine = BayesianEngine(
        axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
        axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
        axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv")
    )
        
    patient_complex = {
        "id": "Paciente Complejo (Genética AD + Biomarcador Tau)",
        "axis1_evidence": ["APOE_e4"],
        "axis2_evidence": ["CSF_p-tau181_positive"]
    }

    print(f"\nn" + "="*50)
    print(f"ANALIZANDO: {patient_complex['id']}")
    print(f"Evidencia Eje 1: {patient_complex['axis1_evidence']}")
    print(f"Evidencia Eje 2: {patient_complex['axis2_evidence']}")
    print("="*50)
    
    final_molecular_profile = engine.run_full_molecular_analysis(
        patient_axis1_evidence=patient_complex['axis1_evidence'],
        patient_axis2_evidence=patient_complex['axis2_evidence']
    )
    
    print("\nn[RESULTADO] Perfil Fisiopatológico Molecular Final:")
    pprint.pprint(final_molecular_profile)
    print("\nn--- [FIN] Prueba de integración completada. ---")

if __name__ == "__main__":
    run_test()
