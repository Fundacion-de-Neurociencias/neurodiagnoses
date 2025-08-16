#!/bin/bash
set -e
set -x

echo "INFO: Building the final, tridimensional Gradio UI..."
cat <<'EOF' > app.py
# app.py
# The user-facing Gradio dashboard for the Neurodiagnoses Tridimensional 'Glass-Box' Engine.

import gradio as gr
import pandas as pd
from pathlib import Path
import json

# Import the core logic from our backend components
from unified_orchestrator import run_full_pipeline
from tools.bayesian_engine.core import BayesianEngine

# --- [OPTIMIZACIÓN]: Singleton Pattern para Carga Perezosa ---
bayesian_engine_instance = None

def get_engine():
    """Singleton factory to load the Bayesian Engine only once."""
    global bayesian_engine_instance
    if bayesian_engine_instance is None:
        print("INFO: First request received. Lazily loading Bayesian Engine and all KBs...")
        try:
            bayesian_engine_instance = BayesianEngine(
                axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
                axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
                axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv")
            )
            print("SUCCESS: Engine loaded and cached for future requests.")
        except FileNotFoundError as e:
            raise gr.Error(f"CRITICAL ERROR: A Knowledge Base file was not found. {e}")
    return bayesian_engine_instance

def get_available_evidence():
    """Gets available biomarkers from the KBs to populate the UI dynamically."""
    try:
        engine = get_engine()
        axis1 = engine.axis1_df['biomarker_name'].unique().tolist()
        axis2 = engine.axis2_df['biomarker_name'].unique().tolist()
        # Para el Eje 3, buscamos los biomarcadores únicos (habrá varios por cada uno)
        axis3 = engine.axis3_df['biomarker_name'].unique().tolist()
        return axis1, axis2, axis3
    except Exception as e:
        print(f"Error loading evidence for UI: {e}")
        return [], [], []

def run_tridimensional_diagnosis(subject_id, clinical_suspicion, axis1_evidence, axis2_evidence, hippocampus_volume):
    """Main function connecting the Gradio UI to the tridimensional backend."""
    if not subject_id:
        raise gr.Error("Please provide a Subject ID.")

    # --- [MEJORA CLÍNICA]: Mapeo de sospecha clínica a un prior numérico ---
    prior_map = {
        "None / Unsure": 0.05, # Prior bajo si no hay sospecha
        "Suspected Alzheimer's Disease": 0.30,
        "Suspected Lewy Body Dementia": 0.15,
        "Suspected Frontotemporal Dementia": 0.15
    }
    initial_prior = prior_map.get(clinical_suspicion, 0.05)

    # Construir el diccionario de datos del paciente con los 3 ejes
    patient_data = {
        "patient_id": subject_id,
        "axis1_features": {"main_snp": axis1_evidence} if axis1_evidence else {},
        "axis2_features": {biomarker: "positive" for biomarker in axis2_evidence},
        "axis3_features": {"HippocampusVolume_mm3": hippocampus_volume} if hippocampus_volume else {}
    }
    
    # Comprobar si hay al menos una pieza de evidencia objetiva
    if not patient_data["axis1_features"] and not patient_data["axis2_features"] and not patient_data["axis3_features"]:
        return None, "<p><i>Please provide at least one piece of objective evidence (Genetic, Molecular, or Imaging).</i></p>"

    try:
        results = run_full_pipeline(
            patient_id=patient_data["patient_id"],
            patient_data=patient_data,
            initial_prior=initial_prior
        )
    except Exception as e:
        raise gr.Error(f"Backend Error: {e}")

    # Formatear la salida para la UI
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
AVAILABLE_AXIS1, AVAILABLE_AXIS2, AVAILABLE_AXIS3 = get_available_evidence()
# Asumimos que el único biomarcador de imagen que tenemos ahora es el volumen del hipocampo
# Esta lógica se puede hacer más robusta en el futuro
HIPPOCAMPUS_STR = next((s for s in AVAILABLE_AXIS3 if "Hippocampus" in s), None)

with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    gr.Markdown("# Neurodiagnoses: The AI-Powered Diagnostic Hub")
    gr.Markdown("---")
    gr.Markdown("""
    **⚠️ Research Use Only Disclaimer**
    This is a developmental tool intended for research purposes only. It is not a medical device and has not been validated or approved by the FDA, EMA, or any other regulatory body. Do not use for clinical diagnosis or patient management. The user assumes all responsibility for data confidentiality and usage.
    """)

    with gr.Tab("Single Case Analysis"):
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 1. Define Case Evidence")
                subject_id_input = gr.Textbox(label="Subject ID", value="ND_Case_001")
                
                clinical_suspicion_radio = gr.Radio(
                    ["None / Unsure", "Suspected Alzheimer's Disease", "Suspected Lewy Body Dementia", "Suspected Frontotemporal Dementia"],
                    label="Initial Clinical Suspicion (Optional)", value="None / Unsure"
                )
                
                with gr.Accordion("Axis 1: Etiology (Genetics)", open=True):
                    axis1_dropdown = gr.Dropdown(choices=AVAILABLE_AXIS1, label="Genetic Variant")
                
                with gr.Accordion("Axis 2: Molecular Profile (Biomarkers)", open=True):
                    axis2_checkboxes = gr.CheckboxGroup(choices=AVAILABLE_AXIS2, label="Positive Biomarkers")
                    
                with gr.Accordion("Axis 3: Phenotype (Neuroimaging)", open=True):
                    axis3_number = gr.Number(label=f"{HIPPOCAMPUS_STR} (mm³)" if HIPPOCAMPUS_STR else "Hippocampus Volume (mm³)")

                run_btn = gr.Button("Run Tridimensional Diagnosis", variant="primary", scale=2)

            with gr.Column(scale=3):
                gr.Markdown("### 2. Diagnostic Result")
                result_display = gr.HTML(label="Posterior Probability")
                with gr.Accordion("Evidence Trail (The 'Why')", open=True, visible=True):
                    evidence_display = gr.HTML()

    with gr.Tab("Batch Cohort Analysis"):
        gr.Markdown("*(Coming Soon)*: This section will allow you to upload a CSV file with a cohort of subjects and receive a downloadable CSV with their diagnostic probabilities.")

    run_btn.click(
        fn=run_tridimensional_diagnosis,
        inputs=[subject_id_input, clinical_suspicion_radio, axis1_dropdown, axis2_checkboxes, axis3_number],
        outputs=[result_display, evidence_display]
    )

if __name__ == "__main__":
    app.launch()
EOF

# --- PASO 2: Pequeña corrección en el orquestador para que la carga perezosa sea más limpia ---
# Asegurarnos de que el motor se inicializa a través de la función get_engine
sed -i "s/bayesian_engine = get_engine()/bayesian_engine = get_engine() # Ensures lazy loading/" unified_orchestrator.py


echo "SUCCESS: The Gradio UI (app.py) has been upgraded to its final tridimensional version."
echo "Launch the definitive interface with: python app.py"