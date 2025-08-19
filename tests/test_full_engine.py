import sys
from pathlib import Path
import pprint
from datetime import datetime
sys.path.append(str(Path(__file__).parent.parent.absolute()))
from tools.bayesian_engine.core import BayesianEngine

def run_test():
    print("\nn--- [INICIO] Prueba Final del Motor Tridimensional Completo ---")
    engine = BayesianEngine(kb_dir=Path("data/knowledge_base"))
        
    patient_case_study_1 = {
        "id": "Case_Study_1",
        "axis1": ["ApoE4_c.388T>C", "hypertension", "hypercholesterolemia", "poor_sleep_habits"],
        "axis2": ["amyloid_beta_positive", "tau_pathology_positive", "NfL_high", "GFAP_elevated", "vascular_dysfunction_markers_positive"],
        "axis3": ["visual_memory_deficits", "visuospatial_impairment", "executive_dysfunction"]
    }

    print(f"\nn--- Analizando: {patient_case_study_1['id']} ---")
    
    final_signature = engine.run_full_tridimensional_analysis(
        patient_data=patient_case_study_1,
        timestamp=datetime.now().strftime("%B %Y")
    )
    
    print("\nn--- [RESULTADO] Blueprint v3.0 Completo: ---")
    pprint.pprint(final_signature)
    
    # Verificación
    assert 'classical_differential' in final_signature
    assert 'tridimensional_annotation' in final_signature
    assert 'axis_1_etiology' in final_signature['tridimensional_annotation']
    assert 'axis_2_molecular_markers' in final_signature['tridimensional_annotation']
    assert 'axis_3_neuroanatomoclinical_correlation' in final_signature['tridimensional_annotation']
    assert len(final_signature['tridimensional_annotation']['axis_3_neuroanatomoclinical_correlation']) == 3
    print("\nn--- [VERIFICACIÓN OK] ---")
    print("--- [FIN] Prueba del motor completo, finalizada con éxito. ---")

if __name__ == "__main__":
    run_test()
