# models/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys
import pandas as pd

# Add project root for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unified_orchestrator import run_full_diagnosis_for_api # We will add this function to the orchestrator
from tools.ml_pipelines.pipelines_axis2_molecular import Axis2MolecularPipeline

# Initialize FastAPI app
app = FastAPI(
    title="Neurodiagnoses API",
    description="An API to serve the 3-axis probabilistic diagnostic framework.",
    version="1.0.0"
)

class PredictionResponse(BaseModel):
    """Defines the structure of the API's response."""
    patient_id: str
    report: dict

@app.on_event("startup")
async def startup_event():
    """
    On startup, run a pre-flight check to ensure the ML models are trained.
    This prevents a long delay on the first API call.
    """
    print("--- API starting up: Running pre-flight checks ---")
    axis2_pipeline = Axis2MolecularPipeline()
    if not os.path.exists(axis2_pipeline.model_path):
      print("Axis 2 model not found. Training now...")
      axis2_pipeline.train_and_evaluate()
      print("Pre-flight training complete.")
    else:
      print("All models found. API is ready.")

@app.get("/", tags=["General"])
def read_root():
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to the Neurodiagnoses 3-Axis Diagnostic API"}

@app.post("/predict/{patient_id}", response_model=PredictionResponse, tags=["Diagnostics"])
def get_3_axis_diagnosis(patient_id: int):
    """
    Runs the full 3-axis diagnosis for a given patient ID and returns the report.
    
    In this PoC, data is simulated based on the ID. In a real system,
    this would trigger a lookup in a patient database.
    """
    print(f"Received prediction request for patient_id: {patient_id}")
    try:
        # Call the orchestrator's logic to get the final report
        final_report = run_full_diagnosis_for_api(patient_id)
        if not final_report:
            raise HTTPException(status_code=404, detail="Patient data could not be processed.")
        
        return {"patient_id": str(patient_id), "report": final_report}
    except Exception as e:
        print(f"ERROR during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))