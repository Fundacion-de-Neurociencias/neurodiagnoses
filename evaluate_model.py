import os
import torch
import json
from tools.phenotype_to_genotype.model import PhenotypeEmbedder
from tools.data_ingestion.parsers.ddd_adapter import parse_ddd_csv

# --- Configuration ---
MODEL_DIR = 'models'
MODEL_PATH = os.path.join(MODEL_DIR, 'embedding_model.pth')
VOCAB_PHENOTYPE_PATH = os.path.join(MODEL_DIR, 'phenotype_vocab.json')
VOCAB_GENE_PATH = os.path.join(MODEL_DIR, 'gene_vocab.json')
DDD_VALIDATION_FILE = 'data/ddd/ddd_validation_sample.csv'

def evaluate_model():
    print("--- Starting Model Evaluation ---")

    # 1. Load Model and Vocabularies
    try:
        with open(VOCAB_PHENOTYPE_PATH, 'r') as f:
            phenotype_vocab = json.load(f)
        with open(VOCAB_GENE_PATH, 'r') as f:
            gene_vocab = json.load(f)

        idx_to_gene = {i: gene for gene, i in gene_vocab.items()}

        model = PhenotypeEmbedder(len(phenotype_vocab), 64, 128, len(gene_vocab))
        model.load_state_dict(torch.load(MODEL_PATH))
        model.eval()
        print("✅ Model and vocabularies loaded.")
    except FileNotFoundError:
        print(f"Error: Model or vocabulary files not found in '{MODEL_DIR}'. Please run training script.")
        return

    # 2. Load DDD Validation Data
    try:
        ddd_patients = parse_ddd_csv(DDD_VALIDATION_FILE)
        print(f"✅ Loaded {len(ddd_patients)} patients from {DDD_VALIDATION_FILE}")
    except FileNotFoundError:
        print(f"Error: DDD validation file not found at {DDD_VALIDATION_FILE}")
        return

    correct_predictions = 0
    total_predictions = 0

    # 3. Evaluate Model for each patient
    for patient in ddd_patients:
        total_predictions += 1
        patient_phenotypes = patient['phenotypes']
        ground_truth_gene = patient['causal_gene']

        # Filter phenotypes to only include those known by the model
        filtered_phenotypes = [p for p in patient_phenotypes if p in phenotype_vocab]

        if not filtered_phenotypes:
            print(f"Skipping patient {patient['patient_id']}: No known phenotypes.")
            continue

        # Prepare input tensor
        input_indices = [phenotype_vocab.get(p, 0) for p in filtered_phenotypes]
        # Pad the input_indices to ensure it's a 2D tensor for the model
        max_len = max(len(input_indices), 1) # Ensure at least 1 for padding
        padded_input_indices = input_indices + [0] * (max_len - len(input_indices))
        input_tensor = torch.tensor(padded_input_indices, dtype=torch.long).unsqueeze(0)

        # Get prediction
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)[0]
            predicted_gene_id = torch.argmax(probabilities).item()
            predicted_gene_name = idx_to_gene.get(predicted_gene_id, "Unknown")

        print(f"Patient {patient['patient_id']}: Ground Truth: {ground_truth_gene}, Predicted: {predicted_gene_name}")

        if predicted_gene_name == ground_truth_gene:
            correct_predictions += 1

    # 4. Report Accuracy
    accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
    print(f"\n--- Evaluation Results ---")
    print(f"Total Patients: {total_predictions}")
    print(f"Correct Predictions: {correct_predictions}")
    print(f"Accuracy: {accuracy:.2f}%")
    print("--------------------------")

if __name__ == '__main__':
    evaluate_model()
