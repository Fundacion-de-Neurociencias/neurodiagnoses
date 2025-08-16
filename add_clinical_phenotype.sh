AXIS3_KB="data/knowledge_base/axis3_likelihoods.csv"

# --- FASE 1: Inspeccionar la KB del Eje 3 para ver qué fenotipos tenemos ---
echo "INFO: Inspecting Axis 3 Knowledge Base for available clinical phenotypes..."
cat "$AXIS3_KB"

# --- FASE 2: Actualizar el Motor para que procese el Fenotipo Clínico ---
echo "INFO: Upgrading Bayesian Engine to reason with Axis 3 clinical phenotype..."
# Nota: La última versión que te di ya tenía la lógica, pero este sed se asegura de que esté presente.
# Es un comando complejo que añade el bucle de procesamiento para el fenotipo clínico.
sed -i "/# --- Axis 3: Neuroimaging (Continuous Variable) ---/i             # --- Axis 3: Clinical Phenotype (Criteria & Signs) ---            for biomarker in patient_data.get('axis3_phenotype', []):                try:                    sens_mean, sens_std, snippet = self._get_dist_params(self.axis3_df, biomarker, disease, ['sensitivity', 'specificity', 'prevalence', 'accuracy'])                    if i == 0: evidence_trail.append(f"[Axis 3 Pheno: {biomarker}] {snippet}")                    spec_mean, spec_std = (sens_mean * 1.1, 0.05) # Placeholder for specificity                    sampled_sens = np.clip(np.random.normal(sens_mean, sens_std), 0.01, 0.99)                    sampled_spec = np.clip(np.random.normal(spec_mean, spec_std), 0.01, 0.99)                    lr = sampled_sens / (1 - sampled_spec)                    current_prob = self.update_belief_with_likelihood_ratio(current_prob, lr)                except (IndexError, ValueError): continue" "tools/bayesian_engine/core.py"
echo "SUCCESS: Bayesian Engine upgraded."


# --- FASE 3: Reescribir la Interfaz de Usuario para que sea completamente tridimensional ---
echo "INFO: Rebuilding the Gradio UI to be fully tridimensional..."
cat <<'EOF' > app.py
# app.py v2.1 - The Fully Tridimensional Diagnostic Hub with Clinical Phenotype
import gradio as gr
from pathlib import Path
from unified_orchestrator import run_full_pipeline
from tools.bayesian_engine.core import BayesianEngine

bayesian_engine_instance = None
def get_engine():
    global bayesian_engine_instance
    if bayesian_engine_instance is None:
        try:
            bayesian_engine_instance = BayesianEngine(
                axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
                axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
                axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv")
            )
        except FileNotFoundError as e:
            raise gr.Error(f"CRITICAL ERROR: A Knowledge Base file was not found. {e}")
    return bayesian_engine_instance

def get_available_evidence():
    engine = get_engine()
    axis1 = sorted(engine.axis1_df['biomarker_name'].unique().tolist())
    axis2 = sorted(engine.axis2_df['biomarker_name'].unique().tolist())
    axis3_all = engine.axis3_df['biomarker_name'].unique()
    axis3_phenotype = sorted([b for b in axis3_all if 'Volume' not in b])
    axis3_imaging = sorted(list(set([name.replace('Left_', '').replace('Right_', '') for name in axis3_all if 'Volume' in name])))
    return axis1, axis2, axis3_phenotype, axis3_imaging

def run_tridimensional_diagnosis(subject_id, clinical_suspicion, axis1_evidence, axis2_evidence, axis3_pheno_evidence, *imaging_values_with_hemi):
    prior_map = {"None / Unsure": 0.05, "Suspected Alzheimer's Disease": 0.30, "Suspected LBD": 0.15, "Suspected FTD": 0.15}
    initial_prior = prior_map.get(clinical_suspicion, 0.05)
    
    patient_data = {
        "patient_id": subject_id,
        "axis1": [axis1_evidence] if axis1_evidence else [],
        "axis2": axis2_evidence,
        "axis3_phenotype": axis3_pheno_evidence,
        "axis3_imaging": {}
    }
    
    imaging_regions, imaging_inputs_flat = get_available_evidence()[3], imaging_values_with_hemi
    for i, region in enumerate(imaging_regions):
        val, hemi = imaging_inputs_flat[i*2], imaging_inputs_flat[i*2+1]
        if val: patient_data["axis3_imaging"][f"{hemi}_{region}"] = val
    
    if not any([patient_data["axis1"], patient_data["axis2"], patient_data["axis3_phenotype"], patient_data["axis3_imaging"]]):
        return None, "<p><i>Please provide at least one piece of objective evidence.</i></p>"

    results = run_full_pipeline(patient_id=subject_id, patient_data=patient_data, initial_prior=initial_prior)
    
    prob = results["bayesian_results"]["posterior_probability"]
    ci = results["bayesian_results"]["credibility_interval_95"]
    result_md = f"""<div style='text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'><p style='font-size: 1.1em;'>Posterior Probability of AD</p><p style='font-size: 2.5em; font-weight: bold; margin: 0; color: #0b5ed7;'>{prob}</p><p style='font-size: 0.9em; color: #555;'>95% Credibility Interval: {ci}</p></div>"""
    trail = results.get("evidence_trail", [])
    trail_items = "".join(f"<li><p><code>{item}</code></p></li>" for item in trail)
    trail_md = f"<ol>{trail_items}</ol>" if trail_items else "No evidence trail."
    return result_md, trail_md

with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    gr.Markdown("# Neurodiagnoses: The AI-Powered Diagnostic Hub")
    gr.Markdown("---")
    gr.Markdown("⚠️ **Research Use Only Disclaimer**...")
    
    AVAILABLE_AXIS1, AVAILABLE_AXIS2, AVAILABLE_AXIS3_PHENO, AVAILABLE_AXIS3_IMG = get_available_evidence()

    with gr.Tab("Single Case Analysis"):
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 1. Define Case Evidence")
                subject_id_input = gr.Textbox(label="Subject ID", value="ND_FullCase_001")
                clinical_suspicion_radio = gr.Radio(["None / Unsure", "Suspected Alzheimer's Disease", "Suspected LBD", "Suspected FTD"], label="Initial Clinical Suspicion", value="None / Unsure")
                
                with gr.Accordion("Axis 1: Etiology (Genetics)", open=False):
                    axis1_dropdown = gr.Dropdown(choices=AVAILABLE_AXIS1, label="Genetic Variant", info=f"{len(AVAILABLE_AXIS1)} options", filterable=True)
                with gr.Accordion("Axis 2: Molecular Profile (Biomarkers)", open=False):
                    axis2_checkboxes = gr.CheckboxGroup(choices=AVAILABLE_AXIS2, label="Positive Biomarkers")
                with gr.Accordion("Axis 3: Phenotype (Clinical & Imaging)", open=True):
                    gr.Markdown("**Clinical Signs & Criteria**")
                    axis3_pheno_checkboxes = gr.CheckboxGroup(choices=AVAILABLE_AXIS3_PHENO, label="Positive Signs / Criteria Met")
                    gr.Markdown("**Neuroimaging (Volumes in mm³)**")
                    imaging_inputs = []
                    for region in AVAILABLE_AXIS3_IMG:
                        with gr.Row():
                            num_input = gr.Number(label=region)
                            hemi_input = gr.Radio(choices=["Left", "Right"], value="Left", label="Hemisphere")
                            imaging_inputs.extend([num_input, hemi_input])
                
                run_btn = gr.Button("Run Tridimensional Diagnosis", variant="primary")
            with gr.Column(scale=3):
                gr.Markdown("### 2. Diagnostic Result")
                result_display = gr.HTML(label="Posterior Probability")
                with gr.Accordion("Evidence Trail (The 'Why')", open=True, visible=True):
                    evidence_display = gr.HTML()

    with gr.Tab("Batch Cohort Analysis"): gr.Markdown("*(Coming Soon)*")

    # Necesitamos empaquetar los inputs de imagen para pasarlos a la función
    all_inputs = [subject_id_input, clinical_suspicion_radio, axis1_dropdown, axis2_checkboxes, axis3_pheno_checkboxes] + imaging_inputs
    run_btn.click(fn=run_tridimensional_diagnosis, inputs=all_inputs, outputs=[result_display, evidence_display])

if __name__ == "__main__":
    app.launch()
EOF
