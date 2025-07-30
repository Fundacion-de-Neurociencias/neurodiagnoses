# tools/embedding_model/train_embedding_model.py
import json
import os
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
import numpy as np

# --- Configuration ---
DATASET_PATH = 'data/simulated_patient_dataset.jsonl'
MODEL_DIR = 'models'
MODEL_PATH = os.path.join(MODEL_DIR, 'embedding_model.pth')
VOCAB_PHENOTYPE_PATH = os.path.join(MODEL_DIR, 'phenotype_vocab.json')
VOCAB_GENE_PATH = os.path.join(MODEL_DIR, 'gene_vocab.json')

# --- Model Hyperparameters ---
EMBEDDING_DIM = 64
HIDDEN_DIM = 128
EPOCHS = 10
LEARNING_RATE = 0.001

# --- Data Loading and Preprocessing ---
def load_data(path):
    data = []
    with open(path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

# --- Neural Network Model Definition ---
class PhenotypeEmbedder(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_size):
        super(PhenotypeEmbedder, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.fc1 = nn.Linear(embedding_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_size)

    def forward(self, x):
        # x is a batch of patient phenotypes
        embedded = self.embedding(x)
        # Average the embeddings for all phenotypes of a patient
        pooled = embedded.mean(dim=1)
        out = self.fc1(pooled)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# --- Main Training Function ---
def train_model():
    print("--- Starting Embedding Model Training ---")
    os.makedirs(MODEL_DIR, exist_ok=True)

    # 1. Load and process data
    print("Loading and preprocessing data...")
    dataset = load_data(DATASET_PATH)

    all_phenotypes = set(p for item in dataset for p in item['phenotypes'])
    phenotype_vocab = {pheno: i+1 for i, pheno in enumerate(all_phenotypes)} # 0 is for padding
    phenotype_vocab['<PAD>'] = 0

    all_genes = sorted(list(set(item['causal_gene'] for item in dataset)))
    gene_vocab = {gene: i for i, gene in enumerate(all_genes)}

    X = [torch.tensor([phenotype_vocab[p] for p in item['phenotypes']], dtype=torch.long) for item in dataset]
    y = torch.tensor([gene_vocab[item['causal_gene']] for item in dataset], dtype=torch.long)

    # Pad sequences to the same length for batching
    X_padded = nn.utils.rnn.pad_sequence(X, batch_first=True, padding_value=0)

    X_train, X_test, y_train, y_test = train_test_split(X_padded, y, test_size=0.2, random_state=42)

    # 2. Initialize model, loss, and optimizer
    model = PhenotypeEmbedder(len(phenotype_vocab), EMBEDDING_DIM, HIDDEN_DIM, len(gene_vocab))
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    print(f"✅ Data preprocessed. Starting training for {EPOCHS} epochs...")

    # 3. Training Loop
    for epoch in range(EPOCHS):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 2 == 0:
            print(f'Epoch [{epoch+1}/{EPOCHS}], Loss: {loss.item():.4f}')

    print("✅ Training finished.")

    # 4. Save model and vocabularies
    print("Saving model and vocabularies...")
    torch.save(model.state_dict(), MODEL_PATH)
    with open(VOCAB_PHENOTYPE_PATH, 'w') as f:
        json.dump(phenotype_vocab, f)
    with open(VOCAB_GENE_PATH, 'w') as f:
        json.dump(gene_vocab, f)

    print(f"   Model saved to: {MODEL_PATH}")
    print(f"   Vocabularies saved to: {MODEL_DIR}/")

if __name__ == '__main__':
    train_model()
