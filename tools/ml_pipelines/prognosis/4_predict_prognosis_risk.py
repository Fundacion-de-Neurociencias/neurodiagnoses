# -*- coding: utf-8 -*-
"""
Neurodiagnoses Prognosis Module: Prognosis Risk Prediction

This script loads a pre-trained prognosis model and uses it to predict
the prognosis risk for new, unseen data based on engineered temporal features.

Workflow:
1. Load new patient data with engineered temporal features for prediction.
2. Load the pre-trained prognosis model.
3. Predict prognosis risk for each patient.
4. Save or display the predictions.
"""

import os
import sys
import argparse
import pandas as pd
import joblib

# Ensure the project root is in the Python path for module imports
# This is typically handled by setting PYTHONPATH or by the execution environment.
# For direct execution, consider adding the project root to sys.path if necessary.
# Example: sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
# However, for a robust project, it's better to manage Python path externally or use proper package installation.


class PrognosisPredictionPipeline:
    """
    A pipeline to predict prognosis risk using a trained model.

    This class encapsulates the logic for loading new data, loading a trained model,
    and generating prognosis risk predictions.
    """

    def __init__(self, data_path, model_path, output_path):
        """
        Initializes the pipeline with paths for input data, model, and output.

        Args:
            data_path (str): Path to the input dataset with engineered temporal features for prediction.
            model_path (str): Path to the pre-trained .joblib prognosis model.
            output_path (str): Path to save the prediction results (e.g., CSV).
        """
        self.data_path = data_path
        self.model_path = model_path
        self.output_path = output_path
        self.model = None
        self.df = None

        # --- Configuration for Features ---
        self.features = [
            'biomarkers_MMSE_value_rate_of_change',
            'biomarkers_Hippocampal Volume_value_rate_of_change',
            'amyloid_tau_interval_years'
        ]

    def load_data_and_model(self):
        """
        Loads the new patient data and the pre-trained model.
        """
        print(f"Loading new patient data from: {self.data_path}")
        try:
            self.df = pd.read_parquet(self.data_path)
        except Exception as e:
            print(f"ERROR: Could not load or read the dataset at {self.data_path}. Error: {e}")
            return False

        print(f"Loading pre-trained model from: {self.model_path}")
        try:
            self.model = joblib.load(self.model_path)
        except Exception as e:
            print(f"ERROR: Could not load the model at {self.model_path}. Error: {e}")
            return False
        return True

    def predict_prognosis(self):
        """
        Predicts the prognosis risk for the loaded data.
        """
        if self.df is None or self.model is None:
            print("ERROR: Data or model not loaded. Aborting prediction.")
            return

        # Ensure required features are present
        if not all(f in self.df.columns for f in self.features):
            print("ERROR: Input dataset is missing one or more required features for prediction.")
            print(f"Missing features: {set(self.features) - set(self.df.columns)}")
            return

        print(f"Predicting prognosis risk for {len(self.df)} records.")

        # Predict partial hazards (which can be interpreted as prognosis risk)
        # Higher values indicate higher risk.
        try:
            self.df['predicted_prognosis_risk'] = self.model.predict_partial_hazard(self.df[self.features])
            print("Prognosis risk prediction completed.")

            # Save or display results
            if self.output_path:
                os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
                self.df.to_csv(self.output_path, index=False)
                print(f"Predictions saved to: {self.output_path}")
            else:
                print("--- Prognosis Risk Predictions ---")
                print(self.df[['predicted_prognosis_risk']].head())
                print("-----------------------")

        except Exception as e:
            print(f"ERROR during prognosis risk prediction: {e}")
            return


def main():
    """
    Main function to parse arguments and run the prediction pipeline.
    """
    parser = argparse.ArgumentParser(description="Predict prognosis risk using a trained model.")
    parser.add_argument(
        '--data_path',
        type=str,
        default='data/processed/prognosis_feature_dataset.parquet',
        help='Path to the dataset with engineered temporal features for prediction.'
    )
    parser.add_argument(
        '--model_path',
        type=str,
        default='models/prognosis/prognosis_model.joblib',
        help='Path to the pre-trained prognosis model file.'
    )
    parser.add_argument(
        '--output_path',
        type=str,
        default='reports/prognosis/prognosis_predictions.csv',
        help='Path to save the prediction results (CSV format).'
    )
    args = parser.parse_args()

    pipeline = PrognosisPredictionPipeline(
        data_path=args.data_path,
        model_path=args.model_path,
        output_path=args.output_path
    )

    if pipeline.load_data_and_model():
        pipeline.predict_prognosis()


if __name__ == '__main__':
    main()
