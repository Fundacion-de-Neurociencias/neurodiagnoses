# tools/ml_pipelines/pipelines_axis3_severity_mapping.py
import os

import joblib
import pandas as pd
import shap
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


class Axis3SeverityMapperPipeline:
    """
    Implements the Axis 3 neurodegenerative severity mapper, inspired by Murad et al. (2025).
    This pipeline trains a regression model to predict a clinical severity score
    from regional neuroimaging data and uses SHAP to explain the predictions.
    """

    def __init__(
        self,
        data_path="data/simulated/axis_3_training_data.csv",
        model_path="models/axis3_severity_model.joblib",
    ):
        self.data_path = data_path
        self.model_path = model_path
        # Load data to determine features
        df = pd.read_csv(self.data_path)
        self.target = "clinical_severity_score"
        self.features = [
            col for col in df.columns if col not in ["patient_id", self.target]
        ]
        self.model = None
        self.explainer = None
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

    def train(self):
        """Trains the XGBoost regressor and creates a SHAP explainer."""
        print(
            f"--- Starting Axis 3 Severity Mapper training from '{self.data_path}' ---"
        )
        df = pd.read_csv(self.data_path)

        self.features = [
            col for col in df.columns if col not in ["patient_id", self.target]
        ]
        X = df[self.features]
        y = df[self.target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )

        print("Training XGBoost Regressor model...")
        model = xgb.XGBRegressor(
            objective="reg:squarederror", n_estimators=100, random_state=42
        )
        model.fit(X_train, y_train)

        # Evaluate model
        preds = model.predict(X_test)
        rmse = mean_squared_error(y_test, preds) ** 0.5
        print(f"Model evaluation | Test RMSE: {rmse:.4f}")

        print(f"Saving trained model to '{self.model_path}'")
        joblib.dump(model, self.model_path)
        self.model = model

        return model

    def predict_and_explain(self, patient_imaging_data: dict) -> dict:
        """
        Predicts clinical severity for a patient and explains the prediction using SHAP.
        """
        if not self.model:
            try:
                self.model = joblib.load(self.model_path)
                print("Loaded pre-trained Axis 3 model.")
            except FileNotFoundError:
                print("Model not found. Training a new one...")
                self.model = self.train()

        # Create a SHAP explainer for our model
        self.explainer = shap.TreeExplainer(self.model)

        patient_df = pd.DataFrame([patient_imaging_data])
        patient_vector = patient_df[self.features]  # Ensure correct feature order

        # Predict the score
        predicted_score = self.model.predict(patient_vector)[0]

        # Explain the prediction
        shap_values = self.explainer.shap_values(patient_vector)

        # Create a map of feature importance for this single prediction
        feature_importance = pd.DataFrame(
            list(zip(self.features, shap_values[0])), columns=["feature", "shap_value"]
        )
        feature_importance["abs_shap"] = feature_importance["shap_value"].abs()
        top_features = feature_importance.nlargest(3, "abs_shap")

        explanation = {
            row["feature"]: row["shap_value"] for index, row in top_features.iterrows()
        }

        return {
            "predicted_severity_score": float(predicted_score),
            "key_contributing_regions": explanation,
        }


if __name__ == "__main__":
    # Demonstrate the pipeline: train and then predict/explain for a sample patient
    pipeline = Axis3SeverityMapperPipeline()
    pipeline.train()

    sample_patient = {
        "lh_entorhinal_volume": 1980.0,
        "rh_entorhinal_volume": 2010.0,
        "lh_hippocampus_volume": 3050.0,
        "rh_hippocampus_volume": 3100.0,
        "lh_precuneus_thickness": 1.85,
        "rh_precuneus_thickness": 1.9,
    }

    print("\n--- Running prediction and explanation for a sample patient ---")
    result = pipeline.predict_and_explain(sample_patient)

    import json

    print(json.dumps(result, indent=2))
