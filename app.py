# app.py: Definitive, research-grade Gradio frontend aligned with the Tridimensional Annotation framework.
import os
import sys

import gradio as gr
import pandas as pd

# Add project root for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the new, correct annotation engine
from tools.ml_pipelines.pipelines_axis2_molecular import Axis2MolecularPipeline
from tools.ml_pipelines.pipelines_axis3_severity_mapping import (
    Axis3SeverityMapperPipeline,
)
from tools.tridimensional_annotation.annotator import generate_tridimensional_annotation

# --- BACKEND LOGIC FOR THE INTERFACE ---


def process_single_patient(subject_id, age, sex):
    """
    Processes a single patient and returns the final tridimensional annotation.
    NOTE: Other input fields from the UI are omitted for this PoC's backend logic,
    but would be used in the real, non-mocked implementation.
    """
    print(f"--- Running Tridimensional Annotation for Subject: {subject_id} ---")

    # In a real system, we'd pre-train models. Here, we ensure they exist.
    if not os.path.exists("models/axis2_molecular_model.joblib"):
        Axis2MolecularPipeline().train_and_evaluate()
    if not os.path.exists("models/axis3_severity_model.joblib"):
        Axis3SeverityMapperPipeline().train()

    # Call the core diagnostic function from our new annotator
    final_annotation = generate_tridimensional_annotation(subject_id)

    return final_annotation


def process_cohort_file(uploaded_file):
    """
    Processes an uploaded CSV file and returns a table with the tridimensional annotation for each subject.
    """
    if uploaded_file is None:
        return None, "Please upload a file first."
    try:
        cohort_df = pd.read_csv(uploaded_file.name)
        num_subjects = len(cohort_df)
    except Exception as e:
        return None, f"Error reading file: {e}"

    results = []
    # Process the full cohort
    for i, row in cohort_df.iterrows():
        patient_id = row.get("participant_id", f"Subject_{i + 1}")
        annotation = generate_tridimensional_annotation(patient_id)
        results.append(
            {
                "Subject ID": patient_id,
                "Tridimensional Annotation": annotation,
            }
        )

    results_df = pd.DataFrame(results)
    status_message = f"Analysis complete for {num_subjects} subjects."

    return results_df, status_message


# --- GRADIO INTERFACE DEFINITION ---
with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as demo:
    gr.Markdown("#  Neurodiagnoses: The AI-Powered Diagnostic Hub")

    with gr.Tabs():
        # --- TAB 1: SINGLE-PATIENT CLINICAL REPORT ---
        with gr.TabItem("Clinical: Single-Patient Report"):
            gr.Markdown("## Interactive Tool for Individual Case Assessment")

            # For simplicity, we only use a few inputs for this demo
            subject_id_input = gr.Textbox(
                label="Subject ID (Mandatory)", value="NACC_11782"
            )
            age_input = gr.Number(label="Age (Mandatory)", value=74)
            sex_input = gr.Radio(
                label="Sex", choices=["Male", "Female"], value="Female"
            )

            run_single_button = gr.Button(
                "Generate Tridimensional Annotation", variant="primary"
            )

            gr.Markdown("---")
            gr.Markdown("### Final Diagnostic Annotation")
            single_output_report = gr.Textbox(
                label="Annotation", lines=5, interactive=False
            )

        # --- TAB 2: COHORT ANALYSIS FOR RESEARCH ---
        with gr.TabItem("Research: Cohort Analysis"):
            gr.Markdown("## Batch Processing and Analysis for Research Datasets")
            file_input = gr.File(label="Upload Patient Cohort CSV", file_types=[".csv"])
            run_cohort_button = gr.Button("Analyze Full Cohort", variant="primary")
            gr.Markdown("---")
            cohort_status_message = gr.Textbox(label="Status", interactive=False)
            cohort_output_table = gr.DataFrame(
                label="Tridimensional Annotations for Cohort", wrap=True
            )

    # --- Connect UI components to backend functions ---
    run_single_button.click(
        fn=process_single_patient,
        inputs=[subject_id_input, age_input, sex_input],
        outputs=[single_output_report],
    )
    run_cohort_button.click(
        fn=process_cohort_file,
        inputs=[file_input],
        outputs=[cohort_output_table, cohort_status_message],
    )

if __name__ == "__main__":
    print("Launching Gradio interface...")
    demo.launch()
