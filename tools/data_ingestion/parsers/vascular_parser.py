# --- tools/data_ingestion/parsers/vascular_parser.py ---
# This parser is responsible for extracting Cerebral Small Vessel Disease (CSVD)
# markers from neuroimaging data, inspired by Lohner et al. (2025).

import pandas as pd
from typing import Dict, Optional

def parse_vascular_data(patient_id: int, csv_path: str = 'data/simulated/vascular_data.csv') -> Optional[Dict]:
    """
    Parses a vascular metrics CSV and extracts CSVD data for a specific patient.
    """
    try:
        df = pd.read_csv(csv_path)
        patient_data = df[df['patient_id'] == patient_id]

        if patient_data.empty:
            return None

        vascular_profile = {
            "white_matter_hyperintensity_volume": float(patient_data['white_matter_hyperintensity_volume'].iloc[0]),
            "lacune_count": int(patient_data['lacune_count'].iloc[0]),
            "microbleed_count": int(patient_data['microbleed_count'].iloc[0])
        }
        return {"vascular_profile": vascular_profile}

    except FileNotFoundError:
        print(f"Warning: Vascular data file not found at {csv_path}")
        return None
    except Exception as e:
        print(f"An error occurred in vascular_parser: {e}")
        return None
