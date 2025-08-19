# app.py v3.1 - Universal Diagnosis with "Why"
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import gradio as gr
from pathlib import Path
import pandas as pd
from unified_orchestrator import run_cohort_pipeline
# ... resto de imports sin cambios

def run_cohort_analysis_ui(file_obj):
    if file_obj is None:
        return None, "Please upload a CSV file to begin analysis."

    initial_prior = 0.10
    
    # La llamada al backend ahora devuelve dos DataFrames
    results_df, _ = run_cohort_pipeline(
        cohort_csv_path=file_obj.name,
        initial_prior=initial_prior
    )

    # --- [LÓGICA DE FILTRADO Y REPORTE RESTAURADA Y MEJORADA] ---
    prob_cols = [col for col in results_df.columns if col.startswith('Prob_')]
    
    final_rows = []
    for index, patient_row in results_df.iterrows():
        patient_summary = {"SubjectID": patient_row["SubjectID"]}
        
        high_prob_diseases = {}
        other_prob_sum = 0.0

        # Ordenar las probabilidades de mayor a menor para este paciente
        patient_probs = {col.replace("Prob_", "").replace("_", " "): patient_row[col] for col in prob_cols}
        sorted_patient_probs = sorted(patient_probs.items(), key=lambda item: item[1], reverse=True)

        for disease_name, prob in sorted_patient_probs:
            if prob > 0.05:
                high_prob_diseases[disease_name] = f"{prob:.1%}"
            else:
                other_prob_sum += prob
        
        patient_summary.update(high_prob_diseases)
        
        if other_prob_sum > 0.0:
            patient_summary["Others (<5%)"] = f"{other_prob_sum:.1%}"
        
        # Placeholder para la evidencia (necesitaría que el motor la devuelva por paciente/enfermedad)
        patient_summary["Supporting Evidence (Why)"] = "Evidence trail generation in progress..."
        final_rows.append(patient_summary)
    
    display_df = pd.DataFrame(final_rows).fillna('-')

    summary_html = f"<h4>Cohort Analysis Summary:</h4>"
    summary_html += f"<ul><li><b>{len(results_df)}</b> patients analyzed.</li></ul>"
    summary_html += f"<p style='font-size: 0.8em; color: #666;'><i>Note: Only diagnoses with a posterior probability > 5% are listed individually.</i></p>"

    return display_df, summary_html

# --- Construcción de la Interfaz (sin cambios) ---
with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    # ... (código de la UI sin cambios)
