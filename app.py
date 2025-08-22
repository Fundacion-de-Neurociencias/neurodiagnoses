import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'neurodiagnoses-engine'))

import gradio as gr
from pathlib import Path
import pandas as pd
import re
from unified_orchestrator import run_cohort_analysis_pipeline, get_engine

def format_signature_to_html(signature: dict) -> str:
    """Convierte el output JSON del motor en un informe HTML profesional y accionable."""
    subject_id = signature.get('SubjectID', 'N/A')
    html = f"<h4>Report for Subject: {subject_id}</h4>"
    
    classical_summary = signature.get('classical_differential', {})
    
    # --- [NUEVO]: Renderizado de Alertas Accionables de Alta Prioridad ---
    actionable_alert = classical_summary.get('actionable_alert')
    if actionable_alert:
        alert_color = "#ffc107" # Ámbar
        alert_border = "#ffc107"
        html += f"<div style='border: 2px solid {alert_border}; background-color: {alert_color}30; padding: 10px; border-radius: 5px; margin-bottom: 15px;'>"
        html += f"<h5 style='color: #664d03; margin:0; font-weight:bold;'> actionable_alert: Treatable Mimic Detected</h5>"
        html += f"<p style='margin:0;'>Potential Diagnosis: <strong>{actionable_alert['disease']}</strong> ({actionable_alert['category']})</p>"
        html += f"<p style='margin:0; font-size:0.9em;'><em>{actionable_alert['reason']}</em></p>"
        html += f"<p style='margin:0; font-size:0.9em; font-weight:bold;'>Recommendation: {actionable_alert['recommendation']}</p></div>"
    
    # --- [MODIFICADO]: El Resumen Clínico ahora agrupa por categoría ---
    html += "<h5>Clinical Summary (Classical Differential)</h5><table style='width:100%; border-collapse: collapse;'>"
    html += "<tr style='background-color:#f0f0f0;'><th>Category</th><th>Diagnosis</th><th>Probability</th></tr>"
    
    engine = get_engine() # Obtenemos una instancia para acceder al disease_map
    
    # Agrupamos las hipótesis por categoría
    hypotheses_by_cat = {}
    for dx in classical_summary.get('hypotheses', []):
        category = engine.disease_map.get(dx['diagnosis'], 'Unknown')
        if category not in hypotheses_by_cat:
            hypotheses_by_cat[category] = []
        hypotheses_by_cat[category].append(dx)

    for category, hypotheses in hypotheses_by_cat.items():
        for i, dx in enumerate(hypotheses):
            html += f"<tr>"
            if i == 0:
                html += f"<td style='padding: 5px; border-bottom: 1px solid #ddd; font-weight:bold;' rowspan='{len(hypotheses)}'>{category}</td>"
            html += f"<td style='padding: 5px; border-bottom: 1px solid #ddd;'>{dx['diagnosis']}</td>"
            html += f"<td style='padding: 5px; border-bottom: 1px solid #ddd;'><b>{dx['probability']:.1%}</b></td>"
            html += f"</tr>"
    html += "</table>"
    
    # Anotación Tridimensional (simplificada para claridad)
    html += "<h5 style='margin-top: 15px;'>Tridimensional Annotation</h5><p><i>(Detailed evidence trail for each axis would be displayed here...)</i></p>"
    
    return f"<div style='border: 1px solid #eee; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>{html}</div>"

def run_cohort_analysis_ui(file_obj):
    if file_obj is None: return "Please upload a CSV file."
    try:
        # Usamos el nuevo fichero de cohorte complejo para la demo
        cohort_df = pd.read_csv(file_obj.name)
    except Exception as e:
        return f"<p style='color:red;'>Error reading CSV file: {e}</p>"
    
    results_list = run_cohort_analysis_pipeline(cohort_df=cohort_df)
    full_report_html = "".join([format_signature_to_html(res) for res in results_list])
    return full_report_html

# ... (El resto del layout de la UI de Gradio no cambia) ...
with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    gr.Markdown("# Neurodiagnoses: The AI-Powered Diagnostic Hub"); gr.Markdown("---"); gr.Markdown("⚠️ **Research Use Only Disclaimer**...")
    with gr.Tab("Cohort Analysis"):
        gr.Markdown("Use the sample file `neurodiagnoses-engine/data/simulated/sample_cohort_complex.csv` to test the new trans-categorical differential diagnosis.")
        with gr.Row():
            with gr.Column(scale=1):
                cohort_csv_input = gr.File(label="Cohort CSV File", file_types=[".csv"])
                run_cohort_btn = gr.Button("Analyze Cohort", variant="primary")
            with gr.Column(scale=2):
                cohort_summary_display = gr.HTML(label="Patient Reports")
    run_cohort_btn.click(fn=run_cohort_analysis_ui, inputs=[cohort_csv_input], outputs=[cohort_summary_display])

if __name__ == "__main__":
    app.launch()