# tools/train_advanced_ttau_model.py
import pandas as pd
import os
import xgboost as xgb
import joblib

def train_ttau_model_from_adni_data():
    """
    Loads mock ADNI data, trains an XGBoost model for tTau positivity, and saves it.
    """
    # --- 1. Load Data ---
    data_path = 'tools/ml_pipelines/src/modeling/adni_csf_prediction/df_clean (2).csv'
    print(f"Loading data from '{data_path}'...")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Mock data file not found at '{data_path}'. Please run create_mock_adni.py first.")

    df = pd.read_csv(data_path)

    # --- 2. Define Features and Target ---
    # We'll use the same robust features as the pTau model for consistency.
    features_to_use = ['AGE', 'APOE4', 'Ventricles', 'Hippocampus', 'ADAS13_bl']
    X = df[features_to_use]
    # In a real scenario, the target for tTau might be different. 
    # Here, we'll use the pTau positivity as a proxy for demonstration.
    y = df['pTau_positivity'] 

    print("Features selected for training:", features_to_use)

    # --- 3. Define the XGBoost Model ---
    # The notebook's README mentioned XGBoost as the best model for tTau.
    print("Defining XGBoost model pipeline...")

    # Handle class imbalance, critical for triage models like this
    scale_pos_weight = (y == 0).sum() / (y == 1).sum()

    xgb_model = xgb.XGBClassifier(
        objective='binary:logistic',
        eval_metric='logloss',
        scale_pos_weight=scale_pos_weight,
        use_label_encoder=False,
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    # --- 4. Train the Model ---
    print("Training final tTau model on the full dataset...")
    xgb_model.fit(X, y)

    # --- 5. Save the Model ---
    model_dir = 'models'
    model_path = os.path.join(model_dir, 'axis2_ttau_model.joblib')
    joblib.dump(xgb_model, model_path)

    print(f"✅ Advanced tTau (XGBoost) model successfully trained and saved to '{model_path}'")

if __name__ == "__main__":
    train_ttau_model_from_adni_data()