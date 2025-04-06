import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv("../data/test_biomarkers.csv")  # Ensure dataset is uploaded to /data/

# Features (biomarkers) and target (diagnosis: 0 = healthy, 1 = neurodegenerative)
X = data[['Amyloid-beta', 'Tau', 'NFL']]
y = data['Diagnosis']

# Split into training/testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate Model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save trained model
joblib.dump(model, "../models/biomarker_model.pkl")

print("Model saved as biomarker_model.pkl")
