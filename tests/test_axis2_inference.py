import sys
from pathlib import Path
import pprint
sys.path.append(str(Path(__file__).parent.parent.absolute()))
from tools.bayesian_engine.core import BayesianEngine

def run_test():
    print("\nn--- [INICIO] Prueba de Inferencia del Eje 2 ---")
    engine = BayesianEngine(kb_dir=Path("data/knowledge_base"))
        
    patient_case_1 = {
        "id": "Case Study 1 Patient",
        "axis1": ["ApoE4_c.388T>C", "hypertension"],
        "axis2": ["amyloid_beta_positive", "tau_pathology_positive", "NfL_high", "GFAP_elevated", "vascular_dysfunction_markers_positive"]
    }

    print(f"\nn--- Analizando: {patient_case_1['id']} ---")
    
    final_signature = engine.run_full_tridimensional_analysis(patient_case_1)
    
    print("\nn--- [RESULTADO] Blueprint Parcial (Eje 1 y 2): ---")
    pprint.pprint(final_signature)
    
    # Verificación
    axis2_result = final_signature['tridimensional_annotation']['axis_2_molecular_markers']
    assert len(axis2_result['primary_proteinopathies']) == 2
    assert any(marker['name'] == 'NfL' and marker['status'] == 'High neurodegenerative activity' for marker in axis2_result['secondary_biomarkers'])
    print("\nn--- [VERIFICACIÓN OK] ---")
    print("--- [FIN] Prueba del Eje 2 completada con éxito. ---")

if __name__ == "__main__":
    run_test()
