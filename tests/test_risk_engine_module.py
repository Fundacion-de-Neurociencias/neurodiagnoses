import sys
from pathlib import Path
import pandas as pd
import unittest

# Add the path to the 'tools' directory within 'neurodiagnoses-engine' to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.absolute() / "neurodiagnoses-engine" / "tools"))

# Now import the module
from risk_prediction_engine import RiskPredictionEngine

class TestRiskPredictionEngine(unittest.TestCase):
    def setUp(self):
        self.test_data_path = "neurodiagnoses-engine/data/simulated/simulated_phs_data.csv"
        self.model_path = "tests/temp_test_model.joblib"
        self.engine = RiskPredictionEngine(model_path=self.model_path)

    def test_full_pipeline(self):
        # 1. Probar el entrenamiento
        print("n--- Probando el entrenamiento del modelo ---")
        self.engine.train(self.test_data_path)
        self.assertTrue(Path(self.model_path).exists())

        # 2. Probar la predicción
        print("n--- Probando la predicción del modelo ---")
        new_patient = pd.DataFrame([{
            "genetics_APOE4_allele_count": 1,
            "genetics_polygenic_risk_score_no_APOE": 0.8
        }])
        
        prediction = self.engine.predict(new_patient)
        
        self.assertIn("polygenic_hazard_score", prediction)
        self.assertIsInstance(prediction["polygenic_hazard_score"], float)
        print(f"Predicción generada con éxito: {prediction}")

    def tearDown(self):
        if Path(self.model_path).exists():
            Path(self.model_path).unlink()

if __name__ == '__main__':
    unittest.main()
