import pandas as pd
import argparse
from pathlib import Path
import re

def parse_ci_text(ci_string):
    if not isinstance(ci_string, str): return None, None
    numbers = re.findall(r"(\d+\.?\d*)", ci_string)
    return (float(numbers[0]), float(numbers[1])) if len(numbers) >= 2 else (None, None)

def main():
    parser = argparse.ArgumentParser(description="Parse GWAS Catalog to populate Axis 1 KB.")
    parser.add_argument("--input-tsv", required=True, type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    args = parser.parse_args()

    print(f"INFO: Reading GWAS Catalog sample from {args.input_tsv}...")
    df = pd.read_csv(args.input_tsv, sep='\t', low_memory=False)

    required_columns = {
        'DISEASE/TRAIT': 'primary_disease',
        'SNPS': 'biomarker_name',
        'OR or BETA': 'value',
        '95% CI (TEXT)': 'ci_text',
        'PUBMEDID': 'source_snippet' # <-- ¡CORRECCIÓN CLAVE!
    }
    df = df[list(required_columns.keys())].rename(columns=required_columns)

    ndd_df = df[df['primary_disease'].str.contains("Alzheimer|Parkinson|Dementia", case=False, na=False)].copy()
    print(f"INFO: Found {len(ndd_df)} associations related to NDDs.")

    ndd_df['value'] = pd.to_numeric(ndd_df['value'], errors='coerce')
    ndd_df.dropna(subset=['value'], inplace=True)
    
    ci_bounds = ndd_df['ci_text'].apply(parse_ci_text)
    ndd_df['ci_lower'] = ci_bounds.apply(lambda x: x[0])
    ndd_df['ci_upper'] = ci_bounds.apply(lambda x: x[1])

    ndd_df['statistic_type'] = 'odds_ratio'
    # La columna 'source_snippet' ahora existe y está correctamente nombrada
    
    final_columns = ['biomarker_name', 'statistic_type', 'value', 'ci_lower', 'ci_upper', 'primary_disease', 'source_snippet']
    output_df = ndd_df[final_columns]

    print(f"INFO: Writing {len(output_df)} processed entries to {args.output_csv}...")
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(args.output_csv, index=False)
    print("SUCCESS: Axis 1 KB CSV has been correctly created with source_snippet data.")

if __name__ == "__main__":
    main()
