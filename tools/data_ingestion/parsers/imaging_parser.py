# tools/data_ingestion/parsers/imaging_parser.py
import pandas as pd

def parse_imaging_data(patient_id, csv_path):
    """
    Parses an imaging metrics CSV and extracts data for a specific patient.
    """
    try:
        df = pd.read_csv(csv_path)
        patient_data = df[df['patient_id'] == patient_id]

        if patient_data.empty:
            return None

        # Build the 'imaging_data' block of the schema
        output = {
            "raw_data_paths": {},
            "derived_metrics": {}
        }

        # Dynamically populate paths and metrics if columns exist
        if 't1_mri_nifti_path' in patient_data.columns:
            output["raw_data_paths"]["t1_mri_nifti"] = str(patient_data['t1_mri_nifti_path'].iloc[0])
        
        if 'hippocampal_volume_norm' in patient_data.columns:
            output["derived_metrics"]["hippocampal_volume_norm"] = float(patient_data['hippocampal_volume_norm'].iloc[0])
        if 'cortical_thickness_avg' in patient_data.columns:
            output["derived_metrics"]["cortical_thickness_avg"] = float(patient_data['cortical_thickness_avg'].iloc[0])
            
        return output

    except Exception as e:
        print(f"An error occurred in imaging_parser: {e}")
        return None
