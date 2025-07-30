from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from huggingface_hub import hf_hub_download

# Initialize FastAPI
app = FastAPI()

# Download the model from Hugging Face
MODEL_REPO = "fneurociencias/neurodiagnoses-agnostic-ml"
MODEL_FILENAME = "model.pkl"

# Load the model (Modify this to load your actual trained model)
model_path = hf_hub_download(repo_id=MODEL_REPO, filename=MODEL_FILENAME)
model = joblib.load(model_path)  # Assuming the model is stored as a .pkl file

# Define the input data format
class BiomarkerData(BaseModel):
    age: int
    sex: str
    plasma_biomarker_1: float
    plasma_biomarker_2: float
    MRI_region_1: float
    MRI_region_2: float

@app.get("/")
def home():
    return {"message": "Neurodiagnoses API is running!"}

@app.post("/predict")
def predict(data: BiomarkerData):
    # Convert input data to a DataFrame
    input_df = pd.DataFrame([data.dict()])

    # Make a prediction
    prediction = model.predict(input_df)

    return {"prediction": prediction.tolist()}
