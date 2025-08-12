# app.py: Main script for the Gradio-based interactive frontend.
import gradio as gr
import json
import pandas as pd
import random

# Import the core logic from our unified orchestrator
from unified_orchestrator import run_full_diagnosis_for_api

def process_patient_and_diagnose(
    # Input fields from the UI will be passed as arguments here
    age, sex, apoe4, mmse, ptau, abeta, nfl, gfap, # Clinical & Biomarker
    hippocampal_vol, cortical_thickness, ventricular_vol # Neuroimaging
    ):
    """
    This function is the bridge between the Gradio UI and our backend logic.
    It takes the user inputs, formats them, calls the orchestrator, and formats the output.
    """
    print("--- Received data from Gradio interface. Running diagnosis... ---")
    
    # --- Data Formatting (Placeholder) ---
    # In a real application, we would use these inputs to create the patient dataframes.
    # For this PoC, we'll continue to use the orchestrator's internal simulation,
    # but this shows how the connection is made.
    
    # We use a dummy patient_id for the simulation
    dummy_patient_id = random.randint(1000, 9999)
    
    # Call the core diagnostic function
    final_report = run_full_diagnosis_for_api(dummy_patient_id)
    
    # --- Format the Output for Gradio ---
    # We will return both a formatted text summary and a JSON object for clarity.
    
    # 1. Tridimensional Summary (Text)
    summary_text = final_report.get("tridimensional_summary", "Summary not available.")
    
    # 2. Probabilistic Diagnosis (Formatted Text)
    probabilities = final_report.get("final_probabilistic_diagnosis", [])
    prob_text = "\n".join([f"- {disease}: {probability:.2%}" for disease, probability in probabilities])
    
    full_text_report = f"## Tridimensional Summary\n{summary_text}\n\n## Probabilistic Diagnosis\n{prob_text}"
    
    # 3. Full JSON object for detailed view
    json_report = json.dumps(final_report, indent=2)
    
    return full_text_report, json_report

# --- Define the Gradio Interface ---
with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as demo:
    gr.Markdown("#  Neurodiagnoses: Interactive Diagnostic Tool")
    gr.Markdown("Enter patient data across the three diagnostic axes and click 'Run Diagnosis' to get a real-time probabilistic report from the AI models.")

    with gr.Tabs():
        with gr.TabItem("Axis 1 & 2: Clinical & Molecular"):
            with gr.Row():
                age = gr.Number(label="Age", value=72)
                sex = gr.Radio(label="Sex", choices=["Male", "Female"], value="Male")
                apoe4 = gr.Slider(label="APOE4 Alleles", minimum=0, maximum=2, step=1, value=1)
            with gr.Row():
                mmse = gr.Slider(label="MMSE Score", minimum=0, maximum=30, step=1, value=24)
                ptau = gr.Number(label="pTau (pg/mL)", value=45.0)
                abeta = gr.Number(label="Abeta42 (pg/mL)", value=850.0)
            with gr.Row():
                nfl = gr.Number(label="NfL (pg/mL)", value=20.0)
                gfap = gr.Number(label="GFAP (pg/mL)", value=1.5)

        with gr.TabItem("Axis 3: Neuroimaging"):
            hippocampal_vol = gr.Number(label="Hippocampal Volume (mm^3)", value=3200)
            cortical_thickness = gr.Number(label="Avg. Cortical Thickness (mm)", value=2.1)
            ventricular_vol = gr.Number(label="Ventricular Volume (cm^3)", value=25)
            
    # The button to trigger the diagnosis
    run_button = gr.Button("Run Diagnosis", variant="primary")
    
    # The output fields
    gr.Markdown("---")
    gr.Markdown("##  Diagnostic Report")
    output_summary = gr.Markdown(label="Formatted Report")
    output_json = gr.JSON(label="Full JSON Output")

    # Connect the button to the function
    run_button.click(
        fn=process_patient_and_diagnose,
        inputs=[age, sex, apoe4, mmse, ptau, abeta, nfl, gfap, hippocampal_vol, cortical_thickness, ventricular_vol],
        outputs=[output_summary, output_json]
    )

if __name__ == "__main__":
    print("Launching Gradio interface... Go to the URL provided in the logs.")
    # The 'share=True' option generates a temporary public link, useful for sharing.
    demo.launch(share=True)
