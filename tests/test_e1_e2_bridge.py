import sys
from pathlib import Path
import pprint

# Añadimos el directorio raíz al path para poder encontrar los módulos
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from tools.bayesian_engine.core import BayesianEngine

def run_test():
    """
    Verifica que la evidencia del Eje 1 (Etiología) modifica correctamente
    los priors de las vías patológicas del Eje 2 (Fisiopatología).
    """
    print("--- [INICIO] Prueba del Puente Eje 1 -> Eje 2 ---")
    
    # 1. Instanciar el motor
    engine = BayesianEngine(
        axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
        # Los otros ejes no son necesarios para esta prueba específica
        axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
        axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv")
    )
        
    # 2. Definir pacientes virtuales con diferentes perfiles etiológicos
    patient_1_genetic_ad = {
        "id": "Paciente 1 (Riesgo Genético AD)",
        "evidence": ["APOE_e4"]
    }
    
    patient_2_infectious = {
        "id": "Paciente 2 (Etiología Infecciosa)",
        "evidence": ["HSV1_presence_in_brain"]
    }

    patient_3_mixed_vascular = {
        "id": "Paciente 3 (Etiología Mixta Genética-Vascular)",
        "evidence": ["APOE_e4", "COL4A1_variant"]
    }

    # 3. Ejecutar la inferencia para cada paciente y mostrar resultados
    for patient in [patient_1_genetic_ad, patient_2_infectious, patient_3_mixed_vascular]:
        print(f"\nn" + "="*50)
        print(f"ANALIZANDO: {patient['id']}")
        print(f"Evidencia Eje 1: {patient['evidence']}")
        print("="*50)
        
        axis2_posterior_probs = engine.run_etiology_to_pathology_inference(
            patient_axis1_evidence=patient['evidence']
        )
        
        print("\nn[RESULTADO] Probabilidades a posteriori del Eje 2 (Fisiopatología):")
        pprint.pprint(axis2_posterior_probs)

    print("\nn--- [FIN] Prueba completada. ---")

if __name__ == "__main__":
    run_test()
