# -*- coding: utf-8 -*-
"""
Knowledge Ingestion Pipeline: Step 2 - Transform & Load

This script reads the raw JSONL file produced by the LangExtract pipeline,
transforms the extracted data to match our knowledge base schema, and appends
it to the corresponding likelihood CSV files.
"""

import os
import sys
import json
import pandas as pd
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define paths to our knowledge base files
KB_AXIS1_PATH = "data/reference/axis1_likelihoods_genetics.csv"
KB_AXIS2_PATH = "data/reference/axis2_likelihoods.csv"
KB_AXIS3_PATH = "data/reference/axis3_likelihoods_phenotype.csv"

def transform_and_load(jsonl_path: str, source_id: str):
    """
    Main function to process the JSONL file and update the knowledge base.
    """
    print(f"--- Transforming and Loading Knowledge from: {jsonl_path} ---")

    # Load existing knowledge bases or create them if they don't exist
    df_kb1 = pd.read_csv(KB_AXIS1_PATH) if os.path.exists(KB_AXIS1_PATH) else pd.DataFrame()
    df_kb2 = pd.read_csv(KB_AXIS2_PATH) if os.path.exists(KB_AXIS2_PATH) else pd.DataFrame()
    df_kb3 = pd.read_csv(KB_AXIS3_PATH) if os.path.exists(KB_AXIS3_PATH) else pd.DataFrame()

    new_rows_axis1, new_rows_axis2, new_rows_axis3 = [], [], []

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            # The extractions are nested, so we need to access them
            for extraction in data.get('extractions', []):
                attrs = extraction.get('attributes', {})
                evidence_type = attrs.get('evidence_type')
                
                # Create a base row with common metadata
                base_row = {'source_id': source_id}
                
                if evidence_type == 'genetic_marker':
                    row = base_row.copy()
                    row.update({
                        'evidence': attrs.get('marker_name'),
                        'label': attrs.get('target_disease'),
                        'likelihood_ratio': attrs.get('metric_value'),
                        'note': f"From {source_id}"
                    })
                    new_rows_axis1.append(row)

                elif evidence_type == 'molecular_biomarker':
                    row = base_row.copy()
                    row.update({
                        'evidence': f"{attrs.get('marker_name')}_positive",
                        'label': attrs.get('target_disease'),
                        'sens': attrs.get('sens'),
                        'spec': attrs.get('spec'),
                        'note': f"Cutoff: {attrs.get('cutoff_direction')}{attrs.get('cutoff_value')}"
                    })
                    new_rows_axis2.append(row)
                
                # Add logic for phenotypic_syndrome (Axis 3) here if needed

    # Append new data to the knowledge bases
    if new_rows_axis1:
        df_new1 = pd.DataFrame(new_rows_axis1)
        df_kb1 = pd.concat([df_kb1, df_new1]).drop_duplicates().reset_index(drop=True)
        df_kb1.to_csv(KB_AXIS1_PATH, index=False)
        print(f"Added {len(df_new1)} new entries to Axis 1 knowledge base.")

    if new_rows_axis2:
        df_new2 = pd.DataFrame(new_rows_axis2)
        df_kb2 = pd.concat([df_kb2, df_new2]).drop_duplicates().reset_index(drop=True)
        df_kb2.to_csv(KB_AXIS2_PATH, index=False)
        print(f"Added {len(df_new2)} new entries to Axis 2 knowledge base.")

    print("--- Knowledge Load complete. ---")


def main():
    parser = argparse.ArgumentParser(description="Transform and load extracted knowledge.")
    parser.add_argument("--jsonl_path", required=True, help="Path to the .jsonl file from LangExtract.")
    parser.add_argument("--source_id", required=True, help="Unique identifier for the source paper (e.g., Homann2025).")
    args = parser.parse_args()
    
    transform_and_load(args.jsonl_path, args.source_id)

if __name__ == "__main__":
    main()
