import sys
import os
sys.path.append(os.getcwd())
print("app.py sys.path:", sys.path)
# app.py v2.2 - Tridimensional Hub con Ingestión Curada
import gradio as gr
from pathlib import Path
import re # Import re a nivel global

# Importar funciones y clases necesarias
from unified_orchestrator import run_full_pipeline
from tools.bayesian_engine.core import BayesianEngine
from workflows.knowledge_ingestion.orchestrator import KnowledgeOrchestrator, ingest_from_url

# --- Lógica de Singleton y Carga de Datos ---
bayesian_engine_instance = None
knowledge_orchestrator_instance = None

def get_engine():
    global bayesian_engine_instance
    if bayesian_engine_instance is None:
        try:
            bayesian_engine_instance = BayesianEngine(
                axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
                axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
                axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv")
            )
        except FileNotFoundError as e: raise gr.Error(f"CRITICAL ERROR: KB file not found. {e}")
    return bayesian_engine_instance

def get_orchestrator():
    global knowledge_orchestrator_instance
    if knowledge_orchestrator_instance is None:
        knowledge_orchestrator_instance = KnowledgeOrchestrator(
            topics_path="data/knowledge_base/topics.csv",
            kb_dir="data/knowledge_base"
        )
    return knowledge_orchestrator_instance

def get_available_evidence():
    engine = get_engine()
    axis1 = sorted(engine.axis1_df['biomarker_name'].unique().tolist())
    axis2 = sorted(engine.axis2_df['biomarker_name'].unique().tolist())
    axis3_all = engine.axis3_df['biomarker_name'].unique()
    axis3_pheno = sorted([b for b in axis3_all if 'Volume' not in b])
    axis3_img = sorted(list(set([name.replace('Left_', '').replace('Right_', '') for name in axis3_all if 'Volume' in name])))
    return axis1, axis2, axis3_pheno, axis3_img

# --- Funciones de Callback para la UI ---
def run_tridimensional_diagnosis(subject_id, clinical_suspicion, axis1_evidence, axis2_evidence, axis3_pheno_evidence, *imaging_values_with_hemi):
    # (Lógica sin cambios)
    prior_map = {"None / Unsure": 0.05, "Suspected Alzheimer's Disease": 0.30, "Suspected LBD": 0.15, "Suspected FTD": 0.15}
    initial_prior = prior_map.get(clinical_suspicion, 0.05)
    patient_data = {"patient_id": subject_id,"axis1_features": {"main_snp": axis1_evidence} if axis1_evidence else {},"axis2_features": {biomarker: "positive" for biomarker in axis2_evidence},"axis3_features": {biomarker: "positive" for biomarker in axis3_pheno_evidence}}
    img_regions, img_inputs = get_available_evidence()[3], imaging_values_with_hemi
    for i, region in enumerate(img_regions):
        val, hemi = img_inputs[i*2], img_inputs[i*2+1]
        if val: patient_data["axis3_features"][f"{hemi}_{region}_Volume"] = val
    if not any(patient_data[key] for key in ["axis1_features", "axis2_features", "axis3_features"]): return None, "<p><i>Please provide at least one piece of objective evidence.</i></p>"
    results = run_full_pipeline(patient_id=subject_id, patient_data=patient_data, initial_prior=initial_prior)
    prob = results["bayesian_results"]["posterior_probability"]; ci = results["bayesian_results"]["credibility_interval_95"]
    result_md = f"""<div style='text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'><p style='font-size: 1.1em;'>Posterior Probability of AD</p><p style='font-size: 2.5em; font-weight: bold; margin: 0; color: #0b5ed7;'>{prob}</p><p style='font-size: 0.9em; color: #555;'>95% Credibility Interval: {ci}</p></div>"""
    trail_items = "".join(f"<li><p><code>{item}</code></p></li>" for item in results.get("evidence_trail", []))
    return result_md, f"<ol>{trail_items}</ol>"

def handle_curated_ingestion(url_or_doi):
    if not url_or_doi: return "<p style='color:red;'>Please provide a URL or DOI.</p>"
    orchestrator = get_orchestrator()
    result_message = ingest_from_url(url_or_doi, orchestrator)
    return f"<p style='color:green;'>{result_message}</p>"

# --- Construcción de la Interfaz ---
with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    gr.Markdown("# Neurodiagnoses: The AI-Powered Diagnostic Hub")
    gr.Markdown("---"); gr.Markdown("⚠️ **Research Use Only Disclaimer**...")
    
    AVAILABLE_AXIS1, AVAILABLE_AXIS2, AVAILABLE_AXIS3_PHENO, AVAILABLE_AXIS3_IMG = get_available_evidence()

    with gr.Tab("Single Case Analysis"):
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 1. Define Case Evidence")
                subject_id_input = gr.Textbox(label="Subject ID", value="ND_FullCase_001")
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

    with gr.Tab("Curated Knowledge Ingestion"):
        gr.Markdown("## Add New Knowledge to the SystemnProvide a URL or DOI of a scientific paper. The system will attempt to read it, extract relevant data, and integrate it into the knowledge base.")
        url_input = gr.Textbox(label="URL or DOI", placeholder="e.g., https://pubmed.ncbi.nlm.nih.gov/35395825/ or 10.1186/s13024-022-00527-3")
        ingest_btn = gr.Button("Extract & Ingest Knowledge", variant="primary")
        ingestion_status = gr.HTML(label="Ingestion Status")

    all_inputs = [subject_id_input, clinical_suspicion_radio, axis1_dropdown, axis2_checkboxes, axis3_pheno_checkboxes] + imaging_inputs
    run_btn.click(fn=run_tridimensional_diagnosis, inputs=all_inputs, outputs=[result_display, evidence_display])
    ingest_btn.click(fn=handle_curated_ingestion, inputs=[url_input], outputs=[ingestion_status])

if __name__ == "__main__":
    app.launch()
