# app.py
# The user-facing Gradio dashboard for the Neurodiagnoses Bayesian Engine.
# (Optimized with Lazy Loading to fit in memory-constrained environments)

import gradio as gr
import json
from pathlib import Path

# Import the core logic from our backend components
from unified_orchestrator import run_full_pipeline
from tools.bayesian_engine.core import BayesianEngine

# --- [OPTIMIZACIÓN]: Singleton Pattern para Carga Perezosa ---
# No inicializamos el motor aquí para ahorrar memoria en el arranque.
# Lo haremos solo cuando sea necesario.
bayesian_engine_instance = None

def get_engine():
    """
    Singleton factory to load the Bayesian Engine only once when first needed.
    """
    global bayesian_engine_instance
    if bayesian_engine_instance is None:
        print("INFO: First request received. Lazily loading Bayesian Engine and Knowledge Bases...")
        try:
            bayesian_engine_instance = BayesianEngine(
                axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
                axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv")
            )
            print("SUCCESS: Engine loaded and cached for future requests.")
        except FileNotFoundError as e:
            print(f"ERROR: Could not load Knowledge Base. {e}")
            # Devolvemos un error que se mostrará en la UI
            raise gr.Error(f"CRITICAL ERROR: Knowledge Base file not found. {e}")
    return bayesian_engine_instance

def get_available_evidence():
    """Gets the available biomarkers from the engine's KB."""
    try:
        engine = get_engine()
        axis1 = engine.axis1_df['biomarker_name'].unique().tolist()
        axis2 = engine.axis2_df['biomarker_name'].unique().tolist()
        return axis1, axis2
    except Exception:
        # Si falla la carga del motor, devolvemos listas vacías para que la UI no se rompa.
        return [], []

def run_bayesian_diagnosis(prior_prob, axis1_evidence, axis2_evidence):
    """
    The main function that connects the Gradio UI to our backend orchestrator.
    """
    if not axis1_evidence and not axis2_evidence:
        return None, "Please select at least one piece of evidence to run the diagnosis."

    print("--- [Gradio App] Received request ---")
    
    # 1. Construir el diccionario de datos del paciente
    patient_data = {
        "patient_id": "VIRTUAL_PATIENT_01",
        "axis1_features": {"main_snp": axis1_evidence} if axis1_evidence else {},
        "axis2_features": {biomarker: "positive" for biomarker in axis2_evidence},
        "axis3_features": {} # Placeholder for future use
    }
    
    # 2. Llamar al orquestador (que ahora usará nuestro motor ya cargado)
    try:
        # Nota: Ya no necesitamos pasar el motor, el orquestador lo crea por sí mismo.
        # Esto es más limpio. Actualizaremos el orquestador para que también sea lazy.
        # Por ahora, simplemente lo llamamos.
        results = run_full_pipeline(
            patient_id=patient_data["patient_id"],
            patient_data=patient_data,
            initial_prior=prior_prob
        )
    except Exception as e:
        # Envia un error visible al usuario en la interfaz de Gradio
        raise gr.Error(f"Backend Error: {e}")

    # 3. Formatear la salida para la UI
    prob = results["axis2_results"]["posterior_probability"]
    ci = results["axis2_results"]["credibility_interval_95"]
    main_result_md = f"""
    <div style="text-align: center;">
        <p style="font-size: 1.2em; margin-bottom: 5px;">Posterior Probability of Alzheimer's Disease</p>
        <p style="font-size: 3em; font-weight: bold; margin-top: 0; margin-bottom: 5px; color: #0b5ed7;">{prob}</p>
        <p style="font-size: 1em; color: #555;">95% Credibility Interval: {ci}</p>
    </div>
    """
    
    trail = results.get("evidence_trail", [])
    trail_items = "".join(f"<li><p><code>{item}</code></p></li>" for item in trail)
    evidence_trail_md = f"<ol>{trail_items}</ol>" if trail_items else "No evidence trail was generated."
        
    return main_result_md, evidence_trail_md

# --- Gradio Interface Definition ---
with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses Glass-Box Engine") as app:
    gr.Markdown("# Neurodiagnoses: The Glass-Box Diagnostic Engine")
    gr.Markdown("Construct a virtual patient by selecting evidence. The Bayesian Engine will calculate the probability of Alzheimer's Disease and show the evidence it used.")

    # Obtenemos las evidencias disponibles una sola vez al cargar la UI
    AVAILABLE_AXIS1, AVAILABLE_AXIS2 = get_available_evidence()

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 1. Define Patient Evidence")
            prior_slider = gr.Slider(minimum=0.01, maximum=1.0, step=0.01, value=0.20, label="Initial Clinical Suspicion (Prior)")
            axis1_dropdown = gr.Dropdown(choices=AVAILABLE_AXIS1, label="Axis 1: Genetic Evidence")
            axis2_checkboxes = gr.CheckboxGroup(choices=AVAILABLE_AXIS2, label="Axis 2: Molecular Biomarkers (Positive)")
            run_btn = gr.Button("Run Diagnosis", variant="primary")
        with gr.Column(scale=2):
            gr.Markdown("### 2. Diagnostic Result")
            result_display = gr.HTML(label="Posterior Probability")
            with gr.Accordion("Show Evidence Trail (The 'Why')", open=False):
                evidence_display = gr.HTML()

    run_btn.click(
        fn=run_bayesian_diagnosis,
        inputs=[prior_slider, axis1_dropdown, axis2_checkboxes],
        outputs=[result_display, evidence_display]
    )

if __name__ == "__main__":
    app.launch()
