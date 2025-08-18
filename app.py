import sys
import os
# --- [CORRECCIÓN CLAVE]: Añadir el directorio actual a la ruta de Python ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# -------------------------------------------------------------------------

import gradio as gr
from pathlib import Path
# --- [CORRECCIÓN CLAVE]: Importar desde el fichero correcto ---
from unified_orchestrator import run_full_pipeline 
from tools.bayesian_engine.core import BayesianEngine

# (El resto del fichero app.py se mantiene igual)

def get_available_evidence():
    engine = BayesianEngine(
        axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
        axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
        axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv")
    )
    axis1 = sorted(engine.axis1_df['biomarker_name'].unique().tolist())
    axis2 = sorted(engine.axis2_df['biomarker_name'].unique().tolist())
    axis3_all = engine.axis3_df['biomarker_name'].unique()
    axis3_pheno = sorted([b for b in axis3_all if 'Volume' not in b])
    axis3_img = sorted(list(set([name.replace('Left_', '').replace('Right_', '') for name in axis3_all if 'Volume' in name])))
    return axis1, axis2, axis3_pheno, axis3_img

def run_differential_diagnosis_ui(subject_id, clinical_suspicion, diseases_to_evaluate, axis1_evidence, axis2_evidence, axis3_pheno_evidence, *imaging_values):
    if not diseases_to_evaluate: raise gr.Error("Please select at least one diagnosis to evaluate.")
    prior_map = {"None / Unsure": 0.05, "Suspected AD": 0.30, "Suspected LBD": 0.15, "Suspected FTD": 0.15}
    initial_prior = prior_map.get(clinical_suspicion, 0.05)
    
    patient_data = {"axis1": [axis1_evidence] if axis1_evidence else [], "axis2": axis2_evidence, "axis3_phenotype": axis3_pheno_evidence, "axis3_imaging": {}}
    img_regions = get_available_evidence()[3]
    for i, region in enumerate(img_regions):
        if imaging_values[i]: patient_data["axis3_imaging"][f"Left_{region}_Volume"] = imaging_values[i]

    results = run_full_pipeline(patient_id=subject_id, patient_data=patient_data, diseases_to_evaluate=diseases_to_evaluate, initial_prior=initial_prior)
    
    html = "<h3>Differential Diagnosis Report</h3>"
    html += "<table style='width:100%; border-collapse: collapse; font-family: sans-serif;'>"
    html += "<tr style='background-color:#f0f0f0; border-bottom: 2px solid #ccc;'><th style='padding: 10px; text-align: left;'>Diagnosis</th><th style='padding: 10px;'>Probability</th><th style='padding: 10px;'>95% Credibility Interval</th><th style='padding: 10px; text-align: left;'>Key Supporting Evidence</th></tr>"
    
    for res in results.get('differential_diagnosis', []):
        prob_pct = f"{res['posterior_probability']:.1%}"
        ci = f"[{res['credibility_interval'][0]:.1%} - {res['credibility_interval'][1]:.1%}]"
        
        trail_items = "".join(f"<li style='margin-bottom: 8px; font-size: 0.9em;'>{item}</li>" for item in res['evidence_trail'])
        trail_html = f"<ul style='padding-left: 20px; margin: 0;'>{trail_items}</ul>" if trail_items else "<p>No specific evidence found for this hypothesis.</p>"

        html += f"<tr style='border-bottom: 1px solid #eee;'><td style='padding: 8px; font-weight:bold;'>{res['disease']}</td><td style='padding: 8px; font-weight:bold; font-size: 1.3em; text-align:center;'>{prob_pct}</td><td style='padding: 8px; text-align:center;'>{ci}</td><td style='padding: 8px;'>{trail_html}</td></tr>"
        
    html += "</table>"
    return html

with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    gr.Markdown("# Neurodiagnoses: The Differential Diagnosis Hub"); gr.Markdown("---"); gr.Markdown("⚠️ **Research Use Only Disclaimer**...")
    AVAILABLE_AXIS1, AVAILABLE_AXIS2, AVAILABLE_AXIS3_PHENO, AVAILABLE_AXIS3_IMG = get_available_evidence()
    with gr.Tab("Single Case Analysis"):
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 1. Define Case & Hypotheses")
                subject_id_input = gr.Textbox(label="Subject ID", value="ND_DiffDx_001")
                clinical_suspicion_radio = gr.Radio(["None / Unsure", "Suspected AD", "Suspected LBD", "Suspected FTD"], label="Initial Clinical Suspicion", value="None / Unsure")
                diseases_checkboxes = gr.CheckboxGroup(choices=["Alzheimer's Disease", "Parkinson's Disease", "Lewy Body Dementia", "Frontotemporal Dementia"], label="Evaluate for (Differential Diagnosis)", value=["Alzheimer's Disease", "Frontotemporal Dementia"])
                
                with gr.Accordion("Axis 1: Genetics", open=False): axis1_dropdown = gr.Dropdown(choices=AVAILABLE_AXIS1, label="Genetic Variant", filterable=True)
                with gr.Accordion("Axis 2: Molecular", open=False): axis2_checkboxes = gr.CheckboxGroup(choices=AVAILABLE_AXIS2, label="Positive Biomarkers")
                with gr.Accordion("Axis 3: Phenotype", open=True):
                    gr.Markdown("**Clinical Signs & Criteria**"); axis3_pheno_checkboxes = gr.CheckboxGroup(choices=AVAILABLE_AXIS3_PHENO, label="Positive Signs / Criteria Met")
                    gr.Markdown("**Neuroimaging (Volumes in mm³)**"); imaging_inputs = [gr.Number(label=f"Left {region}") for region in AVAILABLE_AXIS3_IMG]
                run_btn = gr.Button("Run Differential Diagnosis", variant="primary")
            with gr.Column(scale=3):
                gr.Markdown("### 2. Diagnostic Report")
                result_display = gr.HTML(label="Differential Diagnosis Table")
    
    all_inputs = [subject_id_input, clinical_suspicion_radio, diseases_checkboxes, axis1_dropdown, axis2_checkboxes, axis3_pheno_checkboxes] + imaging_inputs
    run_btn.click(fn=run_differential_diagnosis_ui, inputs=all_inputs, outputs=[result_display])

if __name__ == "__main__":
    app.launch()
