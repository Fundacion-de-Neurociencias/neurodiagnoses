import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load the sample dataset
data_path = "C:/Users/usuario/neurodiagnoses/models/data/sample_data.csv"
data = pd.read_csv(data_path)
data["sex"] = data["sex"].map({"M": 0, "F": 1})  # Convert 'M' -> 0, 'F' -> 1

# Prepare input (X) and target (y)
X = data.drop(columns=["clinical_score"])  # Remove the target variable
y = data["clinical_score"]

# Train a simple model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model as model.pkl
model_filename = "C:/Users/usuario/neurodiagnoses/models/model.pkl"
joblib.dump(model, model_filename)

print("✅ Model saved as model.pkl")
