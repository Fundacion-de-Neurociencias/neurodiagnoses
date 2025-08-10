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
