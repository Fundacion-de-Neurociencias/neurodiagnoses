cat <<'EOF' > tools/bayesian_engine/core.py
import pandas as pd
from pathlib import Path
import numpy as np
from scipy.stats import norm
class BayesianEngine:
    def __init__(self, axis1_kb_path: Path, axis2_kb_path: Path, axis3_kb_path: Path, num_simulations: int = 10000):
        self.axis1_df = self._load_knowledge_base(axis1_kb_path, "Axis 1"); self.axis2_df = self._load_knowledge_base(axis2_kb_path, "Axis 2"); self.axis3_df = self._load_knowledge_base(axis3_kb_path, "Axis 3"); self.num_simulations = num_simulations
    def _load_knowledge_base(self, kb_path: Path, axis_name: str) -> pd.DataFrame:
        if not kb_path.exists(): raise FileNotFoundError(f"{axis_name} KB not found: {kb_path}")
        df = pd.read_csv(kb_path)
        for col in ['value', 'ci_lower', 'ci_upper']:
            if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    def _get_dist_params(self, df, biomarker, disease, stat_types):
        row = df[(df['biomarker_name'] == biomarker) & (df['statistic_type'].isin(stat_types)) & (df['primary_disease'].str.contains(disease, case=False, na=False))].iloc[0]
        mean, std = row['value'], ((row['ci_upper'] - row['ci_lower']) / 4.0) if pd.notna(row['ci_upper']) else 0.1 * abs(row['value'])
        return mean, std, row.get('source_snippet', '')
    def _get_axis3_imaging_params(self, biomarker, cohort):
        mean_row = self.axis3_df[(self.axis3_df['biomarker_name'] == biomarker) & (self.axis3_df['statistic_type'] == 'distribution_mean') & (self.axis3_df['cohort_description'].str.contains(cohort))].iloc[0]
        std_row = self.axis3_df[(self.axis3_df['biomarker_name'] == biomarker) & (self.axis3_df['statistic_type'] == 'distribution_std') & (self.axis3_df['cohort_description'].str.contains(cohort))].iloc[0]
        return mean_row['value'], std_row['value']
    def update_belief_with_likelihood_ratio(self, prior, lr):
        prior_odds = prior / (1 - prior); posterior_odds = prior_odds * lr
        return posterior_odds / (1 + posterior_odds)
    def run_full_tridimensional_inference(self, patient_data: dict, disease: str, initial_prior: float):
        final_posteriors, evidence_trail = [], []
        for i in range(self.num_simulations):
            current_prob = initial_prior
            for ev_type, df, stat_types in [('axis1', self.axis1_df, ['odds_ratio']), ('axis2', self.axis2_df, ['sensitivity', 'auc']), ('axis3_phenotype', self.axis3_df, ['sensitivity', 'specificity', 'accuracy'])]:
                for biomarker in patient_data.get(ev_type, []):
                    try:
                        mean, std, snippet = self._get_dist_params(df, biomarker, disease, stat_types)
                        if i == 0: evidence_trail.append(f"[{ev_type.upper()}: {biomarker}] {snippet}")
                        if ev_type == 'axis1':
                            lr = np.clip(np.random.normal(mean, std), 0.1, 20.0)
                        else:
                            sens = np.clip(np.random.normal(mean, std), 0.01, 0.99); spec = np.clip(np.random.normal(mean*1.1, 0.05), 0.01, 0.99); lr = sens / (1 - spec)
                        current_prob = self.update_belief_with_likelihood_ratio(current_prob, lr)
                    except (IndexError, ValueError): continue
            for biomarker, value in patient_data.get('axis3_imaging', {}).items():
                try:
                    mean_d, std_d = self._get_axis3_imaging_params(biomarker, disease); mean_c, std_c = self._get_axis3_imaging_params(biomarker, 'Control')
                    if i == 0: evidence_trail.append(f"[Axis 3 Image: {biomarker}] ADNI Dataset")
                    lr = norm.pdf(value, mean_d, std_d) / norm.pdf(value, mean_c, std_c) if norm.pdf(value, mean_c, std_c) > 0 else 1
                    current_prob = self.update_belief_with_likelihood_ratio(current_prob, lr)
                except (IndexError, ValueError): continue
            final_posteriors.append(current_prob)
        mean_posterior = np.mean(final_posteriors); credibility_interval = np.percentile(final_posteriors, [2.5, 97.5])
        return mean_posterior, credibility_interval, evidence_trail
EOF

# --- Interfaz Tridimensional Final ---
cat <<'EOF' > app.py
import gradio as gr; from pathlib import Path; from unified_orchestrator import run_full_pipeline; from tools.bayesian_engine.core import BayesianEngine
bayesian_engine_instance = None
def get_engine():
    global bayesian_engine_instance
    if bayesian_engine_instance is None:
        try: bayesian_engine_instance = BayesianEngine(axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"), axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"), axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv"))
        except FileNotFoundError as e: raise gr.Error(f"CRITICAL ERROR: KB file not found. {e}")
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
    prior_map = {"None / Unsure": 0.05, "Suspected Alzheimer's Disease": 0.30, "Suspected LBD": 0.15, "Suspected FTD": 0.15}; initial_prior = prior_map.get(clinical_suspicion, 0.05)
    patient_data = {"patient_id": subject_id, "axis1": [axis1_evidence] if axis1_evidence else [], "axis2": axis2_evidence, "axis3_phenotype": axis3_pheno_evidence, "axis3_imaging": {}}
    img_regions, img_inputs = get_available_evidence()[3], imaging_values_with_hemi
    for i, region in enumerate(img_regions):
        val, hemi = img_inputs[i*2], img_inputs[i*2+1]
        if val: patient_data["axis3_imaging"][f"{hemi}_{region}_Volume"] = val
    if not any([patient_data["axis1"], patient_data["axis2"], patient_data["axis3_phenotype"], patient_data["axis3_imaging"]]): return None, "<p><i>Please provide at least one piece of objective evidence.</i></p>"
    results = run_full_pipeline(patient_id=subject_id, patient_data=patient_data, initial_prior=initial_prior)
    prob = results["bayesian_results"]["posterior_probability"]; ci = results["bayesian_results"]["credibility_interval_95"]
    result_md = f"""<div style='text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'><p style='font-size: 1.1em;'>Posterior Probability of AD</p><p style='font-size: 2.5em; font-weight: bold; margin: 0; color: #0b5ed7;'>{prob}</p><p style='font-size: 0.9em; color: #555;'>95% Credibility Interval: {ci}</p></div>"""
    trail_items = "".join(f"<li><p><code>{item}</code></p></li>" for item in results.get("evidence_trail", []))
    return result_md, f"<ol>{trail_items}</ol>"
with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    gr.Markdown("# Neurodiagnoses: The AI-Powered Diagnostic Hubn---"); gr.Markdown("⚠️ **Research Use Only Disclaimer**...")
    AVAILABLE_AXIS1, AVAILABLE_AXIS2, AVAILABLE_AXIS3_PHENO, AVAILABLE_AXIS3_IMG = get_available_evidence()
    with gr.Tab("Single Case Analysis"):
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 1. Define Case Evidence"); subject_id_input = gr.Textbox(label="Subject ID", value="ND_FullCase_001")
                clinical_suspicion_radio = gr.Radio(["None / Unsure", "Suspected Alzheimer's Disease", "Suspected LBD", "Suspected FTD"], label="Initial Clinical Suspicion", value="None / Unsure")
                with gr.Accordion("Axis 1: Etiology (Genetics)", open=False): axis1_dropdown = gr.Dropdown(choices=AVAILABLE_AXIS1, label="Genetic Variant", info=f"{len(AVAILABLE_AXIS1)} options", filterable=True)
                with gr.Accordion("Axis 2: Molecular Profile (Biomarkers)", open=False): axis2_checkboxes = gr.CheckboxGroup(choices=AVAILABLE_AXIS2, label="Positive Biomarkers")
                with gr.Accordion("Axis 3: Phenotype (Clinical & Imaging)", open=True):
                    gr.Markdown("**Clinical Signs & Criteria**"); axis3_pheno_checkboxes = gr.CheckboxGroup(choices=AVAILABLE_AXIS3_PHENO, label="Positive Signs / Criteria Met")
                    gr.Markdown("**Neuroimaging (Volumes in mm³)**"); imaging_inputs = []
                    for region in AVAILABLE_AXIS3_IMG:
                        with gr.Row(): num_input = gr.Number(label=region); hemi_input = gr.Radio(choices=["Left", "Right"], value="Left", label="Hemisphere"); imaging_inputs.extend([num_input, hemi_input])
                run_btn = gr.Button("Run Tridimensional Diagnosis", variant="primary")
            with gr.Column(scale=3):
                gr.Markdown("### 2. Diagnostic Result"); result_display = gr.HTML(label="Posterior Probability")
                with gr.Accordion("Evidence Trail (The 'Why')", open=True, visible=True): evidence_display = gr.HTML()
    with gr.Tab("Batch Cohort Analysis"): gr.Markdown("*(Coming Soon)*")
    all_inputs = [subject_id_input, clinical_suspicion_radio, axis1_dropdown, axis2_checkboxes, axis3_pheno_checkboxes] + imaging_inputs
    run_btn.click(fn=run_tridimensional_diagnosis, inputs=all_inputs, outputs=[result_display, evidence_display])
if __name__ == "__main__":
    app.launch()