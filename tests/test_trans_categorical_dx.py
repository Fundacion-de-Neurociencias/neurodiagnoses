import sys
from pathlib import Path
import unittest
import pandas as pd

# Add the engine's root directory to the Python path to allow for module imports
engine_path = Path(__file__).parent.parent / "neurodiagnoses-engine"
sys.path.insert(0, str(engine_path.absolute()))

from tools.bayesian_engine.core import BayesianEngine

class TestTransCategoricalDiagnosis(unittest.TestCase):
    def setUp(self):
        self.engine = BayesianEngine(base_dir=Path("neurodiagnoses-engine"))
        self.cohort = pd.read_csv("neurodiagnoses-engine/data/simulated/sample_cohort_complex.csv")

    def test_imitator_detection_and_alert(self):
        print("n--- Probando la detección de un 'imitador' autoinmune ---")
        
        # Seleccionamos al paciente con evidencia de Encefalitis Límbica
        patient_row = self.cohort[self.cohort['SubjectID'] == 'Patient_IMITATOR'].iloc[0]
        
        patient_evidence = {
            'axis2': [col for col, val in patient_row.items() if val == 1 and "LGI1" in col],
            'axis3': [col for col, val in patient_row.items() if val == 1 and "facinbrachial" in col]
        }
        
        result = self.engine.infer_classical_differential(patient_evidence)
        
        # Verificación 1: El diagnóstico principal es el correcto
        top_diagnosis = result['hypotheses'][0]['diagnosis']
        self.assertEqual(top_diagnosis, 'Limbic Encephalitis')
        
        # Verificación 2: La alerta accionable se ha activado
        self.assertIsNotNone(result['actionable_alert'])
        self.assertEqual(result['actionable_alert']['category'], 'Autoimmune')
        
        print("SUCCESS: El motor ha identificado correctamente la enfermedad imitadora y ha generado una alerta.")
        import pprint
        pprint.pprint(result)

if __name__ == '__main__':
    unittest.main()
