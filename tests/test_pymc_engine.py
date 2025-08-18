import sys
from pathlib import Path
import pprint

# Añadimos el directorio raíz al path para que pueda encontrar los módulos
# a través de los enlaces simbólicos.
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from tools.bayesian_engine.core_pymc import BayesianEnginePyMC

def run_test():
    """
    Función principal para probar el nuevo motor PyMC de forma aislada.
    """
    print("--- [INICIO] Prueba del Motor BayesianEnginePyMC ---")
    
    # 1. Instanciar el motor
    try:
        engine = BayesianEnginePyMC(
            axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
            axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
            axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv")
        )
    except FileNotFoundError as e:
        print(f"ERROR CRÍTICO: No se encontró una Base de Conocimiento. Verifica que los enlaces simbólicos existen.")
        print(e)
        sys.exit(1)
        
    # 2. Definir un paciente virtual simple
    virtual_patient = {
        "axis1": ["APOE_e4"],
        "axis2": [],
        "axis3_phenotype": [],
        "axis3_imaging": {}
    }
    
    print("\n[CASO DE PRUEBA]")
    pprint.pprint(virtual_patient)
    
    # 3. Definir las hipótesis y el prior
    diseases_to_evaluate = ["Alzheimer's Disease"]
    initial_prior = 0.20 # Un prior base del 20%
    
    print(f"\nHipótesis a evaluar: {diseases_to_evaluate}")
    print(f"Prior inicial: {initial_prior:.0%}")
    
    # 4. Ejecutar la inferencia con PyMC
    results = engine.run_differential_diagnosis_pymc(
        patient_data=virtual_patient,
        diseases_to_evaluate=diseases_to_evaluate,
        initial_prior=initial_prior
    )
    
    # 5. Imprimir los resultados
    print("\n--- [RESULTADOS DE LA INFERENCIA] ---")
    pprint.pprint(results)
    
    print("\n--- [FIN] Prueba completada con éxito. ---")

if __name__ == "__main__":
    run_test()
