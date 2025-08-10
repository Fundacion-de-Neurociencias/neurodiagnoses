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
