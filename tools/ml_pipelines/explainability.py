# -*- coding: utf-8 -*-
"""
Standardized Explainable AI (XAI) Reporting Module.
(Refactored to return Matplotlib figure objects for direct rendering)
"""

import pandas as pd
import os
import joblib
import shap
import matplotlib.pyplot as plt

# Define paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
MODEL_REGISTRY_DIR = os.path.join(PROJECT_ROOT, 'models')

class XAIReport:
    """A class to generate standardized XAI report assets for a patient."""

    def __init__(self, diagnosis_code, patient_id):
        self.diagnosis_code = diagnosis_code
        self.patient_id = patient_id
        self.model = None
        self.patient_data = None
        self.features_df = None
        self.shap_values = None
        self.explainer = None
        self.prediction = None

    def load_data_and_model(self):
        """Loads the correct model and patient data from the registries."""
        print(f"Loading data for patient {self.patient_id} ({self.diagnosis_code})...")
        model_path = os.path.join(MODEL_REGISTRY_DIR, self.diagnosis_code, 'screening_model.joblib')
        self.model = joblib.load(model_path)

        data_path = os.path.join(DATA_DIR, f'featured_data_{self.diagnosis_code}.parquet')
        df = pd.read_parquet(data_path)
        self.patient_data = df[df['patient_id'] == self.patient_id]
        if self.patient_data.empty:
            raise ValueError(f"Patient {self.patient_id} not found in {self.diagnosis_code} data.")
        
        self.features_df = self.patient_data.drop(columns=['patient_id', 'other_variants', 'diagnosis'], errors='ignore')
        return True

    def generate_shap_explanation(self):
        """Generates SHAP values for the specified patient."""
        print("Generating SHAP explanation...")
        self.explainer = shap.Explainer(self.model.predict, self.features_df)
        self.shap_values = self.explainer(self.features_df)
        self.prediction = self.model.predict(self.features_df)[0]

    def create_shap_force_plot_figure(self):
        """Creates a Matplotlib SHAP force plot and returns the figure object."""
        shap.force_plot(
            self.explainer.expected_value,
            self.shap_values.values[0],
            self.features_df.iloc[0],
            matplotlib=True,
            show=False
        )
        fig = plt.gcf()
        plt.close() # Important to close the plot to prevent it from displaying in the console
        return fig

    def generate_text_summary(self):
        """Generates a human-readable summary of the prediction and explanation."""
        pred_label = "High Risk" if self.prediction == 1 else "Low Risk"
        summary = f"<p>The model predicts a <strong>{pred_label}</strong> status for patient {self.patient_id}.</p>"
        
        shap_series = pd.Series(self.shap_values.values[0], index=self.features_df.columns)
        top_three = shap_series.abs().nlargest(3)
        
        summary += "<p>The most influential factors were:</p><ul>"
        for i, val in top_three.items():
            direction = "increasing" if shap_series[i] > 0 else "decreasing"
            summary += f"<li><strong>{i}</strong> (value: {self.features_df[i].values[0]:.2f}), which had a strong {direction} effect on the prediction.</li>"
        summary += "</ul>"
        return summary

    def generate_report_assets(self):
        """Generates and returns all assets needed for the report."""
        if self.model is None:
            self.load_data_and_model()
            self.generate_shap_explanation()

        print("Generating report assets...")
        text_summary = self.generate_text_summary()
        plot_figure = self.create_shap_force_plot_figure()
        
        report_assets = {
            "text_summary": text_summary,
            "plot_figure": plot_figure
        }
        return report_assets
