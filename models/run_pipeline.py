import pandas as pd

def load_and_clean_data(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path)
    
    # Simple cleaning: For example, check for missing values
    data = data.dropna()
    
    return data

def select_features(data):
    # Detectar dinámicamente qué columnas pertenecen a cada categoría
    feature_blocks = {
        "clinical": [],
        "plasma": [],
        "MRI": [],
        "PET": [],
        "functional": []
    }

    for column in data.columns:
        col_name = column.lower()
        if "plasma" in col_name:
            feature_blocks["plasma"].append(column)
        elif "mri" in col_name:
            feature_blocks["MRI"].append(column)
        elif "pet" in col_name:
            feature_blocks["PET"].append(column)
        elif "clinical" in col_name or column in ["age", "sex", "education"]:
            feature_blocks["clinical"].append(column)
        elif "fmri" in col_name or "eeg" in col_name:
            feature_blocks["functional"].append(column)

    # Seleccionar automáticamente todas las variables detectadas como X (entrada del modelo)
    X = data[feature_blocks["plasma"] + feature_blocks["MRI"] + feature_blocks["PET"] + feature_blocks["functional"]]
    
    # Usamos la última columna como variable objetivo (y), asegurándonos de que no sea parte de X
    y = data.iloc[:, -1]

    return X, y

def train_model(X, y):
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(X, y)
    return model

def evaluate_model(model, X, y):
    from sklearn.metrics import mean_squared_error, r2_score
    predictions = model.predict(X)
    mse = mean_squared_error(y, predictions)
    r2 = r2_score(y, predictions)
    print("Mean Squared Error:", mse)
    print("R-squared:", r2)

def run_pipeline():
    # Update the file path to where you saved sample_data.csv
    file_path = "data/sample_data.csv"
    
    # Step 1: Load and clean data
    data = load_and_clean_data(file_path)
    print("Data Loaded:")
    print(data.head())
    
    # Step 2: Select features
    X, y = select_features(data)
    
    # Step 3: Train the model
    model = train_model(X, y)
    
    # Step 4: Evaluate the model
    evaluate_model(model, X, y)

if __name__ == "__main__":
    run_pipeline()
