# tools/advanced_annotator/run_advanced_annotation.py
import json
import os
import torch
from datetime import datetime

# Import the refactored model class
from tools.phenotype_to_genotype.model import PhenotypeEmbedder
from tools.ml_pipelines.pipelines_axis3_pathology import Axis3PathologyPipeline

def run_full_pipeline(patient_json_path):
    """
    Main function to run the advanced annotation pipeline, now including XAI.
    """
    print(f"--- Running Advanced Annotation for patient: {patient_json_path} ---")

    # --- 1. Load patient JSON and simulate phenotypes ---
    try:
        with open(patient_json_path, 'r') as f:
            patient_data = json.load(f)
        print(f"✅ Patient JSON loaded.")
    except FileNotFoundError:
        print(f"Error: Patient file not found at {patient_json_path}")
        return

    # Simulate HPO phenotypes for Axis 1 prediction
    simulated_hpo_phenotypes = ['HP:0001250', 'HP:0002069', 'HP:0000726']
    print(f"Using simulated HPO phenotypes for Axis 1: {simulated_hpo_phenotypes}")

    # --- 2. Load Model and Vocabularies ---
    model_dir = 'models'
    try:
        with open(os.path.join(model_dir, 'phenotype_vocab.json'), 'r') as f:
            phenotype_vocab = json.load(f)
        with open(os.path.join(model_dir, 'gene_vocab.json'), 'r') as f:
            gene_vocab = json.load(f)

        idx_to_phenotype = {v: k for k, v in phenotype_vocab.items()}
        idx_to_gene = {i: gene for gene, i in gene_vocab.items()}

        model = PhenotypeEmbedder(len(phenotype_vocab), 64, 128, len(gene_vocab))
        model.load_state_dict(torch.load(os.path.join(model_dir, 'embedding_model.pth')))
        model.eval()
        print("✅ Model and vocabularies loaded.")
    except FileNotFoundError:
        print(f"Error: Model or vocabulary files not found in '{model_dir}'. Please run training script.")
        return

    # For now, we simulate the phenotype list as it's not in the JSON yet
    phenotypes = simulated_hpo_phenotypes # Use the simulated HPO phenotypes
    # Filter out phenotypes not in the vocabulary
    phenotypes = [p for p in phenotypes if p in phenotype_vocab]
    print(f"Using simulated and filtered phenotypes: {phenotypes}")

    # --- 3. Predict Etiology (Axis 1) ---
    input_indices = [phenotype_vocab.get(p, 0) for p in phenotypes]
    # Pad the input_indices to ensure it's a 2D tensor for the model
    max_len = max(len(input_indices), 1) # Ensure at least 1 for padding
    padded_input_indices = input_indices + [0] * (max_len - len(input_indices))
    input_tensor = torch.tensor(padded_input_indices, dtype=torch.long).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.softmax(outputs, dim=1)[0]

    top_prob, top_indices = torch.topk(probabilities, 3)

    axis1_predictions = []
    for i in range(top_prob.size(0)):
        gene = idx_to_gene[top_indices[i].item()]
        prob = top_prob[i].item()
        axis1_predictions.append(f"{gene}: {prob:.1%}")

    axis1 = f"Predicted Etiology (Probabilistic): " + ", ".join(axis1_predictions)
    print("✅ Axis 1 (Etiology) prediction generated.")

    # --- 4. Get XAI Explanation ---
    importances = model.get_phenotype_importance(input_tensor, idx_to_phenotype)
    top_features = [f"{phenotype[0].split('(')[0].strip()}" for phenotype in importances[:3]]
    axis1 += f" | Driven by: {', '.join(top_features)}"
    print("✅ XAI explanation generated.")

    # --- 5. Predict Axis 3 (Phenotype from Neuropathology) ---
    axis3_pipeline = Axis3PathologyPipeline()
    # Assuming patient_data contains a 'patient_id' field
    # Extract patient_id from the filename (e.g., ND_001 from ND_001.json)
    patient_filename = os.path.basename(patient_json_path)
    patient_id_str = os.path.splitext(patient_filename)[0]
    # Remove "ND_" prefix and convert to integer
    try:
        patient_id = int(patient_id_str.replace("ND_", ""))
    except ValueError:
        print(f"Error: Could not extract integer patient_id from filename {patient_filename}")
        patient_id = None

    if patient_id is None:
        print("Error: 'patient_id' not found in patient JSON. Cannot predict Axis 3.")
        axis3 = "Neuropathology Profile (t-Tau): Not available (patient_id missing)"
    else:
        axis3 = axis3_pipeline.predict(patient_id)
        print("✅ Axis 3 (Neuropathology) prediction generated.")

    # --- 6. Define Axis 2 (Molecular) ---
    axis2 = "Molecular Profile (Requires Full Omics Data)"

    # --- 7. Format Final Annotation ---

    timestamp = datetime.now().strftime('%Y-%m-%d')
    full_annotation = f"--- FINAL MULTI-MODEL ANNOTATION ---\n[{timestamp}]: {axis1} / {axis2} / {axis3}\n------------------------------------"

    print(full_annotation)

if __name__ == '__main__':
    patient_file = 'patient_database/ND_001.json'
    run_full_pipeline(patient_json_path=patient_file)