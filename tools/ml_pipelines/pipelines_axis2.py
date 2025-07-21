# tools/ml_pipelines/pipelines_axis2.py
import pandas as pd
import joblib
import os

class Axis2Pipeline:
    """
    ML pipeline for Axis 2 (Molecular) prediction.
    Specifically, it predicts pTau positivity based on a pre-trained model
    inspired by the ADNI CSF prediction notebook.
    """
    def __init__(self):
        model_path = 'models/axis2_ptau_model.joblib'
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at '{model_path}'. Run the training script first.")
        
        self.model = joblib.load(model_path)
        
        # Define feature order based on SHAP analysis from the README
        self.feature_order = [
            'ADAS13_bl', 
            'APOE4', 
            'AGE', 
            'Hippocampus', 
            'Ventricles'
        ]
        
        print(f"INFO: Axis 2 (pTau) pipeline initialized and model loaded from '{model_path}'.")

    def _create_interaction_features(self, df):
        """Creates interaction features as described in the README."""
        # Ensure APOE4 and Age are present for interaction term
        if 'APOE4' in df.columns and 'AGE' in df.columns:
            df['APOE4_AGE'] = df['APOE4'] * df['AGE']
        
        # This is a simplified feature engineering step.
        # A real implementation would require more complex logic from the notebook.
        # For now, we ensure the core features are present.
        
        # The model was trained on these features, but we only require the base features as input
        # and create interactions here. This part would need to be expanded based on the notebook.
        final_features = ['ADAS13_bl', 'APOE4_AGE', 'Hippocampus', 'Ventricles']
        
        # For simplicity, we'll assume a slightly different model for now
        # that doesn't rely on features we can't easily calculate.
        # We will adjust this in the next step.
        
        return df

    def predict(self, input_data: dict) -> str:
        """
        Predicts pTau positivity ('pTau+' or 'pTau-').
        
        Required input_data keys:
        - ADAS13_bl: (float) ADAS-Cog 13 score at baseline
        - APOE4: (int) Number of APOE4 alleles (0, 1, or 2)
        - AGE: (float) Age of the patient
        - Hippocampus: (float) Hippocampal volume (normalized)
        - Ventricles: (float) Ventricular volume (normalized)
        """
        input_df = pd.DataFrame([input_data])
        
        # The feature engineering part would go here, for now we pass the data directly
        # input_df = self._create_interaction_features(input_df)

        # Ensure columns are in the correct order for the model
        input_df = input_df[self.feature_order]
        
        # Prediction returns 1 for 'pTau+' and 0 for 'pTau-'
        prediction_value = self.model.predict(input_df)[0]
        
        return 'pTau+' if prediction_value == 1 else 'pTau-'