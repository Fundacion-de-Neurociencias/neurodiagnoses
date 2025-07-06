import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# Ruta donde guardar el modelo
model_path = "tools/genetics/genetic_risk_predictor.pkl"
os.makedirs(os.path.dirname(model_path), exist_ok=True)

# Crear datos de ejemplo y entrenar un modelo
X, y = make_classification(n_samples=100, n_features=4, n_classes=2, random_state=42)
model = RandomForestClassifier()
model.fit(X, y)

# Guardar el modelo
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"✅ Modelo dummy guardado en {model_path}")