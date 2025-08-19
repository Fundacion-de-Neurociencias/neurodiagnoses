import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import gradio as gr
from pathlib import Path
import pandas as pd
from unified_orchestrator import run_cohort_pipeline

def run_cohort_analysis_ui(file_obj):
    if file_obj is None: return None, "Please upload a CSV file to begin analysis."
    initial_prior = 0.05
    
    results = run_cohort_pipeline(
        cohort_csv_path=file_obj.name,
        initial_prior=initial_prior
    )

    # --- [LÓGICA DE REPORTE v3.1] ---
    final_html = "<h3>Differential Diagnosis Report</h3>"
    
    for patient_result in results:
        final_html += f"<div style='margin-top: 20px; border-top: 2px solid #007bff; padding-top: 10px;'>"
        final_html += f"<h4>Patient: {patient_result['SubjectID']}</h4>"
        
        # Ordenar diagnósticos por probabilidad
        sorted_diagnoses = sorted(patient_result['diagnoses'].items(), key=lambda item: item[1]['probability'], reverse=True)
        
        # Filtrar, agrupar y mostrar
        high_prob_diagnoses = []
        other_prob_sum = 0.0
        
        for disease, data in sorted_diagnoses:
            if data['probability'] > 0.05:
                high_prob_diagnoses.append((disease, data))
            else:
                other_prob_sum += data['probability']
        
        # Tabla de resultados para el paciente
        final_html += "<table style='width:100%; border-collapse: collapse; font-family: sans-serif;'>"
        final_html += "<tr style='background-color:#f0f0f0;'><th>Diagnosis</th><th>Probability</th><th>Supporting Evidence (Why)</th></tr>"

        for disease, data in high_prob_diagnoses:
            prob_pct = f"{data['probability']:.1%}"
            trail_items = "".join(f"<li>{item}</li>" for item in data['evidence_trail'])
            trail_html = f"<ul>{trail_items}</ul>" if trail_items else "No specific evidence found."
            final_html += f"<tr><td style='padding: 8px; border-bottom: 1px solid #ddd;'><b>{disease}</b></td><td style='padding: 8px; border-bottom: 1px solid #ddd; text-align:center; font-weight:bold;'>{prob_pct}</td><td style='padding: 8px; border-bottom: 1px solid #ddd; font-size: 0.9em;'>{trail_html}</td></tr>"

        if other_prob_sum > 0.0:
            final_html += f"<tr><td style='padding: 8px; border-bottom: 1px solid #ddd;'>Others (&lt;5%)</td><td style='padding: 8px; border-bottom: 1px solid #ddd; text-align:center;'>{other_prob_sum:.1%}</td><td style='padding: 8px; border-bottom: 1px solid #ddd;'>-</td></tr>"
        
        final_html += "</table></div>"

    summary_html = f"<h4>Cohort Analysis Summary</h4><p><b>{len(results)}</b> patients analyzed against the full spectrum of NDDs.</p><p style='font-size: 0.8em; color: #666;'><i>Note: Only diagnoses with a posterior probability > 5% are listed individually for each patient.</i></p>"
    return "Analysis complete. See report below.", final_html, "" # Limpiamos la tabla antigua

with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    gr.Markdown("# Neurodiagnoses: The AI-Powered Diagnostic Hub"); gr.Markdown("---"); gr.Markdown("⚠️ **Research Use Only Disclaimer**...")
    with gr.Tab("Cohort Analysis"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 1. Upload Cohort")
                gr.Markdown("Upload a CSV file with patient data. The first row must be the header.")
                cohort_csv_input = gr.File(label="Cohort CSV File", file_types=[".csv"])
                run_cohort_btn = gr.Button("Run Universal Analysis", variant="primary")
            with gr.Column(scale=2):
                gr.Markdown("### 2. Clinical Report")
                cohort_summary_display = gr.HTML(label="Cohort Summary")
                # El resultado principal ahora será un único bloque HTML
                cohort_result_html = gr.HTML(label="Patient-level Reports")
    
    run_cohort_btn.click(
        fn=run_cohort_analysis_ui, 
        inputs=[cohort_csv_input], 
        outputs=[cohort_summary_display, cohort_result_html, cohort_result_table] # Usamos un tercer output para limpiar la tabla vieja
    )

if __name__ == "__main__":
    app.launch()
