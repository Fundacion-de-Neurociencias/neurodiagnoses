# Prognosis Modeling Workflow

This directory contains scripts for the prognosis modeling workflow, which includes temporal feature calculation, model training, evaluation, and prediction.

## Scripts

### `1_calculate_temporal_features.py`

This script processes longitudinal data to engineer temporal features such as rates of change for biomarkers and time intervals between key pathological events.

**Usage:**

```bash
python 1_calculate_temporal_features.py \
    --data_path data/processed/analysis_ready_dataset.parquet \
    --output_path data/processed/prognosis_feature_dataset.parquet
```

**Arguments:**

*   `--data_path`: Path to the longitudinal analysis-ready dataset. (default: `data/processed/analysis_ready_dataset.parquet`)
*   `--output_path`: Path to save the engineered features dataset. (default: `data/processed/prognosis_feature_dataset.parquet`)

### `2_train_prognosis_model.py`

This script trains a prognosis model (e.g., Cox Proportional Hazards model) using the engineered temporal features.

**Usage:**

```bash
python 2_train_prognosis_model.py \
    --data_path data/processed/prognosis_feature_dataset.parquet \
    --model_out models/prognosis/prognosis_model.joblib
```

**Arguments:**

*   `--data_path`: Path to the dataset with engineered temporal features. (default: `data/processed/prognosis_feature_dataset.parquet`)
*   `--model_out`: Path to save the trained prognosis model. (default: `models/prognosis/prognosis_model.joblib`)

### `3_evaluate_prognosis_model.py`

This script evaluates a pre-trained prognosis model. It calculates the concordance index (C-index) and generates survival curves.

**Usage:**

```bash
python 3_evaluate_prognosis_model.py \
    --data_path data/processed/prognosis_feature_dataset.parquet \
    --model_path models/prognosis/prognosis_model.joblib \
    --output_dir reports/prognosis/
```

**Arguments:**

*   `--data_path`: Path to the dataset with engineered temporal features for evaluation. (default: `data/processed/prognosis_feature_dataset.parquet`)
*   `--model_path`: Path to the pre-trained prognosis model file. (default: `models/prognosis/prognosis_model.joblib`)
*   `--output_dir`: Directory to save evaluation plots and reports. (default: `reports/prognosis/`)

### `4_predict_prognosis_risk.py`

This script uses a pre-trained prognosis model to predict the prognosis risk for new, unseen data.

**Usage:**

```bash
python 4_predict_prognosis_risk.py \
    --data_path data/processed/prognosis_feature_dataset.parquet \
    --model_path models/prognosis/prognosis_model.joblib \
    --output_path reports/prognosis/prognosis_predictions.csv
```

**Arguments:**

*   `--data_path`: Path to the dataset with engineered temporal features for prediction. (default: `data/processed/prognosis_feature_dataset.parquet`)
*   `--model_path`: Path to the pre-trained prognosis model file. (default: `models/prognosis/prognosis_model.joblib`)
*   `--output_path`: Path to save the prediction results (CSV format). (default: `reports/prognosis/prognosis_predictions.csv`)
