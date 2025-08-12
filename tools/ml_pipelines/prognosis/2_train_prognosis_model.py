# tools/ml_pipelines/prognosis/2_train_prognosis_model.py
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --- CONFIGURATION ---
TEMPORAL_FEATURES_PATH = 'data/processed/prognosis_temporal_features.csv'
OUTCOMES_PATH = 'data/simulated/longitudinal_outcomes.csv'
MODEL_OUTPUT_PATH = 'models/prognosis/prognosis_model.joblib'

def train_prognosis_model():
    """
    Trains a model to predict future cognitive decline, inspired by
    Colautti et al. (2025) and using features from Milà Alomà et al. (2025).

    This process involves:
    1. Loading the pre-calculated temporal features.
    2. Loading the longitudinal outcome data.
    3. Merging them into a final training dataset.
    4. Training a classifier to predict the future outcome.
    5. Saving the trained prognosis model.
    """
    print(f"--- Starting Prognosis Model Training ---")
    
    try:
        features_df = pd.read_csv(TEMPORAL_FEATURES_PATH)
        outcomes_df = pd.read_csv(OUTCOMES_PATH)
    except FileNotFoundError as e:
        print(f"ERROR: A required data file is missing. Details: {e}")
        print("Please run '1_calculate_temporal_features.py' first.")
        return

    # Merge the features and the target variable into one dataset
    training_df = pd.merge(features_df, outcomes_df, on='subject_id')
    
    # Handle missing values simply for this PoC (e.g., fill with median)
    training_df = training_df.fillna(training_df.median())
    
    print(f"--> Created training dataset with {training_df.shape[0]} subjects.")

    # Define features and target
    features = ['age_at_amyloid_pos', 'age_at_tau_pos', 'amyloid_tau_interval']
    target = 'cognitive_status_at_follow_up'
    
    X = training_df[features]
    y = training_df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train a simple RandomForest model for this PoC
    print("--> Training RandomForestClassifier for prognosis prediction...")
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    print(f"  > Model accuracy on test set: {accuracy:.2f}")

    # Save the trained model artifact
    os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH), exist_ok=True)
    joblib.dump(model, MODEL_OUTPUT_PATH)
    print(f"--> Prognosis model artifact saved to '{MODEL_OUTPUT_PATH}'")
    print("\n--- Prognosis Model Training Finished Successfully ---")

if __name__ == '__main__':
    # Ensure the input feature file exists before running
    if not os.path.exists(TEMPORAL_FEATURES_PATH):
        print("Temporal features file not found. Running the calculation script first...")
        from tools.ml_pipelines.prognosis.one_calculate_temporal_features import calculate_temporal_features
        calculate_temporal_features()
    
    train_prognosis_model()
