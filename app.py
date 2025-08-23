import sys, os, pandas as pd, gradio as gr
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from unified_orchestrator import run_cohort_analysis_pipeline

def format_signature_to_html(signature: dict) -> str:
    html = f"<h4>Report for Subject: {signature.get('SubjectID', 'N/A')}</h4>"
    # ... (Renderizado de Riesgo, DiagnÃ³stico, etc. sin cambios)
    
    # --- [NUEVO]: Renderizado de la secciÃ³n de Explicabilidad ---
    explanations = signature.get('explicability_trail', [])
    if explanations:
        html += "<h5 style='margin-top: 15px;'>Scientific Rationale</h5>"
        html += "<details><summary>Click to see the scientific evidence behind this analysis</summary>"
        for item in explanations:
            html += f"<div style='margin-top: 10px; padding: 10px; border-left: 3px solid #0d6efd; background-color: #f8f9fa;'>"
            html += f"<strong>Concept: {item['title']}</strong><br>"
            html += f"<p style='font-size: 0.9em; margin:0;'><em>{item['summary']}</em></p>"
            html += f"<a href='https://doi.org/{item['source_paper_doi']}' target='_blank' style='font-size: 0.8em;'>Source Paper (DOI)</a>"
            html += "</div>"
        html += "</details>"
        
    return f"<div style='border: 1px solid #eee; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>{html}</div>"

# El resto de la UI y la lÃ³gica de llamada no cambian
def run_cohort_analysis_ui(file_obj):
    if file_obj is None: return "Please upload a CSV file."
    results_list = run_cohort_analysis_pipeline(pd.read_csv(file_obj.name))
    return "".join([format_signature_to_html(res) for res in results_list])

with gr.Blocks(theme=gr.themes.Soft()) as app:
    # ... (Layout de la UI sin cambios)
    gr.Markdown("# Neurodiagnoses: The AI-Powered Diagnostic Hub")
    with gr.Tab("Cohort Analysis"):
        cohort_csv_input = gr.File(label="Cohort CSV File")
        run_cohort_btn = gr.Button("Analyze Cohort", variant="primary")
        cohort_summary_display = gr.HTML(label="Patient Reports")
    run_cohort_btn.click(fn=run_cohort_analysis_ui, inputs=[cohort_csv_input], outputs=[cohort_summary_display])

if __name__ == "__main__":
    app.launch()
