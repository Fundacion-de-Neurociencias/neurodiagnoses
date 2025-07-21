# tools/ml_pipelines/pipelines_axis2.py
import pandas as pd
import joblib
import os

class Axis2Pipeline:
    """
    Machine Learning pipeline for Axis 2 (Molecular) prediction.
    Loads a pre-trained model to perform predictions.
    """
    def __init__(self):
        model_path = 'models/axis2_ptau_model.joblib'
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at '{model_path}'. Run the training script first.")

        self.model = joblib.load(model_path)

        # --- CORRECTION HERE ---
        # The feature order must EXACTLY match the order used during training.
        self.feature_order = ['AGE', 'APOE4', 'Ventricles', 'Hippocampus', 'ADAS13_bl']

        print(f"INFO: Axis 2 (pTau) pipeline initialized and pre-trained model loaded from '{model_path}'.")

    def predict(self, input_data: dict) -> str:
        """
        Predicts pTau positivity ('pTau+' or 'pTau-').
        """
        input_df = pd.DataFrame([input_data])
        # Reorder columns to match model's training order
        input_df = input_df[self.feature_order]

        prediction_value = self.model.predict(input_df)[0]

        return 'pTau+' if prediction_value == 1 else 'pTau-'