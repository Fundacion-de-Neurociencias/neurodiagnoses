# app.py: Professional, dual-purpose frontend with an Advanced Genetics section.
import gradio as gr
import pandas as pd
import json
import random
import os
import sys
from datetime import datetime

# Add project root for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Mock backend logic remains the same for UI development
def mocked_run_diagnosis(patient_data: dict):
    """Mocks the output of the unified_orchestrator based on inputs."""
    summary = f"Diagnostic report for patient {patient_data.get('patient_id', 'N/A')}. "
    genetics_summary = []
    if patient_data.get("ht_allele_1", 0) > 35 or patient_data.get("ht_allele_2", 0) > 35:
        genetics_summary.append("Huntington's Disease expansion detected in HTT gene.")
    if patient_data.get("c9orf72_allele_1", 0) > 30 or patient_data.get("c9orf72_allele_2", 0) > 30:
        genetics_summary.append("FTD/ALS expansion detected in C9orf72 gene.")
    if "Positive" in [patient_data.get("psen1_allele_1"), patient_data.get("psen1_allele_2")]:
        genetics_summary.append("Pathogenic PSEN1 variant detected.")
    
    if genetics_summary:
        summary += " ".join(genetics_summary)
    else:
        summary += "No high-penetrance genetic variants detected."

    report = {"tridimensional_summary": summary, "final_probabilistic_diagnosis": [], "input_summary": patient_data}
    return report

# --- Main processing function for the clinical tab ---
def process_single_patient(*args):
    """
    Processes a single patient from the detailed form inputs, now including advanced genetics.
    """
    # Dynamically create the dictionary of all inputs from the UI
    input_names = [
        "patient_id", "age", "sex", # Demographics
        "apoe_allele_1", "apoe_allele_2", "psen1_allele_1", "psen1_allele_2", "psen2_allele_1", "psen2_allele_2", "app_allele_1", "app_allele_2", # AD Genes
        "lrrk2_allele_1", "lrrk2_allele_2", "prkn_allele_1", "prkn_allele_2", "snca_allele_1", "snca_allele_2", # PD Genes
        "mapt_allele_1", "mapt_allele_2", "grn_allele_1", "grn_allele_2", # FTD/Tau Genes
        "c9orf72_allele_1", "c9orf72_allele_2", "ht_allele_1", "ht_allele_2", # Expansion Genes
        "atxn1_allele_1", "atxn1_allele_2", "atxn2_allele_1", "atxn2_allele_2", # Ataxia Genes
        "moca_score", "mmse_score", # Neuropsych
        "tiv", "hippocampal_vol" # Neuroimaging
    ]
    patient_data = dict(zip(input_names, args))

    # TIV Normalization Logic
    tiv = patient_data.get('tiv')
    if tiv and tiv > 0:
        if patient_data.get('hippocampal_vol'):
            patient_data['hippocampal_vol_norm'] = patient_data['hippocampal_vol'] / tiv
    elif patient_data.get('hippocampal_vol'):
        return ("### Error\nPlease provide a Total Intracranial Volume (TIV) to normalize volumetric data.", "{}", "{}")

    report = mocked_run_diagnosis(patient_data)
    summary = report.get("tridimensional_summary", "N/A")
    probs = report.get("final_probabilistic_diagnosis", [])
    prob_markdown = "### Probabilistic Diagnosis\n" + ("\n".join([f"- **{disease}:** {probability:.2%}" for disease, probability in probs]) if probs else "N/A")
    summary_markdown = f"### Tridimensional Summary\n{summary}"
    
    return summary_markdown, prob_markdown, json.dumps(report, indent=2)

# --- GRADIO INTERFACE DEFINITION ---
with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as demo:
    gr.Markdown("#  Neurodiagnoses: The AI-Powered Diagnostic Hub")
    
    with gr.Tabs():
        # --- TAB 1: SINGLE-PATIENT CLINICAL REPORT (NEW ADVANCED GENETICS) ---
        with gr.TabItem("Clinical: Single-Patient Report"):
            gr.Markdown("## Interactive Tool for Individual Case Assessment")
            gr.Markdown("Enter patient data below. **Only Age is mandatory.** All other fields are optional.")
            
            inputs_list = [] # We'll collect all input components here
            
            with gr.Accordion("Demographics", open=True):
                with gr.Row():
                    patient_id_input = gr.Textbox(label="Patient ID", value="Patient-123"); inputs_list.append(patient_id_input)
                    age_input = gr.Number(label="Age (Mandatory)", value=72); inputs_list.append(age_input)
                    sex_input = gr.Radio(label="Sex", choices=["Male", "Female"], value="Male"); inputs_list.append(sex_input)
            
            with gr.Accordion("Advanced Genetics (Optional)", open=False):
                gr.Markdown("For each gene, enter information for both alleles. For expansion variants, enter the number of repeats.")
                
                # Alzheimer's Disease Genes
                with gr.TabItem("AD-Related Genes"):
                    with gr.Row():
                        apoe_1 = gr.Dropdown(label="APOE Allele 1", choices=["e2", "e3", "e4"]); inputs_list.append(apoe_1)
                        apoe_2 = gr.Dropdown(label="APOE Allele 2", choices=["e2", "e3", "e4"]); inputs_list.append(apoe_2)
                    with gr.Row():
                        psen1_1 = gr.Textbox(label="PSEN1 Allele 1 (Variant)"); inputs_list.append(psen1_1)
                        psen1_2 = gr.Textbox(label="PSEN1 Allele 2 (Variant)"); inputs_list.append(psen1_2)
                    with gr.Row():
                        psen2_1 = gr.Textbox(label="PSEN2 Allele 1 (Variant)"); inputs_list.append(psen2_1)
                        psen2_2 = gr.Textbox(label="PSEN2 Allele 2 (Variant)"); inputs_list.append(psen2_2)
                    with gr.Row():
                        app_1 = gr.Textbox(label="APP Allele 1 (Variant)"); inputs_list.append(app_1)
                        app_2 = gr.Textbox(label="APP Allele 2 (Variant)"); inputs_list.append(app_2)

                # Parkinson's Disease Genes
                with gr.TabItem("PD-Related Genes"):
                    with gr.Row():
                        lrrk2_1 = gr.Textbox(label="LRRK2 Allele 1 (Variant)"); inputs_list.append(lrrk2_1)
                        lrrk2_2 = gr.Textbox(label="LRRK2 Allele 2 (Variant)"); inputs_list.append(lrrk2_2)
                    with gr.Row():
                        prkn_1 = gr.Textbox(label="PRKN (Parkin) Allele 1"); inputs_list.append(prkn_1)
                        prkn_2 = gr.Textbox(label="PRKN (Parkin) Allele 2"); inputs_list.append(prkn_2)
                    with gr.Row():
                        snca_1 = gr.Textbox(label="SNCA Allele 1 (Variant)"); inputs_list.append(snca_1)
                        snca_2 = gr.Textbox(label="SNCA Allele 2 (Variant)"); inputs_list.append(snca_2)
                
                # FTD / Tauopathy Genes
                with gr.TabItem("FTD/ALS & Tauopathy Genes"):
                    with gr.Row():
                        mapt_1 = gr.Textbox(label="MAPT Allele 1 (Variant)"); inputs_list.append(mapt_1)
                        mapt_2 = gr.Textbox(label="MAPT Allele 2 (Variant)"); inputs_list.append(mapt_2)
                    with gr.Row():
                        grn_1 = gr.Textbox(label="GRN Allele 1 (Variant)"); inputs_list.append(grn_1)
                        grn_2 = gr.Textbox(label="GRN Allele 2 (Variant)"); inputs_list.append(grn_2)
                
                # Expansion Disorder Genes
                with gr.TabItem("Expansion Repeats"):
                    with gr.Row():
                        c9_1 = gr.Number(label="C9orf72 Allele 1 (Repeats)"); inputs_list.append(c9_1)
                        c9_2 = gr.Number(label="C9orf72 Allele 2 (Repeats)"); inputs_list.append(c9_2)
                    with gr.Row():
                        htt_1 = gr.Number(label="HTT Allele 1 (Repeats)"); inputs_list.append(htt_1)
                        htt_2 = gr.Number(label="HTT Allele 2 (Repeats)"); inputs_list.append(htt_2)
                        
                # Ataxia Genes
                with gr.TabItem("Ataxia-Related Genes"):
                    with gr.Row():
                        atxn1_1 = gr.Number(label="ATXN1 Allele 1 (Repeats)"); inputs_list.append(atxn1_1)
                        atxn1_2 = gr.Number(label="ATXN1 Allele 2 (Repeats)"); inputs_list.append(atxn1_2)
                    with gr.Row():
                        atxn2_1 = gr.Number(label="ATXN2 Allele 1 (Repeats)"); inputs_list.append(atxn2_1)
                        atxn2_2 = gr.Number(label="ATXN2 Allele 2 (Repeats)"); inputs_list.append(atxn2_2)

            with gr.Accordion("Neuropsychological Assessment (Optional)", open=False):
                with gr.Row():
                    moca_input = gr.Slider(label="MoCA Score", minimum=0, maximum=30, step=1); inputs_list.append(moca_input)
                    mmse_input = gr.Slider(label="MMSE Score", minimum=0, maximum=30, step=1); inputs_list.append(mmse_input)
            
            with gr.Accordion("Neuroimaging & Fluid Biomarkers (Optional)", open=False):
                gr.Markdown("**Volumetric Normalization:** If you enter any volumetric data, TIV is mandatory.")
                with gr.Row():
                    tiv_input = gr.Number(label="Total Intracranial Volume (TIV, cm³)"); inputs_list.append(tiv_input)
                    hippocampal_vol_input = gr.Number(label="Hippocampal Volume (cm³)"); inputs_list.append(hippocampal_vol_input)
            
            run_single_button = gr.Button("Generate Clinical Report", variant="primary")
            gr.Markdown("---")
            gr.Markdown("### Diagnostic Report")
            single_output_summary = gr.Markdown(label="Tridimensional Summary")
            single_output_probs = gr.Markdown(label="Probabilistic Diagnosis")
            single_output_json = gr.JSON(label="Full Report Data")

        # --- TAB 2: COHORT ANALYSIS FOR RESEARCH ---
        with gr.TabItem("Research: Cohort Analysis"):
            gr.Markdown("## Batch Processing and Analysis for Research Datasets")
            file_input = gr.File(label="Upload Patient Cohort CSV", file_types=[".csv"])
            run_cohort_button = gr.Button("Analyze Full Cohort", variant="primary")
            gr.Markdown("---")
            cohort_status_message = gr.Textbox(label="Status", interactive=False)
            cohort_output_table = gr.DataFrame(label="Diagnostic Results for Cohort", wrap=True)
            methodology_report = gr.Markdown(label="Methodology")
            
    # --- Connect UI components to backend functions ---
    # (Cohort Analysis connection remains the same, but we mock the function for now)
    run_cohort_button.click(fn=lambda x: (None, "Processing not implemented in this version.", ""), inputs=[file_input], outputs=[cohort_output_table, cohort_status_message, methodology_report])
    
    run_single_button.click(
        fn=process_single_patient,
        inputs=inputs_list,
        outputs=[single_output_summary, single_output_probs, single_output_json]
    )

if __name__ == "__main__":
    print("Launching Gradio interface...")
    demo.launch(share=True)
