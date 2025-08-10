import pandas as pd
import numpy as np
from classifier import NEURO_FEATURES

NUM_PATIENTS = 500
OUTPUT_FILE = "neurodiagnoses_code/axis_3/axis_3_neuroimaging_data.csv"
PHENOTYPE_CLASSES = [0, 1] # 0: Tau-positive, 1: TDP-43

def generate_data():
    """Generates a simulated neuroimaging dataset and saves it to a CSV file."""
    print(f"Generating {NUM_PATIENTS} simulated neuroimaging records...")
    data = np.random.rand(NUM_PATIENTS, len(NEURO_FEATURES))
    df = pd.DataFrame(data, columns=NEURO_FEATURES)
    phenotypes = np.random.choice(PHENOTYPE_CLASSES, NUM_PATIENTS, p=[0.6, 0.4])
    df['phenotype'] = phenotypes
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Dataset successfully saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    generate_data()
