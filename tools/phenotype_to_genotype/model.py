# tools/phenotype_to_genotype/model.py
import torch
import torch.nn as nn
import json
import os

# --- Configuration ---
MODEL_DIR = 'models'
MODEL_PATH = os.path.join(MODEL_DIR, 'embedding_model.pth')
VOCAB_PHENOTYPE_PATH = os.path.join(MODEL_DIR, 'phenotype_vocab.json')
VOCAB_GENE_PATH = os.path.join(MODEL_DIR, 'gene_vocab.json')

# --- Model Hyperparameters ---
EMBEDDING_DIM = 64
HIDDEN_DIM = 128

class PhenotypeEmbedder(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_size):
        super(PhenotypeEmbedder, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.fc1 = nn.Linear(embedding_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_size)

    def forward(self, x):
        embedded = self.embedding(x)
        pooled = embedded.mean(dim=1)
        out = self.fc1(pooled)
        out = self.relu(out)
        out = self.fc2(out)
        return out

    # --- NEW METHOD FOR XAI ---
    def get_phenotype_importance(self, input_tensor, idx_to_phenotype):
        """
        Calculates the importance of each input phenotype for the top prediction
        using a gradient-based saliency method.
        """
        self.eval() # Ensure model is in evaluation mode

        # We need to calculate gradients with respect to the embeddings
        input_embeddings = self.embedding(input_tensor)
        input_embeddings.retain_grad()

        # Forward pass
        pooled = input_embeddings.mean(dim=1)
        out = self.fc1(pooled)
        out = self.relu(out)
        out = self.fc2(out)

        # Get the score for the top predicted class
        top_score = out.max()

        # Backpropagate to get gradients
        top_score.backward()

        # Importance is the norm of the gradient for each phenotype embedding
        saliency = input_embeddings.grad.norm(p=2, dim=2).squeeze(0)

        # Map importance scores back to phenotype names
        importances = []
        for i, score in enumerate(saliency):
            phenotype_idx = input_tensor[0, i].item()
            if phenotype_idx != 0: # Ignore padding
                phenotype_name = idx_to_phenotype.get(phenotype_idx, "Unknown")
                importances.append((phenotype_name, score.item()))

        # Sort by importance (highest first)
        importances.sort(key=lambda x: x[1], reverse=True)

        return importances