# -*- coding: utf-8 -*-
"""
Neurodiagnoses Risk Prediction: Polygenic Hazard Score (PHS) Model Training.

This script implements the training workflow for a survival model based on
genetic features to predict the risk of disease onset.

Methodology Update:
This script is aligned with the findings of Bellou et al., Alzheimer's Research &
Therapy (2025), which benchmarked PRS methodologies. It implements their
best-performing model strategy ("Model 5"), which uses APOE status and a
Polygenic Risk Score (calculated without the APOE region) as two separate
predictors in the risk model.
"""

import os
import sys
import argparse
import pandas as pd
import joblib
from lifelines import CoxPHFitter

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

class PHSTrainingPipeline:
    """
    Trains a Polygenic Hazard Score (PHS) model based on Cox regression.
    """
    def __init__(self, data_path, model_output_path):
        """
        Initializes the pipeline with paths for data and model output.
        """
        self.data_path = data_path
        self.model_output_path = model_output_path
        
        # --- Feature & Target Configuration ---
        # Based on Bellou et al. (2025), we use APOE and a non-APOE PRS
        # as separate predictors for the highest accuracy.
        self.features = [
            'genetics_APOE4_allele_count',
            'genetics_polygenic_risk_score_no_APOE'
        ]
        self.duration_col = 'survival_duration_years'
        self.event_col = 'survival_event_occurred'
        self.model = CoxPHFitter()

    def train_model(self):
        """
        Executes the full model training workflow.
        """
        print("--- Starting PHS Model Training Workflow (Bellou et al. methodology) ---")

        # 1. Load data
        print(f"Loading dataset from: {self.data_path}")
        try:
            df = pd.read_parquet(self.data_path)
        except Exception as e:
            print(f"ERROR: Could not load the dataset. Error: {e}")
            return

        # 2. Prepare data for survival analysis
        required_cols = self.features + [self.duration_col, self.event_col]
        df_survival = df[required_cols].dropna()

        if df_survival.empty:
            print("ERROR: No valid data for survival analysis after dropping NaNs.")
            return

        print(f"Dataset prepared. Using {len(df_survival)} records for training.")
        print(f"Predictor Features: {self.features}")
        
        # 3. Fit the Cox Proportional Hazards model
        print("Fitting Cox Proportional Hazards model...")
        self.model.fit(df_survival, duration_col=self.duration_col, event_col=self.event_col)

        print("n--- Model Training Summary ---")
        self.model.print_summary()
        print("----------------------------n")

        # 4. Save the trained model
        print(f"Saving trained model to: {self.model_output_path}")
        os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
        joblib.dump(self.model, self.model_output_path)

        print("--- PHS Model Training Workflow Completed Successfully ---")

def main():
    """
    Main function to parse arguments and run the training pipeline.
    """
    parser = argparse.ArgumentParser(
        description="Train a PHS model based on Bellou et al. (2025) methodology."
    )
    parser.add_argument(
        '--data_path',
        type=str,
        default='data/processed/analysis_ready_dataset.parquet',
        help='Path to the analysis-ready parquet dataset.'
    )
    parser.add_argument(
        '--model_out',
        type=str,
        default='models/risk_prediction/phs_model_bellou_2025.joblib',
        help='Path to save the trained PHS model file.'
    )
    args = parser.parse_args()

    pipeline = PHSTrainingPipeline(data_path=args.data_path, model_output_path=args.model_out)
    pipeline.train_model()

if __name__ == '__main__':
    main()
