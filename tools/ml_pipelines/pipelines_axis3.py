# tools/ml_pipelines/pipelines_axis3.py

import joblib
import pandas as pd


class Axis3PhenotypicPipeline:
    def __init__(self):
        self.model_path = "models/axis3_model.joblib"
        self.feature_order = [
            "age",
            "cortical_thickness",
            "ventricular_volume",
            "MMSE",
            "hippocampal_volume",
        ]
        self.model = joblib.load(self.model_path)

    def predict(self, features_dict):
        # Convert dict to DataFrame
        input_df = pd.DataFrame([features_dict])

        # Standardize column names
        input_df.columns = [col.strip().lower() for col in input_df.columns]
        required_cols = [col.lower() for col in self.feature_order]

        # Rename input_df columns to exact match if needed
        rename_map = {
            col.lower(): col
            for col in self.feature_order
            if col.lower() in input_df.columns
        }
        input_df = input_df.rename(columns=rename_map)

        # Check for missing columns
        if not all(col in input_df.columns for col in self.feature_order):
            missing = [col for col in self.feature_order if col not in input_df.columns]
            raise KeyError(
                f"❌ Missing required features for Axis 3 prediction: {missing}"
            )

        input_df = input_df[self.feature_order]

        # Predict
        prediction = self.model.predict(input_df)[0]
        return {
            "axis": 3,
            "prediction": prediction,
            "input_used": input_df.to_dict(orient="records")[0],
        }
