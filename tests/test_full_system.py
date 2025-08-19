import sys
from pathlib import Path
import pprint
sys.path.append(str(Path(__file__).parent.parent.absolute()))
from tools.bayesian_engine.core import BayesianEngine

def run_test():
    print("--- [INICIO] Prueba del Sistema Tridimensional Completo ---")
    engine = BayesianEngine(
        axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
        axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
        axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv")
    )
        
    patient_tridimensional = {
        "id": "Paciente Tridimensional (Genética AD + Biomarcadores AD + Clínica AD)",
        "axis1": ["APOE_e4"],
        "axis2": ["CSF_p-tau181_positive", "CSF_Abeta42_negative"],
        "axis3": ["NINCDS-ADRDA_probable_AD"]
    }
    
    diseases_to_evaluate = ["Alzheimer's Disease", "Frontotemporal Dementia"]

    print(f"\nn--- ANALIZANDO: {patient_tridimensional['id']} ---")
    
    final_signature = engine.run_full_tridimensional_analysis(
        patient_data=patient_tridimensional,
        diseases_to_evaluate=diseases_to_evaluate
    )
    
    print("\nn--- [RESULTADO] Firma Neurodegenerativa Completa: ---")
    pprint.pprint(final_signature)
    print("\nn--- [FIN] Prueba del sistema completo, finalizada. ---")

if __name__ == "__main__":
    run_test()
