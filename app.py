"""
Clinical Decision Support Dashboard.

This Gradio application serves as a prototype for a clinical workflow tool.
It allows users to select a neurodegenerative disorder, choose a patient, and
view a comprehensive report including model predictions, explainability (XAI),
and model metadata (Model Card).
"""

import gradio as gr
import pandas as pd
import os
import joblib
import json
from datetime import datetime
from tools.ml_pipelines.explainability import XAIReport # Re-use our XAI module

# --- Configuration ---
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
MODEL_REGISTRY_DIR = os.path.join(PROJECT_ROOT, 'models')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')
DISEASE_COHORTS = ['AD', 'FTD']

# --- Data Loading ---

def load_patient_ids(diagnosis_code):
    """Loads the list of patient IDs for a given disease cohort."""
    if not diagnosis_code:
        return []
    try:
        data_path = os.path.join(DATA_DIR, f'featured_data_{diagnosis_code}.parquet')
        df = pd.read_parquet(data_path)
        return df['patient_id'].tolist()
    except FileNotFoundError:
        return []

# --- Core Logic ---

def handle_feedback(diagnosis_code, patient_id, agreement, notes):
    """Saves the clinician's feedback to a CSV file."""
    if not all([diagnosis_code, patient_id, agreement, notes]):
        return "<span style='color:red'>Please fill all feedback fields.</span>"
    
    feedback_data = {
        'timestamp': [datetime.now().isoformat()],
        'diagnosis_code': [diagnosis_code],
        'patient_id': [patient_id],
        'agreement': [agreement],
        'notes': [notes]
    }
    feedback_df = pd.DataFrame(feedback_data)
    
    feedback_file = os.path.join(REPORTS_DIR, 'clinical_feedback.csv')
    # Append to file, creating it if it doesn't exist
    feedback_df.to_csv(feedback_file, mode='a', header=not os.path.exists(feedback_file), index=False)
    
    return f"<span style='color:green'>Feedback for {patient_id} submitted successfully!</span>"

def generate_clinical_report(diagnosis_code, patient_id):
    """Generates the full clinical report for a selected patient."""
    if not diagnosis_code or not patient_id:
        return "Please select a diagnosis and patient first.", "", ""

    try:
        # 1. Load Model Card
        card_path = os.path.join(MODEL_REGISTRY_DIR, diagnosis_code, 'screening_model_card.json')
        with open(card_path, 'r') as f:
            model_card = json.load(f)
        model_card_html = f"""<b>Model Name:</b> {model_card['model_name']}<br>
                           <b>Version:</b> {model_card['model_version']}<br>
                           <b>Intended Use:</b> {model_card['intended_use']}<br>
                           <b>Limitations:</b> <span style='color:red;'>{model_card['limitations']}</span>"""

        # 2. Generate XAI Report HTML
        # We re-use the class we built in the previous step
        xai_generator = XAIReport(diagnosis_code, patient_id)
        xai_generator.load_data_and_model()
        xai_generator.generate_shap_explanation()
        xai_html = xai_generator.generate_html_report() # This returns the HTML string now
        
        # 3. Get Raw Patient Data for display
        patient_df = xai_generator.patient_data
        patient_data_html = patient_df.to_html(index=False)

        return xai_html, model_card_html, patient_data_html

    except Exception as e:
        return f"<pre>An error occurred: {e}</pre>", "", ""

# --- Gradio Interface Definition ---

with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses Clinical Support") as app:
    gr.Markdown("# Neurodiagnoses Clinical Decision Support Prototype")
    gr.Markdown("Select a disorder and patient to generate a full diagnostic and explainability report.")

    with gr.Row():
        with gr.Column(scale=1):
            diag_dropdown = gr.Dropdown(label="1. Select Diagnosis Cohort", choices=DISEASE_COHORTS)
            patient_dropdown = gr.Dropdown(label="2. Select Patient ID", interactive=True)
            report_btn = gr.Button("Generate Report", variant="primary")
            
            gr.Markdown("### Patient Data")
            patient_data_display = gr.HTML()

        with gr.Column(scale=3):
            gr.Markdown("### Model Information (from Model Card)")
            model_card_display = gr.HTML()
            gr.Markdown("### Explainable AI (XAI) Report")
            xai_report_display = gr.HTML()
            
            with gr.Accordion("Submit Clinical Feedback", open=False):
                gr.Markdown("Your feedback is valuable for model improvement.")
                feedback_agreement = gr.Radio(["Agree", "Disagree"], label="Do you agree with the model's risk assessment?")
                feedback_notes = gr.Textbox(lines=3, label="Clinical Notes", placeholder="Enter any observations or disagreements here...")
                feedback_btn = gr.Button("Submit Feedback")
                feedback_status = gr.Markdown()

    # --- Event Handling ---
    def update_patient_list(diagnosis_code):
        """Callback to update the patient dropdown when a diagnosis is selected."""
        patient_ids = load_patient_ids(diagnosis_code)
        return gr.Dropdown(choices=patient_ids)

    diag_dropdown.change(fn=update_patient_list, inputs=diag_dropdown, outputs=patient_dropdown)
    report_btn.click(
        fn=generate_clinical_report,
        inputs=[diag_dropdown, patient_dropdown],
        outputs=[xai_report_display, model_card_display, patient_data_display]
    )
    feedback_btn.click(
        fn=handle_feedback,
        inputs=[diag_dropdown, patient_dropdown, feedback_agreement, feedback_notes],
        outputs=feedback_status
    )

if __name__ == "__main__":
    app.launch()