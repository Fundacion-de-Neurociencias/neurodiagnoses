# -*- coding: utf-8 -*-
"""
Neurodiagnoses Unified Model: Patient Data Tokenizer

This script is the first step towards the unified, disease-agnostic AI model.
Its purpose is to convert heterogeneous patient data (biomarkers, genetics,
clinical scores) into a unified sequence of discrete tokens, suitable for
input into a Transformer-based architecture.

Workflow:
1. Define a vocabulary for all possible events (biomarker names, value bins).
2. For each patient, convert their timeline of data points into a sequence of tokens.
3. Add special tokens like [CLS] (start), [SEP] (separator), and [PAD] (padding).
4. Save the tokenized sequences for model training.
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np

# Ensure the project root is in the Python path for module imports
# This is typically handled by setting PYTHONPATH or by the execution environment.
# For direct execution, consider adding the project root to sys.path if necessary.
# Example: sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


class PatientDataTokenizer:
    """
    Tokenizes patient records into sequences for a Transformer model.
    """
    def __init__(self, data_path, output_path):
        self.data_path = data_path
        self.output_path = output_path
        self.vocabulary = {}
        self.reverse_vocabulary = {}
        # Special tokens are essential for sequence models
        self.special_tokens = {'[PAD]': 0, '[CLS]': 1, '[SEP]': 2, '[UNK]': 3}
        self.next_token_id = len(self.special_tokens)

    def build_vocabulary(self, df):
        """
        Builds a vocabulary from the dataset columns and binned values.
        
        This is a conceptual implementation. A real implementation would need
        to intelligently handle numerical vs. categorical data.
        """
        print("Building vocabulary...")
        # Add all feature names (biomarkers, genetics, etc.) to vocabulary
        # Assuming columns are identifiers like 'biomarkers_MMSE_value'
        feature_names = [col for col in df.columns if col not in ['patient_id', 'visit_date']]
        for feature in feature_names:
            if feature not in self.vocabulary:
                self.vocabulary[feature] = self.next_token_id
                self.next_token_id += 1
        
        # In a real scenario, we would also create tokens for binned numerical values
        # For now, we'll just use feature names.
        
        self.reverse_vocabulary = {v: k for k, v in self.vocabulary.items()}
        print(f"Vocabulary built with {len(self.vocabulary)} tokens.")

    def tokenize_patient(self, patient_df):
        """
        Converts a single patient's data timeline into a token sequence.
        
        Args:
            patient_df (pd.DataFrame): A dataframe containing all records for one patient,
                                     sorted chronologically.

        Returns:
            list: A list of integer token IDs.
        """
        token_sequence = [self.special_tokens['[CLS]']]
        
        # This is a simplified example. A more complex version would handle
        # time steps and values more explicitly.
        for _, row in patient_df.iterrows():
            for feature, value in row.items():
                if pd.notna(value) and feature in self.vocabulary:
                    # Add token for the feature name
                    token_sequence.append(self.vocabulary[feature])
                    # In a real implementation, we would add a token for the value,
                    # possibly after binning/quantization.
        
        token_sequence.append(self.special_tokens['[SEP]'])
        return token_sequence

    def run_tokenization(self):
        """
        Main workflow to load data, build vocab, and tokenize all patients.
        """
        print("--- Starting Patient Data Tokenization Workflow ---")
        df = pd.read_parquet(self.data_path)
        
        # Build vocabulary based on the entire dataset
        self.build_vocabulary(df)

        # For this example, we'll just show the tokenization of the first patient
        # A full implementation would process and save all patients.
        first_patient_id = df['patient_id'].iloc[0]
        first_patient_df = df[df['patient_id'] == first_patient_id].sort_values(by='biomarkers_Age_value')
        
        print(f"\nTokenizing first patient (ID: {first_patient_id})...")
        tokenized_sequence = self.tokenize_patient(first_patient_df)
        
        print(f"Generated token sequence (first 30 tokens): {tokenized_sequence[:30]}")
        
        # Example of converting back to human-readable format
        human_readable = [self.reverse_vocabulary.get(t, str(t)) for t in tokenized_sequence[:30]]
        print(f"Human-readable (first 30 tokens): {human_readable}")
        
        print("\n--- Tokenization Workflow (Conceptual) Completed ---")
        # In a full run, we would save all tokenized sequences to self.output_path


def main():
    parser = argparse.ArgumentParser(description="Tokenize patient data for unified modeling.")
    parser.add_argument(
        '--data_path',
        type=str,
        default='data/processed/analysis_ready_dataset.parquet',
        help='Path to the analysis-ready dataset.'
    )
    parser.add_argument(
        '--output_path',
        type=str,
        default='data/processed/tokenized_patient_sequences.json',
        help='Path to save the tokenized sequences.'
    )
    args = parser.parse_args()

    tokenizer = PatientDataTokenizer(data_path=args.data_path, output_path=args.output_path)
    tokenizer.run_tokenization()


if __name__ == '__main__':
    main()