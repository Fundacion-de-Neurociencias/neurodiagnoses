import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import gradio as gr
from pathlib import Path
import pandas as pd
# --- [CAMBIO]: Importamos las dos funciones del orquestador ---
from unified_orchestrator import run_single_case_pipeline, run_cohort_pipeline
from tools.bayesian_engine.core import BayesianEngine

# Lógica de la App (sin cambios en get_available_evidence)
def get_available_evidence():
    engine = BayesianEngine(
        axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
        axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
        axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv")
    )
    # ... código sin cambios ...
    axis1 = sorted(engine.axis1_df['biomarker_name'].unique().tolist())
    axis2 = sorted(engine.axis2_df['biomarker_name'].unique().tolist())
    axis3_all = engine.axis3_df['biomarker_name'].unique()
    axis3_pheno = sorted([b for b in axis3_all if 'Volume' not in b])
    axis3_img = sorted(list(set([name.replace('Left_', '').replace('Right_', '') for name in axis3_all if 'Volume' in name])))
    return axis1, axis2, axis3_pheno, axis3_img

# --- [CAMBIO]: La función de un solo caso ahora es un placeholder ---
def run_differential_diagnosis_ui(subject_id, clinical_suspicion, diseases_to_evaluate, axis1_evidence, axis2_evidence, axis3_pheno_evidence, *imaging_values):
    return "<h3>Single Case Analysis is temporarily disabled pending refactor for new engine. Please use Cohort Analysis tab." 

# --- [NUEVA FUNCIÓN REAL]: Lógica para el análisis de cohortes ---
def run_cohort_analysis_ui(file_obj, diseases_to_evaluate):
    if file_obj is None:
        return None, "Please upload a CSV file to begin analysis."
    if not diseases_to_evaluate:
        raise gr.Error("Please select at least one diagnosis to evaluate.")

    # El prior se simplifica para el análisis de cohorte por ahora
    initial_prior = 0.10 
    
    results_df = run_cohort_pipeline(
        cohort_csv_path=file_obj.name,
        diseases_to_evaluate=diseases_to_evaluate,
        initial_prior=initial_prior
    )

    # Calcular insights de la cohorte
    primary_disease = diseases_to_evaluate[0].replace(" ", "_").replace('',"")
    prob_col = f'Prob_{primary_disease.replace(" ", "_").replace('',"")}'
    
    if prob_col in results_df.columns:
        high_risk_patients = results_df[results_df[prob_col] > 0.80]
        num_high_risk = len(high_risk_patients)
        total_patients = len(results_df)
        summary_html = f"<h4>Cohort Analysis Summary:</h4>"
        summary_html += f"<ul><li><b>{total_patients}</b> patients analyzed.</li>"
        summary_html += f"<li><b>{num_high_risk} ({num_high_risk/total_patients:.1%})</b> classified as high-probability (>80%) for {diseases_to_evaluate[0]}.</li></ul>"
    else:
        summary_html = f"<h4>Analysis Complete</h4><p>Results generated without summary statistics.</p>"

    return results_df, summary_html

# --- Construcción de la Interfaz ---
with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    gr.Markdown("# Neurodiagnoses: The AI-Powered Diagnostic Hub"); gr.Markdown("---"); gr.Markdown("⚠️ **Research Use Only Disclaimer**...")
    AVAILABLE_AXIS1, AVAILABLE_AXIS2, AVAILABLE_AXIS3_PHENO, AVAILABLE_AXIS3_IMG = get_available_evidence()
    
    with gr.Tab("Cohort Analysis"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 1. Upload & Configure")
                gr.Markdown("Upload a CSV file with patient data. The first row must be the header with biomarker names.")
                cohort_csv_input = gr.File(label="Cohort CSV File", file_types=[ ".csv"])
                diseases_cohort_checkboxes = gr.CheckboxGroup(choices=["Alzheimer's Disease", "Parkinson's Disease", "Lewy Body Dementia", "Frontotemporal Dementia"], label="Evaluate for (Differential Diagnosis)", value=["Alzheimer's Disease", "Frontotemporal Dementia"])
                run_cohort_btn = gr.Button("Analyze Cohort", variant="primary")
            with gr.Column(scale=2):
                gr.Markdown("### 2. Cohort Analysis Results")
                cohort_summary_display = gr.HTML(label="Cohort Summary")
                cohort_result_table = gr.DataFrame(label="Patient-level Results", wrap=True)

    with gr.Tab("Single Case Analysis"):
        gr.Markdown("## Single Case Analysis\nThis feature is temporarily disabled and will be refactored to use the new vectorized engine.")
    
    run_cohort_btn.click(fn=run_cohort_analysis_ui, inputs=[cohort_csv_input, diseases_cohort_checkboxes], outputs=[cohort_result_table, cohort_summary_display])

if __name__ == "__main__":
    app.launch()