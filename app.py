import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import gradio as gr
from pathlib import Path
import pandas as pd
import re
from unified_orchestrator import run_cohort_analysis_pipeline

def linkify(text):
    """Detecta DOIs y PMIDs en un texto y los convierte en enlaces HTML."""
    # Enlace para DOI
    text = re.sub(r'(DOI:?s*)(10.d{4,9}/[-._;()/:A-Z0-9]+)', r'<a href="https://doi.org/2" target="_blank">12</a>', text, flags=re.IGNORECASE)
    # Enlace para PMID
    text = re.sub(r'(PMID:?s*)(d+)', r'<a href="https://pubmed.ncbi.nlm.nih.gov/2/" target="_blank">12</a>', text)
    return text

def format_signature_to_html(signature: dict) -> str:
    subject_id = signature.get('SubjectID', 'N/A')
    html = f"<h4>Report for Subject: {subject_id}</h4>"
    
    classical_summary = signature.get('classical_differential', {})
    dominant_hypothesis = classical_summary.get('dominant_hypothesis')

    if dominant_hypothesis:
        html += f"<div style='border: 2px solid #198754; background-color: #d1e7dd; padding: 10px; border-radius: 5px; margin-bottom: 15px;'>"
        html += f"<h5 style='color: #0f5132; margin:0;'>High-Confidence Finding</h5>"
        html += f"<p style='margin:0;'>The evidence strongly suggests a dominant diagnosis of: <strong>{dominant_hypothesis}</strong>.</p></div>"

    html += "<h5>Clinical Summary (Classical Differential)</h5><table style='width:100%; border-collapse: collapse;'>"
    html += "<tr style='background-color:#f0f0f0;'><th>Diagnosis</th><th>Probability</th></tr>"
    for dx in classical_summary.get('hypotheses', []):
        style = "style='color: #6c757d;'" if dominant_hypothesis and dx['diagnosis'] != dominant_hypothesis else ""
        if dominant_hypothesis and dx['diagnosis'] == dominant_hypothesis: style = "style='color: #198754; font-weight: bold; font-size: 1.1em;'"
        html += f"<tr><td {style} style='padding: 5px; border-bottom: 1px solid #ddd;'>{dx['diagnosis']}</td><td {style} style='padding: 5px; border-bottom: 1px solid #ddd;'><b>{dx['probability']:.1%}</b></td></tr>"
    html += "</table>"
    
    annotation = signature.get('tridimensional_annotation', {})
    html += "<h5 style='margin-top: 15px;'>Tridimensional Annotation & Evidence Trail</h5>"

    # --- [MODIFICADO]: Se renderiza la pista de evidencia para cada eje ---
    for i, (axis_key, axis_data) in enumerate(annotation.items()):
        axis_name = axis_key.replace('_', ' ').title()
        html += f"<details {'open' if i == 0 else ''}><summary><b>{axis_name}</b></summary><ul style='margin-top: 5px;'>"
        for trail_item in axis_data.get('evidence_trail', []):
            html += f"<li style='font-size: 0.9em;'>{linkify(trail_item)}</li>"
        if not axis_data.get('evidence_trail'): html += "<li>No direct evidence provided for this axis.</li>"
        html += "</ul></details>"
    
    return f"<div style='border: 1px solid #eee; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>{html}</div>"

def run_cohort_analysis_ui(file_obj):
    if file_obj is None: return "Please upload a CSV file to begin analysis."
    try:
        cohort_df = pd.read_csv(file_obj.name)
    except Exception as e:
        return f"<p style='color:red;'>Error reading CSV file: {e}</p>"
    
    results_list = run_cohort_analysis_pipeline(cohort_df=cohort_df)
    full_report_html = "".join([format_signature_to_html(res) for res in results_list])
    return full_report_html

with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    # ... (UI sin cambios)
    gr.Markdown("# Neurodiagnoses: The AI-Powered Diagnostic Hub"); gr.Markdown("---"); gr.Markdown("⚠️ **Research Use Only Disclaimer**...")
    with gr.Tab("Cohort Analysis"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 1. Upload Cohort")
                gr.Markdown("Upload a CSV file with patient data. The system will automatically perform a differential diagnosis against all known pathologies.")
                cohort_csv_input = gr.File(label="Cohort CSV File", file_types=[".csv"])
                run_cohort_btn = gr.Button("Analyze Cohort", variant="primary")
            with gr.Column(scale=2):
                gr.Markdown("### 2. Patient Reports")
                cohort_summary_display = gr.HTML(label="Cohort Results")
    run_cohort_btn.click(fn=run_cohort_analysis_ui, inputs=[cohort_csv_input], outputs=[cohort_summary_display])

if __name__ == "__main__":
    app.launch()
