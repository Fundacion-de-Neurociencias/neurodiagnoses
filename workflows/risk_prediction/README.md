# Polygenic Hazard Score (PHS) Risk Prediction Workflow

This directory contains scripts for the Polygenic Hazard Score (PHS) risk prediction workflow, which includes model training, evaluation, and prediction.

## Scripts

### `1_train_phs_model.py`

This script trains a Cox Proportional Hazards model to predict the risk of disease onset based on genetic features. It uses the `lifelines` library.

**Usage:**

```bash
python 1_train_phs_model.py \
    --data_path data/processed/analysis_ready_dataset.parquet \
    --model_out models/risk_prediction/phs_model.joblib
```

**Arguments:**

*   `--data_path`: Path to the analysis-ready parquet dataset for training. (default: `data/processed/analysis_ready_dataset.parquet`)
*   `--model_out`: Path to save the trained PHS model file. (default: `models/risk_prediction/phs_model.joblib`)

### `2_evaluate_phs_model.py`

This script evaluates a pre-trained PHS model. It calculates the concordance index (C-index) and generates survival curves.

**Usage:**

```bash
python 2_evaluate_phs_model.py \
    --data_path data/processed/analysis_ready_dataset.parquet \
    --model_path models/risk_prediction/phs_model.joblib \
    --output_dir reports/risk_prediction/
```

**Arguments:**

*   `--data_path`: Path to the analysis-ready parquet dataset for evaluation. (default: `data/processed/analysis_ready_dataset.parquet`)
*   `--model_path`: Path to the pre-trained PHS model file. (default: `models/risk_prediction/phs_model.joblib`)
*   `--output_dir`: Directory to save evaluation plots and reports. (default: `reports/risk_prediction/`)

### `3_predict_phs_risk.py`

This script uses a pre-trained PHS model to predict the Polygenic Hazard Score for new, unseen data.

**Usage:**

```bash
python 3_predict_phs_risk.py \
    --data_path data/processed/analysis_ready_dataset.parquet \
    --model_path models/risk_prediction/phs_model.joblib \
    --output_path reports/risk_prediction/phs_predictions.csv
```

**Arguments:**

*   `--data_path`: Path to the input parquet dataset for prediction. (default: `data/processed/analysis_ready_dataset.parquet`)
*   `--model_path`: Path to the pre-trained PHS model file. (default: `models/risk_prediction/phs_model.joblib`)
*   `--output_path`: Path to save the prediction results (CSV format). (default: `reports/risk_prediction/phs_predictions.csv`)
