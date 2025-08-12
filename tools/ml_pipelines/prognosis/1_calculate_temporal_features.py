# tools/ml_pipelines/prognosis/1_calculate_temporal_features.py
import pandas as pd
import os

# --- CONFIGURATION ---
INPUT_DATASET = 'data/simulated/longitudinal_biomarker_data.csv'
OUTPUT_FEATURES = 'data/processed/prognosis_temporal_features.csv'

def calculate_temporal_features():
    """
    Calculates key temporal features from longitudinal biomarker data,
    inspired by the methodology in Milà Alomà et al. (2025).

    This process involves:
    1. Loading longitudinal data for a cohort.
    2. For each subject, identifying the age of first positivity for key biomarkers.
    3. Calculating intervals between these events.
    4. Saving a new feature set ready for a prognosis model.
    """
    print(f"--- Starting Temporal Feature Calculation from '{INPUT_DATASET}' ---")
    
    try:
        df = pd.read_csv(INPUT_DATASET)
    except FileNotFoundError:
        print(f"ERROR: Longitudinal data not found at '{INPUT_DATASET}'.")
        return

    # Group data by each subject to process their timeline
    grouped = df.groupby('subject_id')
    
    temporal_features = []
    
    for subject_id, subject_data in grouped:
        # Find the first visit where amyloid PET became positive (status == 1)
        amyloid_positive_visits = subject_data[subject_data['amyloid_pet_status'] == 1]
        age_at_amyloid_pos = amyloid_positive_visits['visit_age'].min() if not amyloid_positive_visits.empty else None

        # Find the first visit where tau PET became positive (status == 1)
        tau_positive_visits = subject_data[subject_data['tau_pet_status'] == 1]
        age_at_tau_pos = tau_positive_visits['visit_age'].min() if not tau_positive_visits.empty else None

        # Calculate the amyloid-tau interval
        amyloid_tau_interval = None
        if age_at_amyloid_pos is not None and age_at_tau_pos is not None:
            amyloid_tau_interval = age_at_tau_pos - age_at_tau_pos

        temporal_features.append({
            'subject_id': subject_id,
            'age_at_amyloid_pos': age_at_amyloid_pos,
            'age_at_tau_pos': age_at_tau_pos,
            'amyloid_tau_interval': amyloid_tau_interval
        })

    # Create a new DataFrame with the calculated features
    features_df = pd.DataFrame(temporal_features)
    
    # Save the processed features
    os.makedirs(os.path.dirname(OUTPUT_FEATURES), exist_ok=True)
    features_df.to_csv(OUTPUT_FEATURES, index=False)
    
    print(f"--> Temporal features calculated for {len(features_df)} subjects.")
    print(f"--> Processed feature set saved to '{OUTPUT_FEATURES}'")
    print("\n--- Temporal Feature Calculation Finished Successfully ---")
    
    # Display the result for verification
    print("\n--- Generated Temporal Features ---")
    print(features_df)
    print("---------------------------------")


if __name__ == '__main__':
    calculate_temporal_features()
