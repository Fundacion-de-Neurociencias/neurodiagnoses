# ADNI Directory
# processed Directory


# Processed ADNI Data (Sample) from ADNIMERGE

This folder contains **sample outputs** (first 10 rows) from the processed ADNI baseline dataset used in different machine learning pipelines within this project.

Due to ADNI data usage restrictions, only small sample files are included here for illustration and reproducibility. These were derived from the original raw **ADNIMERGE** dataset after careful preprocessing.

## Contents

### 1. `ADNI_baseline_clean_sample.csv`
- **Pipeline**: Artificial Neural Network (ANN) for Alzheimer's diagnosis classification.
- **Contents**: MRI-derived features (normalized by ICV), APOE4 genotype, age, and clinical scores (MMSE, CDRSB).
- **Purpose**: This cleaned dataset was used to train and evaluate ANN models comparing performance with and without clinical scores.

### 2. `df_clean.csv_sample.csv`
- **Pipeline**: CSF biomarker positivity classification (e.g., Aβ, pTau, tTau).
- **Contents**: Demographic, clinical, and biomarker variables cleaned and filtered for baseline visits, with high-missingness features removed.
- **Purpose**: Used to predict CSF biomarker status using machine learning classifiers.

## Preprocessing Details

Full preprocessing logic and scripts are located in:
📁 neurodiagnoses/ml/src/data_processing/ADNI/

## Disclaimer

These CSV files are **illustrative samples** only (top 10 rows) and **do not include full ADNI data** due to privacy and licensing constraints.  
To access full datasets, apply at: [ADNI Data Access](https://adni.loni.usc.edu/data-samples/access-data/)

