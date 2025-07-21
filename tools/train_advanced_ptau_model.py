# tools/train_advanced_ptau_model.py
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import joblib
import os

def train_ptau_model_from_adni_data():
    """
    Loads the mock ADNI data, defines the pTau model pipeline from the notebook,
    trains it on the full dataset, and saves it.
    """
    # --- 1. Load Data ---
    data_path = 'tools/ml_pipelines/src/modeling/adni_csf_prediction/df_clean (2).csv'
    print(f"Loading data from '{data_path}'...")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Mock data file not found at '{data_path}'. Please run create_mock_adni.py first.")
    
    df = pd.read_csv(data_path)
    
    # --- 2. Define Features and Target ---
    # Based on the notebook's logic.
    # The notebook drops multiple columns; here we simplify by selecting the known good ones.
    # In a real scenario, we'd replicate the drop logic exactly.
    features_to_use = ['AGE', 'APOE4', 'Ventricles', 'Hippocampus', 'ADAS13_bl']
    X = df[features_to_use]
    y = df['pTau_positivity'] # Using the binary target from our mock data
    
    print("Features selected for training:", features_to_use)

    # --- 3. Define the Model Pipeline ---
    # This is extracted directly from the notebook's code.
    print("Defining model pipeline...")
    
    # Calculate class weights to handle imbalance, as done in the notebook
    neg_count = (y == 0).sum()
    pos_count = (y == 1).sum()
    class_weights = {0: (neg_count + pos_count) / (2 * neg_count), 
                     1: (neg_count + pos_count) / (2 * pos_count)}

    logreg_pipe = make_pipeline(
        StandardScaler(),
        LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight=class_weights,
            solver='saga',
            penalty='elasticnet',
            l1_ratio=0.5,
            n_jobs=-1
        )
    )

    # --- 4. Train the Model on the FULL Dataset ---
    # Unlike the notebook (which splits for testing), we train on all available data
    # to create the most robust model for deployment.
    print("Training final model on the full dataset...")
    logreg_pipe.fit(X, y)

    # --- 5. Save the Model ---
    model_dir = 'models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    # We will overwrite the previous test model with this advanced one.
    model_path = os.path.join(model_dir, 'axis2_ptau_model.joblib')
    joblib.dump(logreg_pipe, model_path)
    
    print(f"✅ Advanced pTau model successfully trained and saved to '{model_path}'")

if __name__ == "__main__":
    train_ptau_model_from_adni_data()