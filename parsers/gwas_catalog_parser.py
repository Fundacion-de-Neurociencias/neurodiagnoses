import pandas as pd
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Parse a sample of the GWAS Catalog to populate the Axis 1 Knowledge Base.")
    parser.add_argument("--input-tsv", required=True, type=Path, help="Path to the input GWAS catalog sample TSV file.")
    parser.add_argument("--output-csv", required=True, type=Path, help="Path for the output Axis 1 KB CSV file.")
    args = parser.parse_args()

    print(f"INFO: Reading GWAS Catalog sample from {args.input_tsv}...")
    try:
        df = pd.read_csv(args.input_tsv, sep='\t', low_memory=False)
    except Exception as e:
        print(f"ERROR: Failed to read TSV file. It might be empty or corrupted. Error: {e}")
        return

    print(f"INFO: Loaded {len(df)} total associations.")

    # --- 1. Selección de Columnas Clave ---
    required_columns = {
        'DISEASE/TRAIT': 'disease_trait',
        'SNPS': 'variant_id',
        'OR or BETA': 'value',
        '95% CI (TEXT)': 'ci_text',
        'P-VALUE': 'p_value',
        'REPORTED GENE(S)': 'reported_gene',
        'PUBMEDID': 'pubmed_id'
    }
    df = df[list(required_columns.keys())].rename(columns=required_columns)

    # --- 2. Filtrado por Enfermedades de Interés ---
    # Para este PoC, buscamos cualquier rasgo que contenga 'Alzheimer'
    # El `case=False` hace que la búsqueda no distinga mayúsculas/minúsculas.
    ndd_df = df[df['disease_trait'].str.contains("Alzheimer", case=False, na=False)].copy()
    print(f"INFO: Found {len(ndd_df)} associations related to 'Alzheimer'.")

    if ndd_df.empty:
        print("WARNING: No Alzheimer-related associations found in the sample.")
        return

    # --- 3. Transformación y Limpieza ---
    # El Odds Ratio es nuestro 'valor'. Nos aseguramos de que sea numérico.
    ndd_df['value'] = pd.to_numeric(ndd_df['value'], errors='coerce')
    # Eliminamos filas donde el Odds Ratio no sea un número válido
    ndd_df.dropna(subset=['value'], inplace=True)
    
    # Añadimos las columnas que faltan en nuestro schema de KB
    ndd_df['axis'] = 1
    ndd_df['statistic_type'] = 'odds_ratio'
    # (Simplificación: Por ahora no parseamos el CI, lo añadiremos en el siguiente paso)
    ndd_df['ci_lower'] = ''
    ndd_df['ci_upper'] = ''

    # --- 4. Carga al formato final de la KB ---
    final_kb_columns = [
        'biomarker_name', # Usaremos 'variant_id' para esto
        'statistic_type',
        'value',
        'ci_lower',
        'ci_upper',
        'primary_disease', # Usaremos 'disease_trait' para esto
        'source_snippet' # Usaremos 'pubmed_id' para esto
    ]
    # Reordenamos y renombramos para que coincida con nuestro formato final
    ndd_df.rename(columns={'variant_id': 'biomarker_name', 'disease_trait': 'primary_disease', 'pubmed_id': 'source_snippet'}, inplace=True)
    
    # Seleccionamos solo las columnas que necesitamos para el CSV final (simplificado por ahora)
    output_df = ndd_df[['biomarker_name', 'statistic_type', 'value', 'ci_lower', 'ci_upper', 'primary_disease', 'source_snippet']]

    print(f"INFO: Writing {len(output_df)} processed entries to {args.output_csv}...")
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(args.output_csv, index=False)

    print("SUCCESS: Axis 1 Knowledge Base CSV has been created/updated from the GWAS sample.")


if __name__ == "__main__":
    main()
