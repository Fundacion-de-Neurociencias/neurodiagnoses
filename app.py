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
    
    classical_summary = signature.get('classical_differential', {})
    dominant_hypothesis = classical_summary.get('dominant_hypothesis')

    # --- [NUEVO]: Renderizado del Veredicto de Alta Confianza ---
    if dominant_hypothesis:
        html += f"<div style='border: 2px solid #198754; background-color: #d1e7dd; padding: 10px; border-radius: 5px; margin-bottom: 15px;'>"
        html += f"<h5 style='color: #0f5132; margin:0;'>High-Confidence Finding</h5>"
        html += f"<p style='margin:0;'>The evidence strongly suggests a dominant diagnosis of: <strong>{dominant_hypothesis}</strong>.</p></div>"

    # --- [MODIFICADO]: El Resumen Clínico ahora usa estilo condicional ---
    html += "<h5>Clinical Summary (Classical Differential)</h5><table style='width:100%; border-collapse: collapse;'>"
    html += "<tr style='background-color:#f0f0f0;'><th>Diagnosis</th><th>Probability</th></tr>"
    
    for dx in classical_summary.get('hypotheses', []):
        style = "" # Estilo por defecto
        if dominant_hypothesis:
            if dx['diagnosis'] == dominant_hypothesis:
                style = "style='color: #198754; font-weight: bold; font-size: 1.1em;'" # Verde y negrita para la hipótesis dominante
            else:
                style = "style='color: #6c757d;'" # Gris para las hipótesis no dominantes
        
        html += f"<tr><td {style} style='padding: 5px; border-bottom: 1px solid #ddd;'>{dx['diagnosis']}</td><td {style} style='padding: 5px; border-bottom: 1px solid #ddd;'><b>{dx['probability']:.1%}</b></td></tr>"
    html += "</table>"
    
    # Anotación Tridimensional (sin cambios)
    annotation = signature.get('tridimensional_annotation', {})
    html += "<h5 style='margin-top: 15px;'>Tridimensional Annotation</h5>"
    axis1 = annotation.get('axis_1_etiology', {})
    html += "<b>Axis 1 (Etiology):</b><ul>"
    for ev in axis1.get('genetic_factors', []): html += f"<li>{ev} (Genetic)</li>"
    for ev in axis1.get('environmental_risk_factors', []): html += f"<li>{ev} (Environmental)</li>"
    html += "</ul>"
    axis2 = annotation.get('axis_2_molecular_markers', {})
    html += "<b>Axis 2 (Molecular Pathology):</b><ul>"
    if 'primary_proteinopathies' in axis2:
      for p in axis2.get('primary_proteinopathies',[]): html += f"<li>Primary: {p['name']} ({p['status']})</li>"
    if 'secondary_biomarkers' in axis2:
      for k, v in axis2.get('secondary_biomarkers',{}).items(): html += f"<li>Secondary: {k} ({v})</li>"
    html += "</ul>"
    axis3 = annotation.get('axis_3_neuroanatomoclinical_correlation', [])
    html += "<b>Axis 3 (Clinical-Anatomical Phenotype):</b><ul>"
    for ev in axis3: html += f"<li>{ev['neuroanatomical_finding']}: {ev['clinical_correlation']}</li>"
    html += "</ul>"
    
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