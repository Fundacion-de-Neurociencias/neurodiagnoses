import pandas as pd
import argparse
from pathlib import Path
import csv

def main():
    parser = argparse.ArgumentParser(description="Parse ADNI imaging data to populate the Axis 3 Knowledge Base.")
    parser.add_argument("--input-csv", required=True, type=Path, help="Path to the input ADNI sample CSV file.")
    parser.add_argument("--output-csv", required=True, type=Path, help="Path for the output Axis 3 KB CSV file.")
    args = parser.parse_args()

    print(f"INFO: Reading ADNI imaging sample from {args.input_csv}...")
    try:
        # Usamos un nombre de fichero genérico que el agente creó
        df = pd.read_csv(args.input_csv)
    except Exception as e:
        print(f"ERROR: Failed to read CSV file. Error: {e}")
        return

    # --- 1. Análisis Estadístico ---
    target_variable = 'HippocampusVolume_mm3'
    print(f"INFO: Calculating statistics for '{target_variable}' grouped by 'Diagnosis'...")
    
    stats = df.groupby('Diagnosis')[target_variable].agg(['mean', 'std']).reset_index()
    print("--- Calculated Statistics ---")
    print(stats)
    print("---------------------------")

    # --- 2. Transformar a formato de la KB ---
    new_kb_entries = []
    for index, row in stats.iterrows():
        diagnosis_group = row['Diagnosis']
        # Ignoramos grupos con un solo miembro donde no se puede calcular std
        if pd.isna(row['std']):
            continue
            
        new_kb_entries.append({
            'biomarker_name': target_variable,
            'statistic_type': 'distribution_mean',
            'value': row['mean'],
            'cohort_description': f"ADNI cohort - {diagnosis_group} group"
        })
        new_kb_entries.append({
            'biomarker_name': target_variable,
            'statistic_type': 'distribution_std',
            'value': row['std'],
            'cohort_description': f"ADNI cohort - {diagnosis_group} group"
        })

    # --- 3. Cargar (Añadir) a axis3_likelihoods.csv ---
    final_kb_columns = [
        'axis', 'biomarker_name', 'statistic_type', 'value', 'ci_lower', 'ci_upper', 
        'sample_size', 'primary_disease', 'cohort_description', 'source_snippet'
    ]
    
    print(f"INFO: Writing {len(new_kb_entries)} new entries to {args.output_csv}...")
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    
    is_new_file = not args.output_csv.exists()
    with open(args.output_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=final_kb_columns)
        if is_new_file:
            writer.writeheader()
        
        for entry in new_kb_entries:
            full_row = {
                'axis': 3, 'biomarker_name': entry['biomarker_name'],
                'statistic_type': entry['statistic_type'], 'value': entry['value'],
                'primary_disease': "Alzheimer's Disease vs Control",
                'cohort_description': entry['cohort_description'],
                'source_snippet': 'ADNI Cortical Thickness Sample Dataset'
            }
            writer.writerow(full_row)

    print("SUCCESS: Axis 3 KB has been populated with neuroimaging statistics.")

if __name__ == "__main__":
    main()
