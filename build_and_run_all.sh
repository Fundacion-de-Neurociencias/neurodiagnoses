#!/bin/bash
# Gemini Master Script to build the entire project from scratch.
set -e

echo "--- MASTER SCRIPT: STARTING BUILD ---"

# === STEP 1: Create Axis 2 Files ===
echo "--> Creating Axis 2 modules..."
mkdir -p neurodiagnoses_code/axis_2

cat <<EOF > neurodiagnoses_code/axis_2/generate_dataset.py
import pandas as pd
import numpy as np

# Use the feature list from our classifier
from .classifier import CSF_FEATURES

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
EOF

cat <<EOF > neurodiagnoses_code/axis_2/classifier.py
import pandas as pd
import joblib
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# --- Feature Definition (Proteins) ---
CSF_FEATURES = [
    'GDA', 'PDE6D', 'FN1', 'SEMA4B', 'TNFSF8', 'VSIG2', 'GLIPR1', 'IGFBP4',
    'YWHAG', 'NPTX2', 'SETMAR', 'ARRDC3'
]

def train_model(
    data_path="neurodiagnoses_code/axis_2/axis_2_patient_data.csv",
    output_path="neurodiagnoses_code/axis_2/axis2_model.pkl"
):
    """Trains a LightGBM model from a CSV patient dataset."""
    print(f"--- Starting Axis 2 model training from CSV data ---")
    try:
        data = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"ERROR: Data file not found at {data_path}")
        return None
    X = data[CSF_FEATURES]
    y = data['diagnosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    print("Training LightGBM classifier...")
    model = lgb.LGBMClassifier(objective='multiclass', random_state=42)
    model.fit(X_train, y_train)
    print("Evaluating model on the test set...")
    preds = model.predict(X_test)
    report = classification_report(y_test, preds, target_names=['CO', 'AD', 'PD', 'FTD', 'DLB'])
    print("--- Classification Report ---")
    print(report)
    print("-----------------------------")
    print(f"Saving trained model to: {output_path}")
    joblib.dump(model, output_path)
    print("--- Model training completed successfully ---")
    return output_path

def predict_probabilities(patient_data, model_path="neurodiagnoses_code/axis_2/axis2_model.pkl"):
    """Loads a pre-trained model and predicts probabilities for a new patient."""
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        print(f"ERROR: Model file not found at {model_path}. Please run training first.")
        return None
    patient_df = pd.DataFrame(patient_data, index=[0])
    missing_cols = set(CSF_FEATURES) - set(patient_df.columns)
    if missing_cols:
        print(f"ERROR: The following columns are missing from patient data: {missing_cols}")
        return None
    patient_vector = patient_df[CSF_FEATURES]
    probabilities = model.predict_proba(patient_vector)
    return dict(zip(model.classes_, probabilities[0]))

if __name__ == '__main__':
    train_model()
EOF

# === STEP 2: Create Axis 3 Files ===
echo "--> Creating Axis 3 modules..."
mkdir -p neurodiagnoses_code/axis_3

cat <<EOF > neurodiagnoses_code/axis_3/generate_axis3_dataset.py
import pandas as pd
import numpy as np
from .classifier import NEURO_FEATURES

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
EOF

cat <<EOF > neurodiagnoses_code/axis_3/classifier.py
import pandas as pd
import joblib
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

NEURO_FEATURES = [
    'hippocampal_volume',
    'cortical_thickness_temporal',
    'ventricular_volume'
]

def train_model(
    data_path="neurodiagnoses_code/axis_3/axis_3_neuroimaging_data.csv",
    output_path="neurodiagnoses_code/axis_3/axis3_model.pkl"
):
    """Trains a LightGBM model from a neuroimaging CSV dataset."""
    print(f"--- Starting Axis 3 model training from CSV data ---")
    data = pd.read_csv(data_path)
    X = data[NEURO_FEATURES]
    y = data['phenotype']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    print("Training LightGBM classifier for Axis 3...")
    model = lgb.LGBMClassifier(objective='binary', random_state=42)
    model.fit(X_train, y_train)
    print("Evaluating Axis 3 model on the test set...")
    preds = model.predict(X_test)
    report = classification_report(y_test, preds, target_names=['Tau-positive', 'TDP-43'])
    print("--- Axis 3 Classification Report ---")
    print(report)
    print("------------------------------------")
    print(f"Saving trained model to: {output_path}")
    joblib.dump(model, output_path)
    print("--- Axis 3 Model training completed successfully ---")
    return output_path

def predict_probabilities(patient_data, model_path="neurodiagnoses_code/axis_3/axis3_model.pkl"):
    """Loads a pre-trained model and predicts phenotype probabilities."""
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        print(f"ERROR: Model file not found at {model_path}. Please run training first.")
        return None
    patient_df = pd.DataFrame(patient_data, index=[0])
    patient_vector = patient_df[NEURO_FEATURES]
    probabilities = model.predict_proba(patient_vector)
    return dict(zip(model.classes_, probabilities[0]))

if __name__ == '__main__':
    train_model()
EOF

# === STEP 3: Create Axis 1 Files ===
echo "--> Creating Axis 1 module..."
mkdir -p neurodiagnoses_code/axis_1

cat <<EOF > neurodiagnoses_code/axis_1/classifier.py
import numpy as np

PATHOGENIC_MAP = {
    "PSEN1": "AD", "PSEN2": "AD", "APP": "AD",
    "HTT": "Huntington's",
    "GRN": "FTD", "MAPT": "FTD", "C9orf72": "FTD/ALS"
}
SPECIFIC_RISK_MAP = {
    "APOE_e4": {"disease": "AD", "multiplier": 1.5}
}
NON_SPECIFIC_RISK_MAP = {
    "APOE_e4_shared_signature": {"diseases": ["AD", "PD", "FTD"], "boost": 0.1}
}
DISEASE_CLASSES = ['AD', 'PD', 'FTD', 'DLB', 'CO', "Huntington's", 'FTD/ALS']

def predict_etiology(patient_genetics: dict) -> dict:
    """Predicts disease probabilities based on a rules-engine for genetic variants."""
    probabilities = {disease: 1.0 / len(DISEASE_CLASSES) for disease in DISEASE_CLASSES}
    genetics = patient_genetics.get("genetics", {})
    for variant in genetics.get("pathogenic_variants", []):
        variant_gene = variant.split('_')[0]
        if variant_gene in PATHOGENIC_MAP:
            disease = PATHOGENIC_MAP[variant_gene]
            for d in probabilities:
                probabilities[d] = 0.01
            probabilities[disease] = 1.0 - (0.01 * (len(DISEASE_CLASSES) - 1))
            return probabilities
    for variant in genetics.get("disease_specific_risk", []):
        if variant in SPECIFIC_RISK_MAP:
            risk_info = SPECIFIC_RISK_MAP[variant]
            disease = risk_info["disease"]
            multiplier = risk_info["multiplier"]
            if disease in probabilities:
                probabilities[disease] *= multiplier
    for variant in genetics.get("non_specific_risk", []):
        if variant in NON_SPECIFIC_RISK_MAP:
            risk_info = NON_SPECIFIC_RISK_MAP[variant]
            for disease in risk_info["diseases"]:
                if disease in probabilities:
                    probabilities[disease] += risk_info["boost"]
    total_prob = sum(probabilities.values())
    if total_prob > 0:
        for disease in probabilities:
            probabilities[disease] /= total_prob
    return probabilities
EOF

# === STEP 4: Install Dependencies and Run Orchestrator ===
echo "--> Installing Python dependencies..."
pip install -r requirements.txt

echo "--> Running the Python orchestrator script..."
python3 orchestrator.py

echo "--- MASTER SCRIPT: BUILD AND EXECUTION COMPLETE ---"