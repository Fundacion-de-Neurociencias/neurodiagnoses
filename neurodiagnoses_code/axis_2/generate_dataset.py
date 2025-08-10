import pandas as pd
import numpy as np

# Use the feature list from our classifier
from classifier import CSF_FEATURES

# --- CONFIGURATION ---
NUM_PATIENTS = 500
OUTPUT_FILE = "neurodiagnoses_code/axis_2/axis_2_patient_data.csv"
DIAGNOSIS_CLASSES = [0, 1, 2, 3, 4] # 0:CO, 1:AD, 2:PD, 3:FTD, 4:DLB

def generate_data():
    """Generates a simulated patient dataset and saves it to a CSV file."""
    print(f"Generating {NUM_PATIENTS} simulated patient records...")
    data = np.random.rand(NUM_PATIENTS, len(CSF_FEATURES))
    df = pd.DataFrame(data, columns=CSF_FEATURES)
    diagnoses = np.random.choice(DIAGNOSIS_CLASSES, NUM_PATIENTS, p=[0.4, 0.25, 0.2, 0.08, 0.07])
    df['diagnosis'] = diagnoses
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Dataset successfully saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    generate_data()
