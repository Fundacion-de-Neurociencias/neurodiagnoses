# tools/tridimensional_annotation/annotator.py
# This module implements the definitive tridimensional diagnostic annotation framework
# as described in Menendez-Gonzalez (2025), Alzheimer's & Dementia.

from datetime import datetime
import pandas as pd
import numpy as np
import os
import sys

# Add project root for imports to find other tools and models
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# We will import our functional pipelines to get the data for each axis
from tools.ml_pipelines.pipelines_axis2_molecular import Axis2MolecularPipeline
from tools.ml_pipelines.pipelines_axis3_severity_mapping import Axis3SeverityMapperPipeline

# In a real scenario, we would also import the Axis 1 genetics pipeline
# from workflows.risk_prediction.predict_risk import predict_risk

def generate_tridimensional_annotation(patient_id):
    """
    Generates a full, structured tridimensional diagnostic annotation for a patient.
    """
    print(f"--- Generating Tridimensional Annotation for Subject ID: {patient_id} ---")

    # --- Simulate fetching standardized patient data ---
    # In a real system, this would come from the ingestion pipeline (e.g., a PatientRecord object)
    patient_molecular_data = pd.DataFrame([np.random.rand(5)], columns=['biomarkers_Age_value', 'biomarkers_MMSE_value', 'biomarkers_pTau_value', 'biomarkers_Abeta42_value', 'biomarkers_Hippocampal Volume_value'])
    patient_imaging_data = {
        'lh_entorhinal_volume': 1980.0, 'rh_entorhinal_volume': 2010.0,
        'lh_hippocampus_volume': 3050.0, 'rh_hippocampus_volume': 3100.0,
        'lh_precuneus_thickness': 1.85, 'rh_precuneus_thickness': 1.9
    }
    patient_genetics = {"APOE_e4": 1} # Simulating one APOE4 allele

    # --- AXIS 1: ETIOLOGY ---
    # This axis focuses on genetic and environmental root causes.
    axis1_findings = []
    if patient_genetics.get("APOE_e4", 0) > 0:
        axis1_findings.append(f"Sporadic (APOE_e4 Positive, {patient_genetics['APOE_e4']} allele(s))")
    else:
        axis1_findings.append("Sporadic (APOE_e4 Negative)")
    # In a real system, we'd add other pathogenic genes or risk scores here.
    axis1_text = ", ".join(axis1_findings)

    # --- AXIS 2: MOLECULAR MARKERS ---
    # This axis describes primary (proteinopathies) and secondary (e.g., NfL) markers.
    axis2_pipeline = Axis2MolecularPipeline()
    molecular_profile = axis2_pipeline.predict(patient_molecular_data)
    top_molecular_dx = max(molecular_profile, key=molecular_profile.get)
    # This simulates finding a secondary biomarker.
    secondary_marker = "NfL (moderate neurodegenerative activity)"
    axis2_text = f"Primary: {top_molecular_dx} profile ({molecular_profile[top_molecular_dx]:.1%}); Secondary: {secondary_marker}"

    # --- AXIS 3: NEUROANATOMOCLINICAL CORRELATIONS ---
    # This axis links anatomical findings to clinical deficits.
    axis3_pipeline = Axis3SeverityMapperPipeline()
    severity_map = axis3_pipeline.predict_and_explain(patient_imaging_data)
    top_region = max(severity_map['key_contributing_regions'], key=lambda k: abs(severity_map['key_contributing_regions'][k]))
    # This simulates linking the top region to a clinical symptom.
    clinical_correlation = "Episodic Memory Deficit"
    axis3_text = f"{top_region.replace('_volume','')} atrophy: {clinical_correlation}"

    # --- FINAL ANNOTATION ---
    timestamp = datetime.now().strftime("%B %y") # Format: Month YY
    final_annotation = f"[{timestamp}]: {axis1_text} / {axis2_text} / {axis3_text}"
    
    return final_annotation

if __name__ == '__main__':
    # Ensure models are trained before running the example
    print("--- Pre-flight check: Ensuring models are trained ---")
    if not os.path.exists('models/axis2_molecular_model.joblib'):
      Axis2MolecularPipeline().train_and_evaluate()
    if not os.path.exists('models/axis3_severity_model.joblib'):
      Axis3SeverityMapperPipeline().train()

    # Generate an annotation for a sample patient
    annotation = generate_tridimensional_annotation(patient_id="ND_DEMO_001")
    print("\n--- FINAL DIAGNOSTIC ANNOTATION ---")
    print(annotation)
    print("-----------------------------------")
