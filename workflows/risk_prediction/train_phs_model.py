# -*- coding: utf-8 -*-
"""
Neurodiagnoses Risk Prediction: Polygenic Hazard Score (PHS) Model Training.
(Refactored for Testability)
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

class PHSTrainingPipeline:
    def __init__(self, data_path=None, model_path='models/risk_prediction/phs_model.joblib'):
        self.data_path = data_path
        self.model_path = model_path
        self.duration_col = 'survival_duration_years'
        self.event_col = 'survival_event_occurred'
        self.features = ['genetics_APOE4_allele_count', 'genetics_polygenic_risk_score']
        self.model = None

    def train_model(self):
        print(f"--- Starting PHS Model Training ---")
        if not self.data_path:
            raise ValueError("data_path must be provided for training.")
        
        print(f"Loading dataset from: {self.data_path}")
        df = pd.read_parquet(self.data_path)
        df_survival = df[self.features + [self.duration_col, self.event_col]].dropna()
        
        if df_survival.empty:
            raise ValueError("No valid data for survival analysis.")
        
        print("Fitting Cox Proportional Hazards model...")
        cph = CoxPHFitter()
        cph.fit(df_survival, duration_col=self.duration_col, event_col=self.event_col)
        cph.print_summary()
        
        print(f"Saving trained model to: {self.model_path}")
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(cph, self.model_path)
        self.model = cph
        print("--- PHS Model Training Completed ---")

    def predict(self, patient_features: pd.DataFrame):
        """
        Predicts partial hazard for a new patient.
        Requires the model to be loaded or trained first.
        """
        if self.model is None:
            print(f"Loading model from {self.model_path} for prediction.")
            self.model = joblib.load(self.model_path)
        
        # Ensure patient_features has the right columns
        patient_features = patient_features[self.features]
        return self.model.predict_partial_hazard(patient_features)

def main():
    parser = argparse.ArgumentParser(description="Train a PHS model.")
    parser.add_argument('--data_path', default='data/processed/analysis_ready_dataset.parquet')
    parser.add_argument('--model_out', default='models/risk_prediction/phs_model.joblib')
    args = parser.parse_args()
    pipeline = PHSTrainingPipeline(data_path=args.data_path, model_path=args.model_out)
    pipeline.train_model()

if __name__ == '__main__':
    main()