import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'neurodiagnoses-engine'))
import gradio as gr
from pathlib import Path
import pandas as pd
import re
from unified_orchestrator import run_cohort_analysis_pipeline

def format_signature_to_html(signature: dict) -> str:
    subject_id = signature.get('SubjectID', 'N/A')
    html = f"<h4>Report for Subject: {subject_id}</h4>"
    
    risk_assessment = signature.get('risk_assessment', {})
    if risk_assessment and not risk_assessment.get('error'):
        hazard_ratio = risk_assessment.get('relative_hazard_ratio', 1.0)
        interpretation = risk_assessment.get('interpretation', 'No interpretation available.')
        
        if hazard_ratio > 1.5:
            risk_color = "#dc3545"
            risk_level = "High Risk"
        elif hazard_ratio > 1.0:
            risk_color = "#ffc107"
            risk_level = "Moderate Risk"
        else:
            risk_color = "#198754"
            risk_level = "Low Risk"

        html += f"<div style='border: 2px solid {risk_color}; background-color: {risk_color}20; padding: 10px; border-radius: 5px; margin-bottom: 15px;'>"
        html += f"<h5 style='color: {risk_color}; margin:0;'>Genetic Risk Assessment</h5>"
        html += f"<p style='margin:0;'>Relative Hazard Ratio: <strong>{hazard_ratio:.2f}</strong> ({risk_level}).</p>"
        html += f"<p style='margin:0; font-size:0.8em; color:#6c757d;'><em>{interpretation}</em></p></div>"

    classical_summary = signature.get('classical_differential', {})
    html += "<h5>Clinical Summary (Classical Differential)</h5>"
    html += f"<p><strong>Dominant Hypothesis:</strong> {classical_summary.get('dominant_hypothesis', 'N/A')}</p>"
    
    return f"<div style='border: 1px solid #eee; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>{html}</div>"

def run_cohort_analysis_ui(file_obj):
    if file_obj is None: return "<p style='color:red;'>Please upload a CSV file.</p>"
    try:
        cohort_df = pd.read_csv(file_obj.name)
    except Exception as e:
        return f"<p style='color:red;'>Error reading CSV file: {e}</p>"
    
    results_list = run_cohort_analysis_pipeline(cohort_df=cohort_df)
    full_report_html = "".join([format_signature_to_html(res) for res in results_list])
    return full_report_html

with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    gr.Markdown("<h1>Neurodiagnoses: The AI-Powered Diagnostic Hub</h1>")
    gr.Markdown("---<br>⚠️ **Disclaimer:** This tool is for research purposes only and not for clinical use. ...<br>---")
    with gr.Tab("Cohort Analysis"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 1. Upload Cohort Data")
                cohort_csv_input = gr.File(label="Cohort CSV File", file_types=[".csv"])
                run_cohort_btn = gr.Button("Analyze Cohort", variant="primary")
            with gr.Column(scale=2):
                gr.Markdown("### 2. Patient Reports")
                cohort_summary_display = gr.HTML(label="Cohort Results")
    run_cohort_btn.click(fn=run_cohort_analysis_ui, inputs=[cohort_csv_input], outputs=[cohort_summary_display])

if __name__ == "__main__":
    app.launch()
