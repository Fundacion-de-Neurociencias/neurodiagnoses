# -*- coding: utf-8 -*-
"""
Unit tests for the PHS risk prediction pipeline.
"""
import pytest
import pandas as pd
import joblib
import os
from workflows.risk_prediction.train_phs_model import PHSTrainingPipeline

@pytest.fixture
def mock_survival_data_path():
    """Provides the path to the mock survival data."""
    return "tests/data/mock_survival_data.parquet"

def test_risk_pipeline_full_cycle(tmp_path, mock_survival_data_path):
    """
    Tests the full train-save-load-predict cycle of the PHS pipeline.
    
    Args:
        tmp_path: A pytest fixture providing a temporary directory.
    """
    # Define a temporary path for the model artifact
    model_path = tmp_path / "test_phs_model.joblib"
    
    # --- 1. Training Phase ---
    train_pipeline = PHSTrainingPipeline(
        data_path=mock_survival_data_path,
        model_path=model_path
    )
    train_pipeline.train_model()
    # Assert that the model file was created
    assert os.path.exists(model_path)
    
    # --- 2. Prediction Phase ---
    predict_pipeline = PHSTrainingPipeline(model_path=model_path)
    
    # Create dummy patient data for prediction
    new_patient_data = pd.DataFrame([{
        'genetics_APOE4_allele_count': 1,
        'genetics_polygenic_risk_score': 1.1
    }])
    
    prediction = predict_pipeline.predict(new_patient_data)
    
    # Assert that the prediction is in the expected format
    assert isinstance(prediction, pd.Series)
    assert not prediction.empty
    assert pd.api.types.is_numeric_dtype(prediction.dtype)