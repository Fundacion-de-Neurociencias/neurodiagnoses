# app.py v3.1 - The Clinical Differential Diagnosis Hub
import gradio as gr
from pathlib import Path
import pandas as pd
from unified_orchestrator import run_full_pipeline
from tools.bayesian_engine.core import BayesianEngine

def get_available_evidence():
    # (Lógica sin cambios)
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
    
    patient_data = {
        "axis1": [axis1_evidence] if axis1_evidence else [], 
        "axis2": axis2_evidence, "axis3_phenotype": axis3_pheno_evidence, "axis3_imaging": {}
    }
    img_regions = get_available_evidence()[3]
    for i, region in enumerate(img_regions):
        if imaging_values[i]: patient_data["axis3_imaging"][f"Left_{region}_Volume"] = imaging_values[i]

    results = run_full_pipeline(patient_id=subject_id, patient_data=patient_data, diseases_to_evaluate=diseases_to_evaluate, initial_prior=initial_prior)
    
    # --- [LÓGICA MEJORADA]: Construir un informe HTML ---
    html = "<h3>Differential Diagnosis Report</h3>"
    html += "<table style='width:100%; border-collapse: collapse;'>"
    html += "<tr style='background-color:#f2f2f2;'><th>Diagnosis</th><th>Probability</th><th>95% Credibility Interval</th><th>Key Supporting Evidence</th></tr>"
    
    for res in results.get('differential_diagnosis', []):
        prob_pct = f"{res['posterior_probability']:.1%}"
        ci = f"[{res['credibility_interval'][0]:.1%} - {res['credibility_interval'][1]:.1%}]"
        
        # Formatear la pista de auditoría como una lista de viñetas
        trail_items = "".join(f"<li style='font-size: 0.9em; margin-left: -20px;'>{item.split(']')[1].strip()}</li>" for item in res['evidence_trail'])
        trail_html = f"<ul style='padding-left: 20px;'>{trail_items}</ul>" if trail_items else "No specific evidence found."

        html += f"<tr style='border-bottom: 1px solid #ddd;'><td style='padding: 8px;'><b>{res['disease']}</b></td><td style='padding: 8px; font-weight:bold; font-size: 1.2em;'>{prob_pct}</td><td style='padding: 8px;'>{ci}</td><td style='padding: 8px;'>{trail_html}</td></tr>"
        
    html += "</table>"
    return html

# --- Construcción de la Interfaz ---
with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    # ... (El resto de la UI no cambia, solo el componente de salida)
    gr.Markdown("# Neurodiagnoses: The Differential Diagnosis Hub"); gr.Markdown("---"); gr.Markdown("⚠️ **Research Use Only Disclaimer**...")
    AVAILABLE_AXIS1, AVAILABLE_AXIS2, AVAILABLE_AXIS3_PHENO, AVAILABLE_AXIS3_IMG = get_available_evidence()
    with gr.Tab("Single Case Analysis"):
        with gr.Row():
            with gr.Column(scale=2):
                # ... (Todos los inputs se quedan igual)
                run_btn = gr.Button("Run Differential Diagnosis", variant="primary")
            with gr.Column(scale=3):
                gr.Markdown("### 2. Diagnostic Report")
                # --- [MEJORA]: La salida ahora es un componente HTML ---
                result_display = gr.HTML(label="Differential Diagnosis Table")
        
        all_inputs = [subject_id_input, clinical_suspicion_radio, diseases_checkboxes, axis1_dropdown, axis2_checkboxes, axis3_pheno_checkboxes] + imaging_inputs
        run_btn.click(fn=run_differential_diagnosis_ui, inputs=all_inputs, outputs=[result_display])

if __name__ == "__main__":
    app.launch()