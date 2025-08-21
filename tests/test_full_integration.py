import sys
from pathlib import Path
import unittest
import pandas as pd
from datetime import datetime
import joblib, os, types

# --- Directorio de Herramientas ---
tools_dir = Path(__file__).parent.parent / "neurodiagnoses-engine" / "tools"
sys.path.insert(0, str(tools_dir))

# --- Mock RiskPredictionEngine para el test ---
class MockRiskPredictionEngine:
    def __init__(self, model_path):
        # model_path is now an absolute path string from core.py
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Mock model path not found: {model_path}")
    def predict(self, data):
        return {"risk_score": 0.85, "relative_hazard_ratio": 2.5, "percentile": 95}

# --- Mock del módulo risk_prediction_engine ---
sys.modules['risk_prediction_engine'] = types.ModuleType('risk_prediction_engine')
sys.modules['risk_prediction_engine'].RiskPredictionEngine = MockRiskPredictionEngine

# --- Importar BayesianEngine después de mockear ---
from bayesian_engine.core import BayesianEngine

class TestFullIntegration(unittest.TestCase):
    def setUp(self):
        self.engine_dir = Path("neurodiagnoses-engine")
        self.kb_dir = self.engine_dir / "data/knowledge_base"
        self.model_dir = self.engine_dir / "models/risk_prediction"
        self.kb_dir.mkdir(parents=True, exist_ok=True)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        pd.DataFrame({'evidence_input': ['ApoE4_c.388T>C'], 'etiology_type': ['Genetic'], 'annotation_target': ['APOE4']}).to_csv(self.kb_dir / 'axis1_etiology_kb.csv', index=False)
        pd.DataFrame({'evidence_input': ['amyloid_beta_positive'], 'marker_type': ['Primary'], 'pathway_affected': ['Amyloid-Beta'], 'interpretation': ['Positive']}).to_csv(self.kb_dir / 'axis2_molecular_kb.csv', index=False)
        pd.DataFrame({'evidence_input': ['memory_loss'], 'primary_disease': ['Alzheimer'], 'anatomical_location': ['Hippocampus'], 'clinical_correlation': ['Episodic Memory Deficit']}).to_csv(self.kb_dir / 'axis3_phenotype_kb.csv', index=False)
        joblib.dump({"model": "dummy"}, self.model_dir / "phs_model.joblib")

    def test_unified_engine_output(self):
        print("\n--- Probando la salida del motor unificado (Diagnóstico + Riesgo) ---")
        engine = BayesianEngine(kb_dir=self.kb_dir)
        patient_full_profile = {
            "id": "Patient_Integrated_001",
            "axis1": ["ApoE4_c.388T>C"],
            "axis3": ["memory_loss"],
            "demographics": {"phs_score": 0.9}
        }
        full_report = engine.run_full_tridimensional_analysis(
            patient_data=patient_full_profile,
            timestamp=datetime.now().strftime("%B %Y")
        )
        self.assertIn("tridimensional_annotation", full_report)
        self.assertIn("risk_assessment", full_report)
        self.assertNotIn("error", full_report["risk_assessment"])
        self.assertIn("relative_hazard_ratio", full_report["risk_assessment"])
        self.assertEqual(full_report["risk_assessment"]["relative_hazard_ratio"], 2.5)
        print("SUCCESS: El motor unificado ha generado un informe completo.")
        import pprint
        pprint.pprint(full_report)

if __name__ == '__main__':
    unittest.main()
