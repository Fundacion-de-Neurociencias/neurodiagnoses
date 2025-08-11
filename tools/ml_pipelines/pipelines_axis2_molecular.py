import pandas as pd
import numpy as np
import joblib
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import random
import os

class Axis2MolecularPipeline:
    def __init__(self, data_path='data/simulated/axis2_molecular_data.csv', model_path='models/axis2_molecular_model.pkl'):
        self.data_path = data_path
        self.model_path = model_path
        self.features = ['GDA', 'PDE6D', 'FN1', 'SEMA4B', 'TNFSF8', 'YWHAG', 'NPTX2']

        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

        self.model = None

    def _generate_simulated_data(self):
        """Generates a simulated dataset for training."""
        print(f"Generating simulated molecular data at {self.data_path}...")
        data = pd.DataFrame(np.random.rand(100, len(self.features)), columns=self.features)
        data['patient_id'] = range(100)
        data['diagnosis'] = np.random.randint(0, 5, 100)
        data.to_csv(self.data_path, index=False)

    def train(self):
        """Trains and saves the Axis 2 classifier."""
        if not os.path.exists(self.data_path):
            self._generate_simulated_data()

        data = pd.read_csv(self.data_path)
        X = data[self.features]
        y = data['diagnosis']

        model = lgb.LGBMClassifier(objective='multiclass', random_state=42)
        model.fit(X, y)
        joblib.dump(model, self.model_path)
        print(f"Axis 2 model trained and saved to {self.model_path}")

    def predict(self, patient_id):
        """Predicts the molecular profile for a patient."""
        if not self.model:
            try:
                self.model = joblib.load(self.model_path)
            except FileNotFoundError:
                return "Molecular Profile cannot be determined: Axis 2 model not trained."

        patient_data = pd.DataFrame([np.random.rand(len(self.features))], columns=self.features)
        prediction_idx = self.model.predict(patient_data)[0]

        class_map = {0: 'Probable Control', 1: 'Probable AD', 2: 'Probable PD', 3: 'Probable FTD', 4: 'Probable DLB'}
        return class_map.get(prediction_idx, "Unknown Molecular Profile")