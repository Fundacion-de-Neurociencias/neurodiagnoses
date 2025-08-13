# -*- coding: utf-8 -*-
"""
Neurodiagnoses Risk Prediction: Polygenic Hazard Score (PHS) Model Training.

This script implements the training workflow for a survival model based on
genetic features to predict the risk of disease onset. It is inspired by the
methodologies of Akdeniz et al. (2025) and Bellou et al. (2025).

The core of this module is a Cox Proportional Hazards model, which is used
to estimate the hazard ratios associated with various genetic markers,
forming the basis of a Polygenic Hazard Score (PHS).

Workflow:
1. Load the analysis-ready dataset.
2. Select relevant features (genetic markers, e.g., APOE, PRS) and survival data.
3. Fit a Cox Proportional Hazards model using the 'lifelines' library.
4. Save the trained model object for later use in prediction.
"""

import os
import sys
import argparse
import pandas as pd
import joblib
from lifelines import CoxPHFitter

# Ensure the project root is in the Python path for module imports
# This is typically handled by setting PYTHONPATH or by the execution environment.
# For direct execution, consider adding the project root to sys.path if necessary.
# Example: sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
# However, for a robust project, it's better to manage Python path externally or use proper package installation.


class PHSTrainingPipeline:
    """
    A pipeline to train a Polygenic Hazard Score (PHS) model.

    This class encapsulates the logic for loading data, selecting features,
    training a Cox Proportional Hazards survival model, and saving the
    resulting model artifact.
    """

    def __init__(self, data_path, model_output_path):
        """
        Initializes the pipeline with paths for data and model output.

        Args:
            data_path (str): Path to the input parquet dataset.
            model_output_path (str): Path to save the trained .joblib model.
        """
        self.data_path = data_path
        self.model_output_path = model_output_path
        # --- Configuration for Survival Analysis ---
        # These column names should exist in the input dataset.
        self.duration_col = 'survival_duration_years'
        self.event_col = 'survival_event_occurred'
        self.features = [
            'genetics_APOE4_allele_count',
            'genetics_polygenic_risk_score'
            # Add other relevant genetic markers here as they become available
        ]
        self.model = CoxPHFitter()

    def train_model(self):
        """
        Executes the full model training workflow.
        """
        print("--- Starting PHS Model Training Workflow ---")

        # 1. Load data
        print(f"Loading dataset from: {self.data_path}")
        try:
            df = pd.read_parquet(self.data_path)
        except Exception as e:
            print(f"ERROR: Could not load or read the dataset at {self.data_path}. Error: {e}")
            return

        # 2. Prepare data for survival analysis
        required_cols = self.features + [self.duration_col, self.event_col]
        # For this PoC, we will drop rows with missing data in key columns.
        # A more robust implementation might involve imputation.
        df_survival = df[required_cols].dropna()

        if df_survival.empty:
            print("ERROR: No valid data available for survival analysis after dropping NaNs. Please check the dataset.")
            return

        print(f"Dataset prepared. Using {len(df_survival)} records for training.")
        print(f"Features: {self.features}")
        print(f"Duration Column: {self.duration_col}")
        print(f"Event Column: {self.event_col}")


        # 3. Fit the Cox Proportional Hazards model
        print("Fitting Cox Proportional Hazards model...")
        self.model.fit(df_survival, duration_col=self.duration_col, event_col=self.event_col)

        print("\n--- Model Training Summary ---")
        self.model.print_summary()
        print("----------------------------\n")


        # 4. Save the trained model
        print(f"Saving trained model to: {self.model_output_path}")
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
        joblib.dump(self.model, self.model_output_path)

        print("--- PHS Model Training Workflow Completed Successfully ---")


def main():
    """
    Main function to parse arguments and run the training pipeline.
    """
    parser = argparse.ArgumentParser(description="Train a Polygenic Hazard Score (PHS) model.")
    parser.add_argument(
        '--data_path',
        type=str,
        default='data/processed/analysis_ready_dataset.parquet',
        help='Path to the analysis-ready parquet dataset.'
    )
    parser.add_argument(
        '--model_out',
        type=str,
        default='models/risk_prediction/phs_model.joblib',
        help='Path to save the trained PHS model file.'
    )
    args = parser.parse_args()

    pipeline = PHSTrainingPipeline(data_path=args.data_path, model_output_path=args.model_out)
    pipeline.train_model()


if __name__ == '__main__':
    main()
