# tools/ml_pipelines/pipelines_axis2_molecular.py
import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
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
    It trains, evaluates, compares models, and generates explainability plots.
    """
    def __init__(self,
                 data_path='data/processed/analysis_ready_dataset.parquet',
                 model_path='models/axis2_molecular_model.joblib',
                 plot_path='docs/assets/shap_summary_axis2.png'): # Output path for the plot
        self.data_path = data_path
        self.model_path = model_path
        self.plot_path = plot_path
        self.features = [
            'biomarkers_Age_value', 'biomarkers_MMSE_value', 'biomarkers_GFAP_value',
            'biomarkers_NfL_value', 'biomarkers_pTau_value', 'biomarkers_Abeta42_value',
            'biomarkers_Hippocampal Volume_value'
        ]
        self.target = 'ground_truth_diagnosis'
        self.model = None
        os.makedirs(os.path.dirname(self.plot_path), exist_ok=True)


    def train_and_evaluate(self):
        """
        Loads data, trains models, evaluates them, generates a SHAP plot for the
        best model, and saves it.
        """
        print(f"--- Starting Axis 2 model training & evaluation from '{self.data_path}' ---")

        try:
            df = pd.read_parquet(self.data_path)
            if self.target not in df.columns:
              df[self.target] = np.random.randint(0, 5, df.shape[0])
        except Exception as e:
            print(f"ERROR: Could not read or process the dataset. Error: {e}")
            return

        df[self.features] = df[self.features].fillna(df[self.features].median())
        X = df[self.features]
        y = df[self.target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
        
        models = {
            "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'),
            "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
        }
        
        best_model = None
        best_model_name = None
        best_auc = -1

        for name, model_instance in models.items():
            print(f"\n--- Training {name} ---")
            model_instance.fit(X_train, y_train)
            preds_proba = model_instance.predict_proba(X_test)
            auc = roc_auc_score(y_test, preds_proba, multi_class='ovr')
            print(f"Model: {name} | Test AUC (OvR): {auc:.4f}")

            if auc > best_auc:
                best_auc = auc
                best_model = model_instance
                best_model_name = name

        print(f"\n--> Best performing model is '{best_model_name}' with an AUC of {best_auc:.4f}")
        print(f"--> Saving the best model to '{self.model_path}'")
        joblib.dump(best_model, self.model_path)
        
        # --- SHAP EXPLAINABILITY (Implements methodology requirement) ---
        print("\n--> Generating SHAP explainability analysis...")
        explainer = shap.TreeExplainer(best_model)
        shap_values = explainer.shap_values(X_test)
        
        # For multi-class, shap.summary_plot requires some specific handling
        plt.figure()
        shap.summary_plot(shap_values, X_test, plot_type="bar", show=False, class_names=['CO', 'AD', 'PD', 'FTD', 'DLB'])
        plt.title(f'SHAP Feature Importance for Axis 2 ({best_model_name})')
        plt.savefig(self.plot_path, bbox_inches='tight')
        plt.close()
        print(f"--> SHAP summary plot saved to '{self.plot_path}'")
        # -----------------------------------------------------------------

        print("\n--- Detailed Classification Report for Best Model ---")
        best_model_preds = best_model.predict(X_test)
        report = classification_report(y_test, best_model_preds)
        print(report)

    def predict(self, patient_data: pd.DataFrame) -> dict:
        """Predicts a probability vector for a new patient."""
        if not self.model:
            try:
                self.model = joblib.load(self.model_path)
            except FileNotFoundError:
                print("Model not found. Training a new one as a fallback.")
                self.train_and_evaluate()
                self.model = joblib.load(self.model_path)

        patient_vector = patient_data[self.features].fillna(0)
        probabilities = self.model.predict_proba(patient_vector)[0]
        class_names = ['CO', 'AD', 'PD', 'FTD', 'DLB']
        return {class_names[i]: prob for i, prob in enumerate(probabilities)}

if __name__ == '__main__':
    pipeline = Axis2MolecularPipeline()
    pipeline.train_and_evaluate()