"""
Standardized Explainable AI (XAI) Reporting Module.

This script defines a class, XAIReport, to generate standardized, multi-part
HTML reports for interpreting model predictions for a single patient.
"""

import pandas as pd
import os
import joblib
import shap
import base64
from io import BytesIO
import matplotlib.pyplot as plt

# Define paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
MODEL_REGISTRY_DIR = os.path.join(PROJECT_ROOT, 'models')
REPORT_DIR = os.path.join(PROJECT_ROOT, 'reports', 'xai')

class XAIReport:
    """A class to generate a standardized XAI report for a patient."""

    def __init__(self, diagnosis_code, patient_id):
        """Initializes the report generator for a specific patient and diagnosis."""
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
        # Load model
        model_path = os.path.join(MODEL_REGISTRY_DIR, self.diagnosis_code, 'screening_model.joblib')
        self.model = joblib.load(model_path)

        # Load data
        data_path = os.path.join(DATA_DIR, f'featured_data_{self.diagnosis_code}.parquet')
        df = pd.read_parquet(data_path)
        self.patient_data = df[df['patient_id'] == self.patient_id]
        if self.patient_data.empty:
            raise ValueError(f"Patient {self.patient_id} not found in {self.diagnosis_code} data.")
        
        self.features_df = self.patient_data.drop(columns=['patient_id', 'other_variants', 'diagnosis'])
        return True

    def generate_shap_explanation(self):
        """Generates SHAP values for the specified patient."""
        print("Generating SHAP explanation...")
        X = self.features_df.to_numpy()
        self.explainer = shap.LinearExplainer(self.model, X) # Simple data, so pass it all
        self.shap_values = self.explainer.shap_values(X)
        self.prediction = self.model.predict(X)[0]

    def create_shap_force_plot_html(self):
        """Creates the HTML for a SHAP force plot."""
        force_plot = shap.force_plot(
            self.explainer.expected_value,
            self.shap_values[0, :],
            self.features_df.iloc[0, :],
            matplotlib=False
        )
        return force_plot.html()

    def generate_text_summary(self):
        """Generates a human-readable summary of the prediction and explanation."""
        pred_label = "High Risk" if self.prediction == 1 else "Low Risk"
        summary = f"<p>The model predicts a <strong>{pred_label}</strong> status for patient {self.patient_id}.</p>"
        
        shap_series = pd.Series(self.shap_values[0], index=self.features_df.columns)
        top_three = shap_series.abs().nlargest(3)
        
        summary += "<p>The most influential factors were:</p><ul>"
        for i, val in top_three.items():
            direction = "increasing" if shap_series[i] > 0 else "decreasing"
            summary += f"<li><strong>{i}</strong> (value: {self.features_df[i].values[0]:.2f}), which had a strong {direction} effect on the prediction.</li>"
        summary += "</ul>"
        return summary

    def generate_html_report(self, save_to_file=False):
        """Generates and returns a full, standardized HTML report string."""
        if self.model is None: # Lazy generation
            self.load_data_and_model()
            self.generate_shap_explanation()

        print("Generating full HTML report...")
        force_plot_html = self.create_shap_force_plot_html()
        text_summary = self.generate_text_summary()

        html_template = f"""
        <html>
        <head>
            <title>XAI Report for {self.patient_id}</title>
            <style> body {{ font-family: sans-serif; margin: 2em; }} h1, h2 {{ color: #333; }} </style>
            {shap.getjs()}
        </head>
        <body>
            <h1>XAI Diagnostic Report</h1>
            <h2>Patient: {self.patient_id} | Diagnosis Cohort: {self.diagnosis_code}</h2>
            <hr>
            <h3>Prediction Summary</h3>
            {text_summary}
            <h3>Prediction Explanation</h3>
            <p>The plot below shows the features that push the prediction higher (red) or lower (blue).</p>
            {force_plot_html}
        </body>
        </html>
        """
        
        if save_to_file:
            report_path = os.path.join(REPORT_DIR, f'XAI_Report_{self.patient_id}.html')
            with open(report_path, 'w') as f:
                f.write(html_template)
            print(f"Successfully generated report: {report_path}")
        
        return html_template


if __name__ == "__main__":
    os.makedirs(REPORT_DIR, exist_ok=True)
    # Demonstrate by creating a report for one AD and one FTD patient
    patients_to_report = [('AD', 'ND_003'), ('FTD', 'ND_005')]
    
    for diag, pat_id in patients_to_report:
        try:
            report = XAIReport(diagnosis_code=diag, patient_id=pat_id)
            report.generate_html_report(save_to_file=True) # Save file when run directly
            print("---")
        except Exception as e:
            print(f"Could not generate report for {pat_id}: {e}")
