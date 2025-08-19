import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import gradio as gr
from pathlib import Path
import pandas as pd
# --- [CAMBIO]: Importamos solo la función de cohorte ---
from unified_orchestrator import run_cohort_pipeline
from tools.bayesian_engine.core import BayesianEngine

# --- Lógica de la App ---
def get_available_evidence():
    # Esta función ahora solo es necesaria para la pestaña de un solo caso (desactivada)
    # En el futuro, podría usarse para validar cabeceras de CSV.
    engine = BayesianEngine(
        axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
        axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods_v2.csv"),
        axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv")
    )
    axis1 = sorted(engine.axis1_df['biomarker_name'].unique().tolist())
    axis2 = sorted(engine.axis2_df['biomarker_name'].unique().tolist())
    axis3_all = engine.axis3_df['biomarker_name'].unique()
    axis3_pheno = sorted([b for b in axis3_all if 'Volume' not in b])
    axis3_img = sorted(list(set([name.replace('Left_', '').replace('Right_', '') for name in axis3_all if 'Volume' in name])))
    return axis1, axis2, axis3_pheno, axis3_img

def run_cohort_analysis_ui(file_obj):
    """
    Función principal de la UI. Llama al orquestador y luego formatea los
    resultados con la lógica de filtrado del 5% y agrupación.
    """
    if file_obj is None:
        return None, "Please upload a CSV file to begin analysis."

    initial_prior = 0.10 # Prior base para el análisis universal
    
    # El orquestador ya no necesita la lista de enfermedades
    results_df = run_cohort_pipeline(
        cohort_csv_path=file_obj.name,
        initial_prior=initial_prior
    )

    # --- [NUEVA LÓGICA DE FILTRADO Y AGRUPACIÓN] ---
    prob_cols = [col for col in results_df.columns if col.startswith('Prob_')]
    
    # DataFrame para mostrar en la UI, empezamos con las columnas originales
    display_df_data = []

    for index, patient_row in results_df.iterrows():
        patient_display = {"SubjectID": patient_row["SubjectID"]}
        
        high_prob_diseases = {}
        other_prob_sum = 0.0

        for col in prob_cols:
            disease_name = col.replace("Prob_", "").replace("_", " ")
            prob = patient_row[col]
            if prob > 0.05:
                high_prob_diseases[disease_name] = f"{prob:.1%}"
            else:
                other_prob_sum += prob
        
        # Añadir las enfermedades con alta probabilidad
        patient_display.update(high_prob_diseases)
        
        # Añadir la categoría "Otras" si es necesario
        if other_prob_sum > 0.0:
            patient_display["Others (<5%)"] = f"{other_prob_sum:.1%}"

        display_df_data.append(patient_display)
    
    display_df = pd.DataFrame(display_df_data).fillna('-')

    summary_html = f"<h4>Cohort Analysis Summary:</h4>"
    summary_html += f"<ul><li><b>{len(results_df)}</b> patients analyzed against the full spectrum of NDDs.</li></ul>"
    summary_html += f"<p style='font-size: 0.8em; color: #666;'><i>Note: Only diagnoses with a posterior probability > 5% are listed individually. All others are grouped under 'Others'.</i></p>"

    return display_df, summary_html

# --- Construcción de la Interfaz ---
with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    gr.Markdown("# Neurodiagnoses: The AI-Powered Diagnostic Hub"); gr.Markdown("---"); gr.Markdown("⚠️ **Research Use Only Disclaimer**...")
    
    with gr.Tab("Cohort Analysis"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 1. Upload Cohort")
                gr.Markdown("Upload a CSV file with your patient data. The first row must be the header with biomarker names.")
                cohort_csv_input = gr.File(label="Cohort CSV File", file_types=[".csv"])
                # --- [ELIMINADO]: El CheckboxGroup para seleccionar enfermedades ---
                run_cohort_btn = gr.Button("Run Universal Analysis", variant="primary")
            with gr.Column(scale=2):
                gr.Markdown("### 2. Differential Diagnosis Report")
                cohort_summary_display = gr.HTML(label="Cohort Summary")
                cohort_result_table = gr.DataFrame(label="Patient-level Probabilities", wrap=True, height=500)

    with gr.Tab("Single Case Analysis (Disabled)"):
        gr.Markdown("## Single Case Analysis\nThis feature is temporarily disabled and will be refactored to use the new universal diagnosis engine.")
    
    # --- [CAMBIO]: La llamada a la función ya no necesita el input de los checkboxes ---
    run_cohort_btn.click(fn=run_cohort_analysis_ui, inputs=[cohort_csv_input], outputs=[cohort_result_table, cohort_summary_display])

if __name__ == "__main__":
    app.launch()
