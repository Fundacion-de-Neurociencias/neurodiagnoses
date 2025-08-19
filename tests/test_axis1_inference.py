import sys
from pathlib import Path
import pprint
sys.path.append(str(Path(__file__).parent.parent.absolute()))
from tools.bayesian_engine.core import BayesianEngine

def run_test():
    print("\nn--- [INICIO] Prueba de Inferencia del Eje 1 ---")
    engine = BayesianEngine(kb_dir=Path("data/knowledge_base"))
        
    patient_case_1 = {
        "id": "Case Study 1 Patient",
        "axis1": ["ApoE4_c.388T>C", "hypertension", "hypercholesterolemia", "poor_sleep_habits"]
    }

    print(f"\nn--- Analizando: {patient_case_1['id']} ---")
    
    final_signature = engine.run_full_tridimensional_analysis(patient_case_1)
    
    print("\nn--- [RESULTADO] Blueprint Parcial (Solo Eje 1): ---")
    pprint.pprint(final_signature)
    
    # Verificación simple
    assert final_signature['tridimensional_annotation']['axis_1_etiology']['classification'] == 'Sporadic'
    assert "Hypertension" in final_signature['tridimensional_annotation']['axis_1_etiology']['environmental_risk_factors']
    print("\nn--- [VERIFICACIÓN OK] ---")
    print("--- [FIN] Prueba del Eje 1 completada con éxito. ---")

if __name__ == "__main__":
    run_test()
