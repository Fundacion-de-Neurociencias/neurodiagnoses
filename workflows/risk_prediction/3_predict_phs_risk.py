# -*- coding: utf-8 -*-
"""
Neurodiagnoses Risk Prediction: Polygenic Hazard Score (PHS) Risk Prediction.

This script loads a pre-trained Cox Proportional Hazards model (PHS model)
and uses it to predict the Polygenic Hazard Score (PHS) for new, unseen data.

Workflow:
1. Load new patient data for prediction.
2. Load the pre-trained PHS model.
3. Predict PHS for each patient.
4. Save or display the predictions.
"""

import os
import argparse
import pandas as pd
import joblib


class PHSPredictionPipeline:
    """
    A pipeline to predict Polygenic Hazard Score (PHS) using a trained model.

    This class encapsulates the logic for loading new data, loading a trained model,
    and generating PHS predictions.
    """

    def __init__(self, data_path, model_path, output_path):
        """
        Initializes the pipeline with paths for input data, model, and output.

        Args:
            data_path (str): Path to the input parquet dataset for prediction.
            model_path (str): Path to the pre-trained .joblib PHS model.
            output_path (str): Path to save the prediction results (e.g., CSV).
        """
        self.data_path = data_path
        self.model_path = model_path
        self.output_path = output_path
        self.model = None
        self.df = None

        # --- Configuration for Features ---
        self.features = [
            'genetics_APOE4_allele_count',
            'genetics_polygenic_risk_score'
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

    def predict_phs(self):
        """
        Predicts the PHS for the loaded data.
        """
        if self.df is None or self.model is None:
            print("ERROR: Data or model not loaded. Aborting prediction.")
            return

        # Ensure required features are present
        if not all(f in self.df.columns for f in self.features):
            print("ERROR: Input dataset is missing one or more required features for prediction.")
            print(f"Missing features: {set(self.features) - set(self.df.columns)}")
            return

        print(f"Predicting PHS for {len(self.df)} records.")

        # Predict partial hazards (which can be interpreted as PHS)
        # Higher values indicate higher risk.
        try:
            self.df['predicted_phs'] = self.model.predict_partial_hazard(self.df[self.features])
            print("PHS prediction completed.")

            # Save or display results
            if self.output_path:
                os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
                self.df.to_csv(self.output_path, index=False)
                print(f"Predictions saved to: {self.output_path}")
            else:
                print("--- PHS Predictions ---")
                print(self.df[['predicted_phs']].head())
                print("-----------------------")

        except Exception as e:
            print(f"ERROR during PHS prediction: {e}")
            return


def main():
    """
    Main function to parse arguments and run the prediction pipeline.
    """
    parser = argparse.ArgumentParser(description="Predict Polygenic Hazard Score (PHS) using a trained model.")
    parser.add_argument(
        '--data_path',
        type=str,
        default='data/processed/analysis_ready_dataset.parquet',
        help='Path to the input parquet dataset for prediction.'
    )
    parser.add_argument(
        '--model_path',
        type=str,
        default='models/risk_prediction/phs_model.joblib',
        help='Path to the pre-trained PHS model file.'
    )
    parser.add_argument(
        '--output_path',
        type=str,
        default='reports/risk_prediction/phs_predictions.csv',
        help='Path to save the prediction results (CSV format).'
    )
    args = parser.parse_args()

    pipeline = PHSPredictionPipeline(
        data_path=args.data_path,
        model_path=args.model_path,
        output_path=args.output_path
    )

    if pipeline.load_data_and_model():
        pipeline.predict_phs()


if __name__ == '__main__':
    main()
