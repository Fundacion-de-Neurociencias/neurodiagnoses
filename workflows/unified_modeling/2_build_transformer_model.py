# -*- coding: utf-8 -*-
"""
Neurodiagnoses Unified Model: Transformer Model Builder

This script defines and builds a conceptual Transformer-based neural network
architecture for unified disease modeling. It focuses on the structure of the
model, including embedding layers, Transformer encoder blocks, and output layers.

Workflow:
1. Define model parameters (vocab size, embedding dim, num heads, etc.).
2. Construct the Transformer encoder architecture.
3. Define input and output layers suitable for various prediction tasks.
4. (Conceptual) Compile the model.
"""

import os
import sys
import argparse
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Ensure the project root is in the Python path for module imports
# This is typically handled by setting PYTHONPATH or by the execution environment.
# For direct execution, consider adding the project root to sys.path if necessary.
# Example: sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
# However, for a robust project, it's better to manage Python path externally or use proper package installation.


class MultiHeadSelfAttention(layers.Layer):
    def __init__(self, embed_dim, num_heads=8):
        super(MultiHeadSelfAttention, self).__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        if embed_dim % num_heads != 0:
            raise ValueError(
                f"embedding dimension = {embed_dim} should be divisible by number of heads = {num_heads}"
            )
        self.projection_dim = embed_dim // num_heads
        self.query_dense = layers.Dense(embed_dim)
        self.key_dense = layers.Dense(embed_dim)
        self.value_dense = layers.Dense(embed_dim)
        self.combine_heads = layers.Dense(embed_dim)

    def attention(self, query, key, value):
        key_transposed = keras.ops.transpose(key, axes=(0, 1, 3, 2)) # Transpose the last two dimensions
        score = keras.ops.matmul(query, key_transposed)
        dim_key = keras.ops.cast(keras.ops.shape(key)[-1], "float32")
        scaled_score = score / keras.ops.sqrt(dim_key)
        weights = keras.ops.softmax(scaled_score, axis=-1)
        output = keras.ops.matmul(weights, value)
        return output, weights

    def separate_heads(self, x, batch_size):
        x = keras.ops.reshape(x, (batch_size, -1, self.num_heads, self.projection_dim))
        return keras.ops.transpose(x, axes=[0, 2, 1, 3])

    def call(self, inputs):
        batch_size = keras.ops.shape(inputs)[0]
        query = self.query_dense(inputs)
        key = self.key_dense(inputs)
        value = self.value_dense(inputs)
        query = self.separate_heads(query, batch_size)
        key = self.separate_heads(key, batch_size)
        value = self.separate_heads(value, batch_size)
        attention, weights = self.attention(query, key, value)
        attention = keras.ops.transpose(attention, axes=[0, 2, 1, 3])
        concat_attention = keras.ops.reshape(attention, (batch_size, -1, self.embed_dim))
        output = self.combine_heads(concat_attention)
        return output


class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerBlock, self).__init__()
        self.att = MultiHeadSelfAttention(embed_dim, num_heads)
        self.ffn = keras.Sequential(
            [
                layers.Dense(ff_dim, activation="relu"),
                layers.Dense(embed_dim),
            ]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.att(inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)


class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        maxlen = keras.ops.shape(x)[-1]
        positions = keras.ops.arange(start=0, stop=maxlen)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions


class UnifiedTransformerModel:
    """
    Defines the architecture for the unified Transformer model.
    """
    def __init__(self, vocab_size, maxlen, embed_dim, num_heads, ff_dim):
        self.vocab_size = vocab_size
        self.maxlen = maxlen
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.model = self._build_model()

    def _build_model(self):
        inputs = layers.Input(shape=(self.maxlen,))
        # Define a placeholder for the training argument
        # For model building/summary, we can pass a concrete boolean False
        training_arg = False

        embedding_layer = TokenAndPositionEmbedding(self.maxlen, self.vocab_size, self.embed_dim)
        x = embedding_layer(inputs)
        transformer_block = TransformerBlock(self.embed_dim, self.num_heads, self.ff_dim)
        x = transformer_block(x, training=training_arg) # Pass the training argument
        x = layers.GlobalAveragePooling1D()(x)
        x = layers.Dropout(0.1)(x, training=training_arg) # Pass the training argument
        x = layers.Dense(20, activation="relu")(x)
        x = layers.Dropout(0.1)(x, training=training_arg) # Pass the training argument
        outputs = layers.Dense(1, activation="sigmoid")(x) # Example output for binary classification

        model = keras.Model(inputs=inputs, outputs=outputs) # Revert to single input for simplicity of summary
        return model

    def summary(self):
        # Create dummy inputs for summary
        dummy_inputs = tf.zeros((1, self.maxlen), dtype=tf.int32)
        self.model(dummy_inputs) # Call the model once to build it
        self.model.summary()


def main():
    parser = argparse.ArgumentParser(description="Build a conceptual Transformer model for unified modeling.")
    parser.add_argument('--vocab_size', type=int, default=10000, help='Size of the vocabulary.')
    parser.add_argument('--maxlen', type=int, default=200, help='Maximum sequence length.')
    parser.add_argument('--embed_dim', type=int, default=32, help='Embedding dimension.')
    parser.add_argument('--num_heads', type=int, default=2, help='Number of attention heads.')
    parser.add_argument('--ff_dim', type=int, default=32, help='Feed forward dimension.')
    args = parser.parse_args()

    print("--- Building Unified Transformer Model ---")
    model_builder = UnifiedTransformerModel(
        vocab_size=args.vocab_size,
        maxlen=args.maxlen,
        embed_dim=args.embed_dim,
        num_heads=args.num_heads,
        ff_dim=args.ff_dim
    )
    model_builder.summary()
    print("--- Unified Transformer Model Built Successfully (Conceptual) ---")


if __name__ == '__main__':
    main()
