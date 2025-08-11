# tools/data_ingestion/orchestrator.py
import json
import os
from datetime import datetime
from dataclasses import asdict

# Import parsers
from tools.data_ingestion.parsers.clinical_parser import parse_clinical_data
from tools.data_ingestion.parsers.imaging_parser import parse_imaging_data
from tools.data_ingestion.parsers.genomics_parser import parse_genomics_data
from tools.data_ingestion.parsers.cornblath_adapter import parse_cornblath_patient

def ingest_cornblath_patient(patient_id, data_dir, output_dir='patient_database/cornblath'):
    """
    Orchestrates the ingestion of a single patient from the Cornblath dataset.
    """
    print(f"--- Starting Cornblath ingestion for patient: {patient_id} ---")
    print(f"Searching for data in: {data_dir}")

    # Call the specialized parser for the Cornblath dataset
    parsed_data = parse_cornblath_patient(patient_id, final_json['metadata'], data_dir)

    if not parsed_data:
        print(f"!!! Ingestion failed for patient {patient_id}.")
        return

    # Assemble the final JSON with metadata
    final_json = {
        "patient_id": str(patient_id),
        "metadata": {
            "schema_version": "1.1",
            "ingestion_timestamp": datetime.now().isoformat(),
            "source_dataset": "Cornblath2020"
        }
    }

    # Save the final JSON file
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{patient_id}.json")
    with open(output_path, 'w') as f:
        json.dump(asdict(parsed_data), f, indent=2)

    print(f"✅ Ingestion complete. Patient data saved to: {output_path}")
    return output_path

if __name__ == '__main__':
    # --- MODIFICATION ---
    # Use the user-provided local path for the Cornblath dataset
    cornblath_source_path = r'C:\Users\usuario\Downloads\SourceData'

    sample_patient_id_cornblath = 4101131 

    ingest_cornblath_patient(
        patient_id=sample_patient_id_cornblath,
        data_dir=cornblath_source_path
    )