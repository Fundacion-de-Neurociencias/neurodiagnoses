import gradio as gr
from pathlib import Path
import pandas as pd
from unified_orchestrator import run_full_pipeline
from tools.bayesian_engine.core import BayesianEngine

# --- Lógica de la App ---
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
        if imaging_values[i]: patient_data["axis3_imaging"][f"Left_{region}_Volume"] = imaging_values[i] # Simplificado a solo izquierdo por ahora
    
    results = run_full_pipeline(patient_id=subject_id, patient_data=patient_data, diseases_to_evaluate=diseases_to_evaluate, initial_prior=initial_prior)
    
    # Formatear la salida como un DataFrame de Pandas para la tabla de Gradio
    df_data = []
    for res in results.get('differential_diagnosis', []):
        prob_pct = f"{res['posterior_probability']:.2%}"
        ci = f"[{res['credibility_interval'][0]:.2%} - {res['credibility_interval'][1]:.2%}]"
        trail_html = "<ul>" + "".join(f"<li>{item}</li>" for item in res['evidence_trail']) + "</ul>"
        df_data.append([res['disease'], prob_pct, ci, trail_html])
    
    return pd.DataFrame(df_data, columns=["Diagnosis", "Probability", "95% CI", "Supporting Evidence"])

# --- Construcción de la Interfaz ---
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
                result_display = gr.DataFrame(headers=["Diagnosis", "Probability", "95% CI", "Supporting Evidence"], datatype=["str", "str", "str", "markdown"], wrap=True)
    
    all_inputs = [subject_id_input, clinical_suspicion_radio, diseases_checkboxes, axis1_dropdown, axis2_checkboxes, axis3_pheno_checkboxes] + imaging_inputs
    run_btn.click(fn=run_differential_diagnosis_ui, inputs=all_inputs, outputs=[result_display])

if __name__ == "__main__":
    app.launch()