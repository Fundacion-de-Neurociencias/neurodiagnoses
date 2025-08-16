# app.py
# The user-facing Gradio dashboard for the Neurodiagnoses 'Glass-Box' Engine.

import gradio as gr
import pandas as pd
from pathlib import Path
import json

# Import the core logic from our backend components
from unified_orchestrator import run_full_pipeline
from tools.bayesian_engine.core import BayesianEngine

# --- [OPTIMIZACIÓN]: Singleton Pattern para Carga Perezosa ---
# No inicializamos el motor aquí para ahorrar memoria en el arranque.
bayesian_engine_instance = None

def get_engine():
    """Singleton factory to load the Bayesian Engine only once."""
    global bayesian_engine_instance
    if bayesian_engine_instance is None:
        print("INFO: First request received. Lazily loading Bayesian Engine and KBs...")
        try:
            bayesian_engine_instance = BayesianEngine(
                axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
                axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv")
                # Add axis3_kb_path here when available
            )
            print("SUCCESS: Engine loaded and cached for future requests.")
        except FileNotFoundError as e:
            raise gr.Error(f"CRITICAL ERROR: Knowledge Base file not found. {e}")
    return bayesian_engine_instance

def get_available_evidence():
    """Gets available biomarkers from the KBs to populate the UI dynamically."""
    try:
        engine = get_engine()
        axis1 = engine.axis1_df['biomarker_name'].unique().tolist()
        axis2 = engine.axis2_df['biomarker_name'].unique().tolist()
        return axis1, axis2
    except Exception:
        return [], []

def run_bayesian_diagnosis(subject_id, prior_prob, axis1_evidence, axis2_evidence):
    """Main function connecting the Gradio UI to our backend orchestrator."""
    if not subject_id:
        raise gr.Error("Please provide a Subject ID.")
    if not axis1_evidence and not axis2_evidence:
        return None, "<p><i>Please select at least one piece of evidence.</i></p>"

    print(f"--- [Gradio App] Received request for Subject: {subject_id} ---")
    
    patient_data = {
        "patient_id": subject_id,
        "axis1_features": {"main_snp": axis1_evidence} if axis1_evidence else {},
        "axis2_features": {biomarker: "positive" for biomarker in axis2_evidence},
        "axis3_features": {} # Placeholder for Axis 3
    }
    
    try:
        results = run_full_pipeline(
            patient_id=patient_data["patient_id"],
            patient_data=patient_data,
            initial_prior=prior_prob
        )
    except Exception as e:
        raise gr.Error(f"Backend Error: {e}")

    # Format the rich output for display
    prob = results["axis2_results"]["posterior_probability"]
    ci = results["axis2_results"]["credibility_interval_95"]
    result_md = f"""
    <div style="text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
        <p style="font-size: 1.1em; margin-bottom: 5px;">Posterior Probability of Alzheimer's Disease</p>
        <p style="font-size: 2.5em; font-weight: bold; margin: 0; color: #0b5ed7;">{prob}</p>
        <p style="font-size: 0.9em; color: #555;">95% Credibility Interval: {ci}</p>
    </div>
    """
    
    trail = results.get("evidence_trail", [])
    trail_items = "".join(f"<li><p><code>{item}</code></p></li>" for item in trail)
    trail_md = f"<ol>{trail_items}</ol>" if trail_items else "No evidence trail was generated."
        
    return result_md, trail_md

# --- Gradio Interface Definition ---
# Load evidence choices once when the script starts
AVAILABLE_AXIS1, AVAILABLE_AXIS2 = get_available_evidence()

with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    gr.Markdown("# Neurodiagnoses: The AI-Powered Diagnostic Hub")
    gr.Markdown("""
    **⚠️ Research Use Only Disclaimer**
    This is a developmental tool intended for research purposes only. It is not a medical device and has not been validated or approved by the FDA, EMA, or any other regulatory body. Do not use for clinical diagnosis or patient management. The user assumes all responsibility for data confidentiality and usage.
    """)

    with gr.Tab("Single Case Analysis"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 1. Define Case Evidence")
                subject_id_input = gr.Textbox(label="Subject ID", value="ND_Case_001")
                prior_slider = gr.Slider(minimum=0.01, maximum=1.0, step=0.01, value=0.20, label="Initial Clinical Suspicion (Prior)")
                
                with gr.Accordion("Axis 1: Etiology (Genetics)", open=True):
                    axis1_dropdown = gr.Dropdown(choices=AVAILABLE_AXIS1, label="Genetic Variant")
                
                with gr.Accordion("Axis 2: Molecular Profile (Biomarkers)", open=True):
                    axis2_checkboxes = gr.CheckboxGroup(choices=AVAILABLE_AXIS2, label="Positive Biomarkers")
                
                run_btn = gr.Button("Run Diagnosis", variant="primary", scale=2)

            with gr.Column(scale=2):
                gr.Markdown("### 2. Diagnostic Result")
                result_display = gr.HTML(label="Posterior Probability")
                with gr.Accordion("Evidence Trail (The 'Why')", open=True):
                    evidence_display = gr.HTML()

    with gr.Tab("Batch Cohort Analysis"):
        gr.Markdown("*(Coming Soon)*: This section will allow you to upload a CSV file with a cohort of subjects and receive a downloadable CSV with their diagnostic probabilities.")


    # --- Event Handling ---
    run_btn.click(
        fn=run_bayesian_diagnosis,
        inputs=[subject_id_input, prior_slider, axis1_dropdown, axis2_checkboxes],
        outputs=[result_display, evidence_display]
    )

if __name__ == "__main__":
    app.launch()