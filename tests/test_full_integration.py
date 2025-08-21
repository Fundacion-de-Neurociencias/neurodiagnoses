import sys
from pathlib import Path
import unittest
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.absolute() / "neurodiagnoses-engine" / "tools"))
from bayesian_engine.core import BayesianEngine

class TestFullIntegration(unittest.TestCase):
    def test_unified_engine_output(self):
        print("n--- Probando la salida del motor unificado (Diagnóstico + Riesgo) ---")
        
        # El motor ahora se inicializa con la ruta base del repositorio 'engine'
        engine = BayesianEngine(base_dir=Path("neurodiagnoses-engine"))

        # Paciente con datos para ambos motores
        patient_profile = {
            "id": "Patient_Integrated_001",
            "axis1": ["ApoE4_c.388T>C"],
            "APOE_e4": 1, # Dato para el motor de riesgo
            "phs_score_no_apoe": 0.9 # Dato para el motor de riesgo
        }
        
        full_report = engine.run_full_tridimensional_analysis(patient_profile)

        # Verificar que ambas secciones principales existen
        self.assertIn("tridimensional_annotation", full_report)
        self.assertIn("risk_assessment", full_report)
        
        # Verificar que la sección de riesgo no dio error y tiene contenido
        self.assertNotIn("error", full_report["risk_assessment"])
        self.assertIn("relative_hazard_ratio", full_report["risk_assessment"])

        print("SUCCESS: El motor unificado ha generado un informe completo.")
        import pprint
        pprint.pprint(full_report)

if __name__ == '__main__':
    unittest.main()
