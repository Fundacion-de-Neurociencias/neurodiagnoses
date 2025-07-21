# tools/ml_pipelines/pipelines_axis2.py
import pandas as pd
import joblib
import os

class Axis2Pipeline:
    """
    ML pipeline for Axis 2 (Molecular) prediction.
    Loads pre-trained pTau and tTau models to perform predictions.
    """
    def __init__(self):
        ptau_model_path = 'models/axis2_ptau_model.joblib'
        ttau_model_path = 'models/axis2_ttau_model.joblib'

        if not os.path.exists(ptau_model_path) or not os.path.exists(ttau_model_path):
            raise FileNotFoundError("One or more Axis 2 model files are missing. Run training scripts first.")

        # Load both models
        self.ptau_model = joblib.load(ptau_model_path)
        self.ttau_model = joblib.load(ttau_model_path)

        # Feature order is consistent for both models
        self.feature_order = ['AGE', 'APOE4', 'Ventricles', 'Hippocampus', 'ADAS13_bl']

        print(f"INFO: Axis 2 pipeline initialized. pTau and tTau models loaded.")

    def predict(self, input_data: dict) -> str:
        """
        Predicts pTau and tTau positivity and returns a combined string.
        """
        input_df = pd.DataFrame([input_data])
        # Reorder columns to match model's training order
        input_df = input_df[self.feature_order]

        # Predict with each model
        ptau_pred_val = self.ptau_model.predict(input_df)[0]
        ttau_pred_val = self.ttau_model.predict(input_df)[0]

        # Format results
        ptau_status = 'pTau+' if ptau_pred_val == 1 else 'pTau-'
        ttau_status = 'tTau+' if ttau_pred_val == 1 else 'tTau-'

        # Return combined string
        return f"{ptau_status}, {ttau_status}"