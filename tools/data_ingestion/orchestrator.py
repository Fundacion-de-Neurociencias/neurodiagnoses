# tools/data_ingestion/orchestrator.py
import json
import os
from datetime import datetime

from tools.data_ingestion.parsers.clinical_parser import parse_clinical_data
from tools.data_ingestion.parsers.imaging_parser import parse_imaging_data
from tools.data_ingestion.parsers.genomics_parser import parse_genomics_data

def run_ingestion(patient_id, clinical_csv_path=None, imaging_csv_path=None, genomics_csv_path=None, output_dir="."):
    """Orchestrates the data ingestion process for a single patient."""
    print(f"--- Starting ingestion for patient: {patient_id} ---")

    patient_json = {
        "patient_id": patient_id,
        "metadata": { "schema_version": "1.1", "ingestion_timestamp": datetime.now().isoformat() },
        "clinical_data": None, "genetic_data": None, "imaging_data": None, "omics_data": None
    }

    if clinical_csv_path:
        patient_json["clinical_data"] = parse_clinical_data(patient_id, clinical_csv_path)
    if imaging_csv_path:
        patient_json["imaging_data"] = parse_imaging_data(patient_id, imaging_csv_path)
    if genomics_csv_path:
        patient_json["genetic_data"] = parse_genomics_data(patient_id, genomics_csv_path)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{patient_id}.json")
    with open(output_path, 'w') as f:
        json.dump(patient_json, f, indent=2)
        
    print(f"✅ Ingestion complete for {patient_id}. Saved to: {output_path}")
    return output_path

if __name__ == '__main__':
    # --- MODIFICATION ---
    # Process all patients from our sample data to create a full dataset
    patients_to_process = ['ND_001', 'ND_002', 'ND_003']
    print(f"Starting batch ingestion for {len(patients_to_process)} patients...")
    
    for patient in patients_to_process:
        run_ingestion(patient_id=patient, 
                      clinical_csv_path='clinical_data.csv', 
                      imaging_csv_path='imaging_metrics.csv',
                      genomics_csv_path='genomics_summary.csv',
                      output_dir='patient_database')
    
    print("\nBatch ingestion finished.")