# src Directory


This directory contains all code (ipynb) and experimental notebooks for the neurodiagnostic ML pipelines. Code is organized by workflow stage (processing → modelling → evaluation) and by disease cohort (ADNI/PPMI).

## Directory Structure

- **src/**
  - data_processing/ - Data pipelines
    - ADNI/ - ADNI processing scripts
    - PPMI/ - PPMI processing scripts
  - evaluation/ - Model evaluation
  - modelling/ - ML models
    - adni_csf_prediction.py - CSF biomarker prediction
    - adni_ad_diagnosis.py - Alzheimer's diagnosis
    - ppmi_regression.py - UPDRS III regression
