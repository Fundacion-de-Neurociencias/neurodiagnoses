import pandas as pd
import os

def main():
    # Asegurarse de que openpyxl está instalado para leer .xlsx
    try:
        import openpyxl
    except ImportError:
        os.system("pip install -q openpyxl")

    # Mapeo de ficheros a la información que necesitamos para procesarlos
    files_to_process = {
        "supplementary_data_1.xlsx": {'header_row': 1, 'cols': {'Gene': 'Gene ', 'Protein': 'Protein change/Splicing', 'CADD': 'CADD', 'Disease': 'Disease in AoU', 'Ancestry': 'AF (EUR)-AD (n=333)', 'rsID': 'rs ID '}},
        "supplementary_data_2.xlsx": {'header_row': 1, 'cols': {'Gene': 'Gene ', 'Protein': 'Protein change/Splicing ', 'CADD': 'CADD', 'Disease': 'Disease in UKB', 'Ancestry': 'AF (EUR)-AD (n=4051)', 'rsID': 'rs ID '}},
        "supplementary_data_3.xlsx": {'header_row': 1, 'cols': {'Gene': 'Gene ', 'Protein': 'Protein change/Splicing', 'CADD': 'CADD', 'Disease': 'Genetic Ancestry', 'Ancestry': 'Genetic Ancestry', 'rsID': 'rs ID '}}
    }
    
    output_csv = "data/knowledge_base/axis1_likelihoods.csv"
    all_kb_data = []

    for file, meta in files_to_process.items():
        print(f"--- Processing {file} ---")
        try:
            df = pd.read_excel(file, engine='openpyxl', header=meta['header_row'])
            
            # Strip column names of the DataFrame first
            df.columns = df.columns.str.strip()

            # Strip the required column names from the metadata before checking
            required_cols_stripped = [col.strip() for col in meta['cols'].values()]
            if not all(col in df.columns for col in required_cols_stripped):
                print(f"Skipping {file}: missing one of the required columns: {required_cols_stripped}")
                continue

            for _, row in df.iterrows():
                # Limpiar y validar datos
                gene = row.get(meta['cols']['Gene'].strip()) # Use stripped column name for access
                protein_change = row.get(meta['cols']['Protein'].strip()) # Use stripped column name for access
                cadd = pd.to_numeric(row.get(meta['cols']['CADD'].strip()), errors='coerce') # Use stripped column name for access
                disease = row.get(meta['cols']['Disease'].strip()) # Use stripped column name for access
                ancestry = row.get(meta['cols']['Ancestry'].strip()) # Use stripped column name for access
                rs_id = row.get(meta['cols']['rsID'].strip()) # Use stripped column name for access

                if pd.isna(cadd) or not gene or not protein_change:
                    continue

                all_kb_data.append({
                    'axis': 1,
                    'biomarker_name': f"{gene}_{protein_change}",
                    'statistic_type': 'pathogenicity_score',
                    'value': cadd,
                    'ci_lower': None, 'ci_upper': None, 'sample_size': None,
                    'primary_disease': disease,
                    'cohort_description': f"Multi-ancestry ({ancestry})",
                    'source_snippet': f"Khani_2025_PMID:39456102_rsID:{rs_id}"
                })
        except Exception as e:
            print(f"Error processing {file}: {e}")

    if all_kb_data:
        kb_df = pd.DataFrame(all_kb_data)
        kb_df.to_csv(output_csv, mode='a', header=not Path(output_csv).exists(), index=False)
        print(f"\nSUCCESS: Appended {len(all_kb_data)} new entries to {output_csv}")

if __name__ == "__main__":
    from pathlib import Path
    main()
