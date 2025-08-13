# -*- coding: utf-8 -*-
"""
Neurodiagnoses Prognosis Module: Temporal Feature Calculation

This script processes a longitudinal dataset to engineer features that capture
disease progression over time. Inspired by methodologies from Colautti et al. (2025)
and Milà Alomà et al. (2025), it calculates rates of change for key
biomarkers and critical time intervals, such as the amyloid-tau interval.

Workflow:
1. Load a dataset with multiple entries per patient over time.
2. For each patient, calculate rates of change for specified biomarkers.
3. For each patient, calculate the time difference between key pathological events.
4. Output a new patient-level dataframe with these engineered features.
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np

# Ensure the project root is in the Python path for module imports
# This is typically handled by setting PYTHONPATH or by the execution environment.
# For direct execution, consider adding the project root to sys.path if necessary.
# Example: sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


class TemporalFeatureEngineer:
    """
    A class to engineer temporal and longitudinal features from patient data.
    """

    def __init__(self, data_path, output_path):
        """
        Initializes the feature engineering pipeline.

        Args:
            data_path (str): Path to the input longitudinal dataset (parquet format).
            output_path (str): Path to save the engineered features (parquet format).
        """
        self.data_path = data_path
        self.output_path = output_path
        # --- Configuration ---
        # Biomarkers for which to calculate the rate of change
        self.rate_change_biomarkers = [
            'biomarkers_MMSE_value',
            'biomarkers_Hippocampal Volume_value'
        ]
        # Configuration for the amyloid-tau interval calculation
        self.amyloid_biomarker = 'biomarkers_Abeta42_value'
        self.amyloid_threshold = 977  # Example threshold (lower is abnormal)
        self.tau_biomarker = 'biomarkers_pTau_value'
        self.tau_threshold = 21.8  # Example threshold (higher is abnormal)
        self.age_col = 'biomarkers_Age_value'
        self.patient_id_col = 'patient_id'


    def calculate_features(self):
        """
        Main method to run the entire feature engineering workflow.
        """
        print("--- Starting Temporal Feature Engineering ---")
        print(f"Loading data from {self.data_path}")
        df = pd.read_parquet(self.data_path)
        
        # Sort data to ensure correct chronological order
        df = df.sort_values(by=[self.patient_id_col, self.age_col])

        # Group by patient and apply feature calculation functions
        patient_groups = df.groupby(self.patient_id_col)
        
        feature_list = []
        for patient_id, group in patient_groups:
            patient_features = {self.patient_id_col: patient_id}
            
            # Calculate rates of change
            for biomarker in self.rate_change_biomarkers:
                slope, _ = self._calculate_slope(group[self.age_col], group[biomarker])
                patient_features[f'{biomarker}_rate_of_change'] = slope

            # Calculate amyloid-tau interval
            interval = self._calculate_amyloid_tau_interval(group)
            patient_features['amyloid_tau_interval_years'] = interval

            feature_list.append(patient_features)

        # Create the final dataframe
        features_df = pd.DataFrame(feature_list)
        print(f"Engineered features for {len(features_df)} patients.")

        # Save the output
        print(f"Saving engineered features to {self.output_path}")
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        features_df.to_parquet(self.output_path)
        
        print("--- Temporal Feature Engineering Completed Successfully ---")
        return features_df

    def _calculate_slope(self, x, y):
        """Calculates the slope (rate of change) using linear regression."""
        # Drop NaN values for robust calculation
        valid_indices = ~np.isnan(x) & ~np.isnan(y)
        x, y = x[valid_indices], y[valid_indices]
        
        if len(x) < 2:
            return np.nan, np.nan # Not enough data to calculate a slope
        
        # Using numpy's polyfit for simple linear regression
        slope, intercept = np.polyfit(x, y, 1)
        return slope, intercept

    def _calculate_amyloid_tau_interval(self, patient_df):
        """Calculates the time between first amyloid and tau positivity."""
        # Find the first time amyloid becomes abnormal
        amyloid_positive_df = patient_df[patient_df[self.amyloid_biomarker] < self.amyloid_threshold]
        first_amyloid_age = amyloid_positive_df[self.age_col].min()

        # Find the first time tau becomes abnormal
        tau_positive_df = patient_df[patient_df[self.tau_biomarker] > self.tau_threshold]
        first_tau_age = tau_positive_df[self.age_col].min()

        if pd.notna(first_amyloid_age) and pd.notna(first_tau_age):
            # We are interested in the interval where Tau becomes abnormal *after* Amyloid
            interval = first_tau_age - first_amyloid_age
            return interval if interval >= 0 else np.nan
        
        return np.nan


def main():
    """
    Main function to parse arguments and run the pipeline.
    """
    parser = argparse.ArgumentParser(description="Engineer temporal features for prognosis modeling.")
    parser.add_argument(
        '--data_path',
        type=str,
        default='data/processed/analysis_ready_dataset.parquet',
        help='Path to the longitudinal analysis-ready dataset.'
    )
    parser.add_argument(
        '--output_path',
        type=str,
        default='data/processed/prognosis_feature_dataset.parquet',
        help='Path to save the engineered features dataset.'
    )
    args = parser.parse_args()

    engineer = TemporalFeatureEngineer(data_path=args.data_path, output_path=args.output_path)
    engineer.calculate_features()


if __name__ == '__main__':
    main()