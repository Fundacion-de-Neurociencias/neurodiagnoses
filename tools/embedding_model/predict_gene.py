# tools/embedding_model/predict_gene.py
import json
import os
import torch

# We need to import the model's class definition from the training script
try:
    from .train_embedding_model import PhenotypeEmbedder, MODEL_DIR, MODEL_PATH, VOCAB_PHENOTYPE_PATH, VOCAB_GENE_PATH, EMBEDDING_DIM, HIDDEN_DIM
except ImportError as e:
    print(f"FAILED to import from train_embedding_model. Error: {e}")

def predict_causal_gene(patient_phenotypes: list):
    """
    Loads the trained model and predicts the most likely causal gene(s)
    for a given list of patient phenotypes.
    """
    print("--- Starting Causal Gene Prediction ---")

    # 1. Load vocabularies
    print("Loading model and vocabularies...")
    try:
        with open(VOCAB_PHENOTYPE_PATH, 'r') as f:
            phenotype_vocab = json.load(f)
        with open(VOCAB_GENE_PATH, 'r') as f:
            gene_vocab = json.load(f)
        idx_to_gene = {i: gene for gene, i in gene_vocab.items()}
    except FileNotFoundError:
        print("Error: Vocabulary files not found. Please run the training script first.")
        return

    # 2. Initialize and load the model
    model = PhenotypeEmbedder(len(phenotype_vocab), EMBEDDING_DIM, HIDDEN_DIM, len(gene_vocab))
    try:
        model.load_state_dict(torch.load(MODEL_PATH))
        model.eval() 
    except FileNotFoundError:
        print(f"Error: Model file not found at {MODEL_PATH}. Please run the training script first.")
        return

    print("✅ Model and vocabularies loaded successfully.")

    # 3. Preprocess the input phenotypes
    input_indices = [phenotype_vocab.get(p, 0) for p in patient_phenotypes]
    if not any(p in phenotype_vocab for p in patient_phenotypes):
         print(f"Warning: None of the provided phenotypes {patient_phenotypes} were found in the vocabulary.")
         return

    input_tensor = torch.tensor(input_indices, dtype=torch.long).unsqueeze(0)

    # 4. Make a prediction
    print(f"\nInput Phenotypes: {patient_phenotypes}")
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.softmax(outputs, dim=1)[0]

    # 5. Get and print top predictions
    k = min(5, len(gene_vocab))
    top_prob, top_indices = torch.topk(probabilities, k)

    print(f"\n--- Top {k} Predicted Causal Genes ---")
    for i in range(top_prob.size(0)):
        gene_index = top_indices[i].item()
        gene_name = idx_to_gene[gene_index]
        probability = top_prob[i].item()
        print(f"{i+1}. Gene: {gene_name:<12} | Probability: {probability:.2%}")

def main():
    """Main execution function."""
    sample_patient_1 = {"phenotypes": ["HP:0001300", "HP:0002069"]}
    sample_patient_2 = {"phenotypes": ["HP:0001250", "HP:0002120"]}

    predict_causal_gene(patient_phenotypes=sample_patient_1["phenotypes"])
    print("\n---------------------------------------")
    predict_causal_gene(patient_phenotypes=sample_patient_2["phenotypes"])

# This check is crucial for running the script directly
if __name__ == '__main__':
    main()