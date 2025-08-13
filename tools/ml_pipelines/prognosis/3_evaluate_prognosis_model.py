# -*- coding: utf-8 -*-
"""
Neurodiagnoses Prognosis Module: Prognosis Model Evaluation

This script loads a pre-trained prognosis model and evaluates its performance
on a given dataset. It calculates key survival metrics such as concordance index
(C-index) and generates survival curves.

Workflow:
1. Load the dataset with engineered temporal features for evaluation.
2. Load the pre-trained prognosis model.
3. Evaluate the model using appropriate metrics.
4. Visualize survival curves if desired.
"""

import os
import sys
import argparse
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
from lifelines.plotting import plot_lifetimes

# Ensure the project root is in the Python path for module imports
# This is typically handled by setting PYTHONPATH or by the execution environment.
# For direct execution, consider adding the project root to sys.path if necessary.
# Example: sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
# However, for a robust project, it's better to manage Python path externally or use proper package installation.


class PrognosisModelEvaluator:
    """
    A class to evaluate a prognosis model.

    This class encapsulates the logic for loading data, loading a trained model,
    evaluating its performance, and optionally visualizing results.
    """

    def __init__(self, data_path, model_path, output_dir):
        """
        Initializes the evaluator.

        Args:
            data_path (str): Path to the input dataset with engineered temporal features for evaluation.
            model_path (str): Path to the pre-trained .joblib prognosis model.
            output_dir (str): Directory to save evaluation plots.
        """
        self.data_path = data_path
        self.model_path = model_path
        self.output_dir = output_dir
        self.model = None
        self.df = None

        # --- Configuration for Survival Analysis ---
        self.duration_col = 'survival_duration_years'
        self.event_col = 'survival_event_occurred'
        self.features = [
            'biomarkers_MMSE_value_rate_of_change',
            'biomarkers_Hippocampal Volume_value_rate_of_change',
            'amyloid_tau_interval_years'
        ]

    def load_data_and_model(self):
        """
        Loads the evaluation dataset and the pre-trained model.
        """
        print(f"Loading evaluation dataset from: {self.data_path}")
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

    def evaluate_model(self):
        """
        Evaluates the loaded model on the dataset.
        """
        if self.df is None or self.model is None:
            print("ERROR: Data or model not loaded. Aborting evaluation.")
            return

        # Ensure required columns are present and handle missing data
        required_cols = self.features + [self.duration_col, self.event_col]
        df_eval = self.df[required_cols].dropna()

        if df_eval.empty:
            print("ERROR: No valid data available for evaluation after dropping NaNs. Please check the dataset.")
            return

        print(f"Evaluating model on {len(df_eval)} records.")

        # Calculate concordance index (C-index)
        try:
            if not all(f in df_eval.columns for f in self.features):
                print("ERROR: Evaluation dataset is missing one or more required features.")
                print(f"Missing features: {set(self.features) - set(df_eval.columns)}")
                return

            predicted_hazards = self.model.predict_partial_hazard(df_eval[self.features])

            c_index = concordance_index(
                event_times=df_eval[self.duration_col],
                predicted_scores=predicted_hazards,
                event_observed=df_eval[self.event_col]
            )
            print(f"Concordance Index (C-index): {c_index:.4f}")

        except Exception as e:
            print(f"ERROR during C-index calculation: {e}")
            return

        # Optional: Visualize survival curves for different risk groups
        self.visualize_survival_curves(df_eval)

    def visualize_survival_curves(self, df_eval):
        """
        Visualizes survival curves based on predicted risk.
        For demonstration, we'll split into high and low risk groups.
        """
        if self.model is None:
            print("Model not loaded, cannot visualize survival curves.")
            return

        print("Generating survival curve visualization...")
        os.makedirs(self.output_dir, exist_ok=True)

        df_eval['risk_score'] = self.model.predict_log_partial_hazard(df_eval[self.features])

        median_risk = df_eval['risk_score'].median()
        df_eval['risk_group'] = df_eval['risk_score'].apply(lambda x: 'High Risk' if x > median_risk else 'Low Risk')

        from lifelines import KaplanMeierFitter
        kmf = KaplanMeierFitter()

        plt.figure(figsize=(10, 7))
        for name, grouped_df in df_eval.groupby('risk_group'):
            kmf.fit(grouped_df[self.duration_col], event_observed=grouped_df[self.event_col], label=name)
            kmf.plot_survival_function()

        plt.title('Survival Curves by Risk Group')
        plt.xlabel('Time (years)')
        plt.ylabel('Survival Probability')
        plt.grid(True)
        plot_path = os.path.join(self.output_dir, 'prognosis_survival_curves.png')
        plt.savefig(plot_path)
        plt.close()
        print(f"Survival curves saved to: {plot_path}")


def main():
    """
    Main function to parse arguments and run the evaluation pipeline.
    """
    parser = argparse.ArgumentParser(description="Evaluate a prognosis model.")
    parser.add_argument(
        '--data_path',
        type=str,
        default='data/processed/prognosis_feature_dataset.parquet',
        help='Path to the dataset with engineered temporal features for evaluation.'
    )
    parser.add_argument(
        '--model_path',
        type=str,
        default='models/prognosis/prognosis_model.joblib',
        help='Path to the pre-trained prognosis model file.'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default='reports/prognosis/',
        help='Directory to save evaluation plots and reports.'
    )
    args = parser.parse_args()

    pipeline = PrognosisModelEvaluator(
        data_path=args.data_path,
        model_path=args.model_path,
        output_dir=args.output_dir
    )

    if pipeline.load_data_and_model():
        pipeline.evaluate_model()


if __name__ == '__main__':
    main()
