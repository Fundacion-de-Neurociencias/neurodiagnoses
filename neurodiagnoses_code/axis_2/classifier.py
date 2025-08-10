import pandas as pd
import joblib
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

CSF_FEATURES = [
    'GDA', 'PDE6D', 'FN1', 'SEMA4B', 'TNFSF8', 'VSIG2', 'GLIPR1', 'IGFBP4',
    'YWHAG', 'NPTX2', 'SETMAR', 'ARRDC3'
]

def train_model(output_path="neurodiagnoses_code/axis_2/axis2_model.pkl"):
    print(f"--- Iniciando entrenamiento simulado del modelo del Eje 2 ---")
    features = CSF_FEATURES + ['some_other_protein_1', 'some_other_protein_2']
    data = pd.DataFrame(pd.np.random.rand(100, len(features)), columns=features)
    data['diagnosis'] = pd.np.random.randint(0, 5, 100)
    X = data[CSF_FEATURES]
    y = data['diagnosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = lgb.LGBMClassifier(objective='multiclass', random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Precisión del modelo de ejemplo en datos de test: {acc:.2f}")
    print(f"Guardando modelo en: {output_path}")
    joblib.dump(model, output_path)
    print("--- Entrenamiento finalizado con éxito ---")
    return output_path

def predict_probabilities(patient_data, model_path="neurodiagnoses_code/axis_2/axis2_model.pkl"):
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        print(f"Error: Archivo de modelo no encontrado. Ejecute el entrenamiento primero.")
        return None
    patient_df = pd.DataFrame(patient_data, index=[0])
    missing_cols = set(CSF_FEATURES) - set(patient_df.columns)
    if missing_cols:
        print(f"Error: Faltan columnas en los datos del paciente: {missing_cols}")
        return None
    patient_vector = patient_df[CSF_FEATURES]
    probabilities = model.predict_proba(patient_vector)
    return dict(zip(model.classes_, probabilities[0]))
