# tools/ml_pipelines/pipelines_axis3.py
import pandas as pd
import joblib
import os

class Axis3Pipeline:
    """
    Machine Learning pipeline for Axis 3 (Phenotypic) prediction.
    Loads a pre-trained model to perform predictions.
    """
    def __init__(self):
        # 1. Load the pre-trained model
        model_path = 'models/axis3_model.joblib'
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at '{model_path}'. Please run the data generator and training script first.")
        
        self.model = joblib.load(model_path)
        
        # Define the feature order based on how the model was trained
        self.feature_order = ['age', 'MMSE', 'hippocampal_volume', 'cortical_thickness', 'ventricular_volume']
        
        print(f"INFO: Axis 3 pipeline initialized and pre-trained model loaded from '{model_path}'.")

    def predict(self, input_data: dict) -> str:
        """
        Performs a phenotypic prediction based on input data.
        """
        input_df = pd.DataFrame([input_data])
        # Reorder columns to match model's training order
        input_df = input_df[self.feature_order]
        
        prediction = self.model.predict(input_df)
        
        return prediction[0]