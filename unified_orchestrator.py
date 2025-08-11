# --- Unified Neurodiagnoses Orchestrator ---
# This script serves as the central brain of the project, integrating the
# different diagnostic axes into a single, cohesive workflow.

import os
import torch
import pandas as pd
import random
from dataclasses import asdict

# --- Import existing and new components ---

# AXIS 1: The advanced PyTorch model for Phenotype-to-Genotype prediction
from tools.phenotype_to_genotype.model import PhenotypeEmbedder, VOCAB_PHENOTYPE_PATH, VOCAB_GENE_PATH, MODEL_PATH as AXIS1_MODEL_PATH

# AXIS 2: Our new ML-based molecular classifier (we'll create its file first)
# We will create its definitive home now.
from tools.ml_pipelines.pipelines_axis2_molecular import Axis2MolecularPipeline

# AXIS 3: The existing rules-based pathology pipeline
from tools.ml_pipelines.pipelines_axis3_pathology import Axis3PathologyPipeline

# --- Helper function to load Axis 1 model ---
def load_axis1_model():
    """Loads the pre-trained PyTorch model for Axis 1."""
    if not os.path.exists(AXIS1_MODEL_PATH):
        print("WARNING: Axis 1 model file not found. Skipping Axis 1.")
        return None, None, None
    
    with open(VOCAB_PHENOTYPE_PATH, 'r') as f: phenotype_vocab = json.load(f)
    with open(VOCAB_GENE_PATH, 'r') as f: gene_vocab = json.load(f)
    
    model = PhenotypeEmbedder(
        vocab_size=len(phenotype_vocab),
        embedding_dim=64,
        hidden_dim=128,
        output_size=len(gene_vocab)
    )
    model.load_state_dict(torch.load(AXIS1_MODEL_PATH))
    model.eval()
    return model, phenotype_vocab, gene_vocab

# --- Main Orchestration ---
def run_full_diagnosis(patient_id):
    """
    Orchestrates the full 3-axis diagnosis for a given patient ID.
    """
    print(f"--- Starting Full 3-Axis Diagnosis for Patient: {patient_id} ---")

    # --- AXIS 1: ETIOLOGY PREDICTION (using existing PyTorch model) ---
    print("\n[INFO] Running Axis 1 (Phenotype-to-Genotype) Prediction...")
    # This is a simulation. In a real case, we'd get HPO terms from the patient data.
    sample_hpo_terms = ["HP:0001250", "HP:0001290"] # Seizure, Generalized hypotonia
    
    # Logic to run the PyTorch model would go here. For this PoC, we'll use a placeholder.
    # axis1_model, p_vocab, g_vocab = load_axis1_model()
    # if axis1_model:
    #     # tokenized_input = ... convert sample_hpo_terms to tensor ...
    #     # prediction = axis1_model(tokenized_input)
    #     axis1_result = "Predicted Genotype: C9orf72 (Placeholder)"
    # else:
    axis1_result = "Axis 1 model not found or failed to run."
    print(f"  > Axis 1 Result: {axis1_result}")

    # --- AXIS 2: MOLECULAR PREDICTION (using our new ML model) ---
    print("\n[INFO] Running Axis 2 (Molecular Profile) Prediction...")
    axis2_pipeline = Axis2MolecularPipeline()
    axis2_result = axis2_pipeline.predict(patient_id)
    print(f"  > Axis 2 Result: {axis2_result}")

    # --- AXIS 3: PHENOTYPE PREDICTION (using existing rules-based pipeline) ---
    print("\n[INFO] Running Axis 3 (Neuropathology) Prediction...")
    axis3_pipeline = Axis3PathologyPipeline()
    axis3_result = axis3_pipeline.predict(patient_id)
    print(f"  > Axis 3 Result: {axis3_result}")

    # --- FINAL REPORT ---
    print("\n\n================ NEURODIAGNOSES FINAL REPORT ================")
    print(f"Patient ID: {patient_id}")
    print("---------------------------------------------------------")
    print(f"AXIS 1 (Etiology):     {axis1_result}")
    print(f"AXIS 2 (Molecular):    {axis2_result}")
    print(f"AXIS 3 (Phenotype):    {axis3_result}")
    print("============================================================")


if __name__ == '__main__':
    # We use a sample patient ID that we know exists in the Cornblath dataset for Axis 3.
    sample_patient_id = 0
    
    # We need to create the Axis 2 model first for this to work.
    print("--- Pre-flight check: Ensuring Axis 2 model is trained ---")
    axis2_pipeline = Axis2MolecularPipeline()
    axis2_pipeline.train()
    
    # Run the full diagnosis
    run_full_diagnosis(patient_id=sample_patient_id)
