#!/bin/bash
set -e
set -x

# --- PASO 1: Crear el script del parser de Python para datos de ADNI ---
echo "INFO: Creating the ADNI Imaging Data Parser script..."
mkdir -p parsers

cat <<'EOF' > parsers/adni_imaging_parser.py
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
        df = pd.read_csv(args.input_csv)
    except Exception as e:
        print(f"ERROR: Failed to read CSV file. Error: {e}")
        return

    # --- 1. Análisis Estadístico: Calcular media y std por grupo de diagnóstico ---
    target_variable = 'HippocampusVolume_mm3'
    print(f"INFO: Calculating statistics for '{target_variable}' grouped by 'Diagnosis'...")
    
    # Usamos groupby y agg para calcular media y desviación estándar de una vez
    stats = df.groupby('Diagnosis')[target_variable].agg(['mean', 'std']).reset_index()
    print("--- Calculated Statistics ---")
    print(stats)
    print("---------------------------")

    # --- 2. Transformar las estadísticas al formato de la Base de Conocimiento ---
    new_kb_entries = []
    for index, row in stats.iterrows():
        diagnosis_group = row['Diagnosis']
        mean_val = row['mean']
        std_val = row['std']
        
        # Creamos una entrada para la media
        new_kb_entries.append({
            'biomarker_name': target_variable,
            'statistic_type': 'distribution_mean',
            'value': mean_val,
            'cohort_description': f"ADNI cohort - {diagnosis_group} group"
        })
        # Creamos una entrada para la desviación estándar
        new_kb_entries.append({
            'biomarker_name': target_variable,
            'statistic_type': 'distribution_std',
            'value': std_val,
            'cohort_description': f"ADNI cohort - {diagnosis_group} group"
        })

    # --- 3. Cargar (Añadir) los nuevos datos a axis3_likelihoods.csv ---
    final_kb_columns = [
        'axis', 'biomarker_name', 'statistic_type', 'value', 'ci_lower', 'ci_upper', 
        'sample_size', 'primary_disease', 'cohort_description', 'source_snippet'
    ]
    
    print(f"INFO: Writing {len(new_kb_entries)} new entries to {args.output_csv}...")
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    
    # Abrimos en modo 'append' (a) y comprobamos si el fichero es nuevo para escribir la cabecera
    is_new_file = not args.output_csv.exists()
    with open(args.output_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=final_kb_columns)
        if is_new_file:
            writer.writeheader()
        
        for entry in new_kb_entries:
            # Rellenamos el resto de campos para que coincida con nuestro schema
            full_row = {
                'axis': 3, 'biomarker_name': entry['biomarker_name'],
                'statistic_type': entry['statistic_type'], 'value': entry['value'],
                'ci_lower': '', 'ci_upper': '', 'sample_size': '',
                'primary_disease': "Alzheimer's Disease vs Control", # Contexto general
                'cohort_description': entry['cohort_description'],
                'source_snippet': 'ADNI Cortical Thickness Dataset' # Trazabilidad
            }
            writer.writerow(full_row)

    print("SUCCESS: Axis 3 Knowledge Base has been populated with neuroimaging statistics.")

if __name__ == "__main__":
    main()
EOF

# --- PASO 2: Ejecutar el Parser de Neuroimagen ---
echo "INFO: Executing the ADNI Imaging Parser..."
python parsers/adni_imaging_parser.py     --input-csv "data/raw/imaging/neuroscience_sample.csv"     --output-csv "data/knowledge_base/axis3_likelihoods.csv"

# --- PASO 3: Verificar el resultado ---
echo -e "n--- [ Contenido de la Nueva Base de Conocimiento del Eje 3 ] ---"
column -s, -t < "data/knowledge_base/axis3_likelihoods.csv"
echo "---------------------------------------------------------------"