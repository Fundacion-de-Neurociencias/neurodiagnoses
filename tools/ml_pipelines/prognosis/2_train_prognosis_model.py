# -*- coding: utf-8 -*-
"""
Neurodiagnoses Prognosis Module: Prognosis Model Training

This script trains a machine learning model for disease prognosis using
temporal features engineered from longitudinal patient data. It leverages
techniques from survival analysis and time-series modeling.

Workflow:
1. Load the dataset with engineered temporal features.
2. Split data into training and testing sets.
3. Train a suitable prognosis model (e.g., Random Survival Forest, CoxPH).
4. Save the trained model.
"""

import os
import sys
import argparse
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from lifelines import CoxPHFitter
# from sksurv.ensemble import RandomSurvivalForest # Example for more advanced models

# Ensure the project root is in the Python path for module imports
# This is typically handled by setting PYTHONPATH or by the execution environment.
# For direct execution, consider adding the project root to sys.path if necessary.
# Example: sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


class PrognosisModelTrainer:
    """
    A class to train a prognosis model using temporal features.
    """

    def __init__(self, data_path, model_output_path):
        """
        Initializes the model trainer.

        Args:
            data_path (str): Path to the input dataset with engineered temporal features.
            model_output_path (str): Path to save the trained model.
        """
        self.data_path = data_path
        self.model_output_path = model_output_path
        self.model = CoxPHFitter() # Using CoxPHFitter as a robust baseline

        # --- Configuration for Survival Analysis ---
        self.duration_col = 'survival_duration_years' # Assuming this is available in the feature dataset
        self.event_col = 'survival_event_occurred'   # Assuming this is available in the feature dataset
        self.features = [
            'biomarkers_MMSE_value_rate_of_change',
            'biomarkers_Hippocampal Volume_value_rate_of_change',
            'amyloid_tau_interval_years'
        ]

    def train_model(self):
        """
        Main method to run the model training workflow.
        """
        print("--- Starting Prognosis Model Training ---")
        print(f"Loading data from {self.data_path}")
        df = pd.read_parquet(self.data_path)

        # Ensure required columns are present
        required_cols = self.features + [self.duration_col, self.event_col]
        df_train = df[required_cols].dropna()

        if df_train.empty:
            print("ERROR: No valid data available for training after dropping NaNs. Please check the dataset.")
            return

        print(f"Training model on {len(df_train)} records.")

        # Train the Cox Proportional Hazards model
        self.model.fit(df_train, duration_col=self.duration_col, event_col=self.event_col)

        print("\n--- Model Training Summary ---")
        self.model.print_summary()
        print("----------------------------\n")

        # Save the trained model
        print(f"Saving trained model to {self.model_output_path}")
        os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
        joblib.dump(self.model, self.model_output_path)

        print("--- Prognosis Model Training Completed Successfully ---")


def main():
    """
    Main function to parse arguments and run the pipeline.
    """
    parser = argparse.ArgumentParser(description="Train a prognosis model.")
    parser.add_argument(
        '--data_path',
        type=str,
        default='data/processed/prognosis_feature_dataset.parquet',
        help='Path to the dataset with engineered temporal features.'
    )
    parser.add_argument(
        '--model_out',
        type=str,
        default='models/prognosis/prognosis_model.joblib',
        help='Path to save the trained prognosis model.'
    )
    args = parser.parse_args()

    trainer = PrognosisModelTrainer(data_path=args.data_path, model_output_path=args.model_out)
    trainer.train_model()


if __name__ == '__main__':
    main()
