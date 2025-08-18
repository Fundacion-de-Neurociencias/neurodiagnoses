import sys
from pathlib import Path
import pprint
sys.path.append(str(Path(__file__).parent.parent.absolute()))
from tools.bayesian_engine.core import BayesianEngine
def run_test():
    print("--- [INICIO] Prueba del Motor Nativo BayesianEngine ---")
    engine = BayesianEngine(
        axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
        axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
        axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv")
    )
    print("--- [FIN] Prueba completada: El motor nativo se instancia sin errores. ---")
if __name__ == "__main__":
    run_test()
