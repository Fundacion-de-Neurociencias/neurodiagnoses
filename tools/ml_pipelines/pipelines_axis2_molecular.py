# tools/ml_pipelines/pipelines_axis2_molecular.py
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score
import os
import sys

# Add project root for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from tools.ontology.neuromarker import Biomarker

class Axis2MolecularPipeline:
    """
    A research-grade pipeline for the Axis 2 (Molecular) classifier.
    It trains, evaluates, and compares multiple models, saving the best one.
    The prediction output is a probability vector for co-pathology analysis.
    """
    def __init__(self, 
                 data_path='data/processed/analysis_ready_dataset.parquet',
                 model_path='models/axis2_molecular_model.joblib'):
        self.data_path = data_path
        self.model_path = model_path
        # Define features based on the Neuromarker ontology fields
        self.features = [
            'biomarkers_Age_value', 'biomarkers_MMSE_value', 'biomarkers_GFAP_value',
            'biomarkers_NfL_value', 'biomarkers_pTau_value', 'biomarkers_Abeta42_value',
            'biomarkers_Hippocampal Volume_value'
        ]
        # The target variable needs to be defined based on the dataset's ground truth column
        self.target = 'ground_truth_diagnosis' # This column needs to exist in the dataset
        self.model = None

    def train_and_evaluate(self):
        """
        Loads the processed data, trains multiple models, evaluates them,
        and saves the best performing one.
        """
        print(f"--- Starting Axis 2 model training & evaluation from '{self.data_path}' ---")

        try:
            df = pd.read_parquet(self.data_path)
            # Placeholder for target variable - in a real scenario this would be the neuropath diagnosis
            df[self.target] = np.random.randint(0, 5, df.shape[0])
        except Exception as e:
            print(f"ERROR: Could not read or process the dataset at {self.data_path}. Error: {e}")
            return

        # Simple feature engineering: handle potential missing values
        df[self.features] = df[self.features].fillna(df[self.features].median())
        
        X = df[self.features]
        y = df[self.target]
        
        # Stratify split is important for potentially imbalanced datasets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
        
        models = {
            "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'),
            "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
        }
        
        best_model_name = None
        best_auc = -1

        for name, model in models.items():
            print(f"--- Training {name} ---")
            model.fit(X_train, y_train)
            preds_proba = model.predict_proba(X_test)
            
            # Use One-vs-Rest for multiclass AUC calculation
            auc = roc_auc_score(y_test, preds_proba, multi_class='ovr')
            print(f"Model: {name} | Test AUC (OvR): {auc:.4f}")

            if auc > best_auc:
                best_auc = auc
                best_model_name = name

        print(f"--> Best performing model is '{best_model_name}' with an AUC of {best_auc:.4f}")
        
        print(f"--> Saving the best model to '{self.model_path}'")
        joblib.dump(models[best_model_name], self.model_path)
        
        print("\n--- Detailed Classification Report for Best Model ---")
        best_model_preds = models[best_model_name].predict(X_test)
        report = classification_report(y_test, best_model_preds)
        print(report)

    def predict(self, patient_data: pd.DataFrame) -> dict:
        """
        Predicts a probability vector for a new patient.

        Returns:
            A dictionary of disease probabilities, allowing for co-pathology analysis.
        """
        if not self.model:
            try:
                self.model = joblib.load(self.model_path)
            except FileNotFoundError:
                print("Model not found. Training a new one as a fallback.")
                self.train_and_evaluate()
                self.model = joblib.load(self.model_path)

        # Ensure patient data has the correct features
        patient_vector = patient_data[self.features].fillna(0) # Basic imputation
        
        probabilities = self.model.predict_proba(patient_vector)[0]
        
        # Map probabilities to class names
        class_names = ['CO', 'AD', 'PD', 'FTD', 'DLB'] # Assuming 5 classes
        return {class_names[i]: prob for i, prob in enumerate(probabilities)}

if __name__ == '__main__':
    # This block allows the script to be run directly to train the models
    pipeline = Axis2MolecularPipeline()
    pipeline.train_and_evaluate()
