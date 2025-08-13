# -*- coding: utf-8 -*-
"""
Neurodiagnoses Risk Prediction: Polygenic Hazard Score (PHS) Model Evaluation.

This script loads a pre-trained Cox Proportional Hazards model (PHS model)
and evaluates its performance on a given dataset. It calculates key survival
metrics such as concordance index (C-index) and generates survival curves.

Workflow:
1. Load the analysis-ready evaluation dataset.
2. Load the pre-trained PHS model.
3. Evaluate the model using appropriate metrics.
4. Visualize survival curves if desired.
"""

import argparse
import os

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from lifelines.utils import concordance_index


class PHSEvaluationPipeline:
    """
    A pipeline to evaluate a Polygenic Hazard Score (PHS) model.

    This class encapsulates the logic for loading data, loading a trained model,
    evaluating its performance, and optionally visualizing results.
    """

    def __init__(self, data_path, model_path, output_dir):
        """
        Initializes the pipeline with paths for data, model, and output.

        Args:
            data_path (str): Path to the input parquet dataset for evaluation.
            model_path (str): Path to the pre-trained .joblib PHS model.
            output_dir (str): Directory to save evaluation plots.
        """
        self.data_path = data_path
        self.model_path = model_path
        self.output_dir = output_dir
        self.model = None
        self.df = None

        # --- Configuration for Survival Analysis ---
        self.duration_col = "survival_duration_years"
        self.event_col = "survival_event_occurred"
        self.features = ["genetics_APOE4_allele_count", "genetics_polygenic_risk_score"]

    def load_data_and_model(self):
        """
        Loads the evaluation dataset and the pre-trained model.
        """
        print(f"Loading evaluation dataset from: {self.data_path}")
        try:
            self.df = pd.read_parquet(self.data_path)
        except Exception as e:
            print(
                f"ERROR: Could not load or read the dataset at {self.data_path}. Error: {e}"
            )
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
            print(
                "ERROR: No valid data available for evaluation after dropping NaNs. Please check the dataset."
            )
            return

        print(f"Evaluating model on {len(df_eval)} records.")

        # Calculate concordance index (C-index)
        # The predict_partial_hazard method returns the hazard ratio for each individual.
        # A higher hazard ratio means higher risk.
        try:
            # Ensure the features used for prediction match those the model was trained on
            # and are present in the evaluation dataframe.
            if not all(f in df_eval.columns for f in self.features):
                print(
                    "ERROR: Evaluation dataset is missing one or more required features."
                )
                print(f"Missing features: {set(self.features) - set(df_eval.columns)}")
                return

            # Predict partial hazards. The C-index expects higher values for higher risk.
            # CoxPHFitter's predict_partial_hazard returns exp(linear_predictor), which is the hazard ratio.
            # Higher hazard ratio means higher risk.
            predicted_hazards = self.model.predict_partial_hazard(
                df_eval[self.features]
            )

            c_index = concordance_index(
                event_times=df_eval[self.duration_col],
                predicted_scores=predicted_hazards,
                event_observed=df_eval[self.event_col],
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

        # Predict risk scores (e.g., linear predictor or partial hazard)
        # For simplicity, let's use the linear predictor (log-hazard ratio)
        # A higher linear predictor means higher risk.
        df_eval["risk_score"] = self.model.predict_log_partial_hazard(
            df_eval[self.features]
        )

        # Create risk groups (e.g., median split)
        median_risk = df_eval["risk_score"].median()
        df_eval["risk_group"] = df_eval["risk_score"].apply(
            lambda x: "High Risk" if x > median_risk else "Low Risk"
        )

        # Plot survival curves for each group
        from lifelines import KaplanMeierFitter

        kmf = KaplanMeierFitter()

        plt.figure(figsize=(10, 7))
        for name, grouped_df in df_eval.groupby("risk_group"):
            kmf.fit(
                grouped_df[self.duration_col],
                event_observed=grouped_df[self.event_col],
                label=name,
            )
            kmf.plot_survival_function()

        plt.title("Survival Curves by Risk Group")
        plt.xlabel("Time (years)")
        plt.ylabel("Survival Probability")
        plt.grid(True)
        plot_path = os.path.join(self.output_dir, "survival_curves.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"Survival curves saved to: {plot_path}")


def main():
    """
    Main function to parse arguments and run the evaluation pipeline.
    """
    parser = argparse.ArgumentParser(
        description="Evaluate a Polygenic Hazard Score (PHS) model."
    )
    parser.add_argument(
        "--data_path",
        type=str,
        default="data/processed/analysis_ready_dataset.parquet",
        help="Path to the analysis-ready parquet dataset for evaluation.",
    )
    parser.add_argument(
        "--model_path",
        type=str,
        default="models/risk_prediction/phs_model.joblib",
        help="Path to the pre-trained PHS model file.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="reports/risk_prediction/",
        help="Directory to save evaluation plots and reports.",
    )
    args = parser.parse_args()

    pipeline = PHSEvaluationPipeline(
        data_path=args.data_path, model_path=args.model_path, output_dir=args.output_dir
    )

    if pipeline.load_data_and_model():
        pipeline.evaluate_model()


if __name__ == "__main__":
    main()
