import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import gradio as gr
from pathlib import Path
import pandas as pd
from unified_orchestrator import run_cohort_analysis_pipeline

def format_signature_to_html(signature: dict) -> str:
    """Convierte el output JSON del motor en un informe HTML profesional."""
    subject_id = signature.get('SubjectID', 'N/A')
    html = f"<h4>Report for Subject: {subject_id}</h4>"
    
    # Resumen Clínico
    html += "<h5>Clinical Summary (Classical Differential)</h5><table style='width:100%; border-collapse: collapse;'>"
    html += "<tr style='background-color:#f0f0f0;'><th>Diagnosis</th><th>Probability</th></tr>"
    for dx in signature.get('resumen_clinico', {}).get('diagnostico_diferencial', []):
        html += f"<tr><td style='padding: 5px; border-bottom: 1px solid #ddd;'>{dx['enfermedad']}</td><td style='padding: 5px; border-bottom: 1px solid #ddd;'><b>{dx['probabilidad']:.1%}</b></td></tr>"
    html += "</table>"
    
    # Anotación Tridimensional
    annotation = signature.get('anotacion_diagnostica_tridimensional', {})
    html += "<h5 style='margin-top: 15px;'>Tridimensional Annotation</h5>"
    
    # Eje 1
    axis1 = annotation.get('eje_1_etiologia', {})
    html += "<b>Axis 1 (Etiology):</b><ul>"
    for ev in axis1.get('raw_evidence', []): html += f"<li>{ev}</li>"
    html += "</ul>"

    # Eje 2
    axis2 = annotation.get('eje_2_fisiopatologia_molecular', {})
    html += "<b>Axis 2 (Molecular Pathology):</b><ul>"
    for path, prob in axis2.items(): html += f"<li>{path.replace('_', ' ').title()}: <b>{prob}</b></li>"
    html += "</ul>"

    # Eje 3
    axis3 = annotation.get('eje_3_fenotipo_clinico_anatomico', {})
    html += "<b>Axis 3 (Clinical-Anatomical Phenotype):</b><ul>"
    for ev in axis3.get('raw_evidence', []): html += f"<li>{ev}</li>"
    html += "</ul>"
    
    return f"<div style='border: 1px solid #eee; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>{html}</div>"

def run_cohort_analysis_ui(file_obj, diseases_to_evaluate):
    if file_obj is None: return "Please upload a CSV file."
    if not diseases_to_evaluate: raise gr.Error("Please select at least one diagnosis to evaluate.")
    
    results_list = run_cohort_analysis_pipeline(
        cohort_csv_path=file_obj.name,
        diseases_to_evaluate=diseases_to_evaluate
    )
    
    if isinstance(results_list, str): return results_list # Devolver mensaje de error
    
    # Concatenar todos los informes HTML
    full_report_html = "".join([format_signature_to_html(res) for res in results_list])
    
    return full_report_html

# --- UI Build ---
with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    gr.Markdown("# Neurodiagnoses: The AI-Powered Diagnostic Hub"); gr.Markdown("---"); gr.Markdown("⚠️ **Research Use Only Disclaimer**...")
    
    with gr.Tab("Cohort Analysis"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 1. Upload & Configure")
                cohort_csv_input = gr.File(label="Cohort CSV File", file_types=[".csv"])
                diseases_cohort_checkboxes = gr.CheckboxGroup(choices=["Alzheimer's Disease", "Frontotemporal Dementia", "Lewy Body Dementia"], label="Evaluate for (Differential Diagnosis)", value=["Alzheimer's Disease", "Frontotemporal Dementia"])
                run_cohort_btn = gr.Button("Analyze Cohort", variant="primary")
            with gr.Column(scale=2):
                gr.Markdown("### 2. Patient Reports")
                cohort_summary_display = gr.HTML(label="Cohort Results")

    run_cohort_btn.click(fn=run_cohort_analysis_ui, inputs=[cohort_csv_input, diseases_cohort_checkboxes], outputs=[cohort_summary_display])

if __name__ == "__main__":
    app.launch()
