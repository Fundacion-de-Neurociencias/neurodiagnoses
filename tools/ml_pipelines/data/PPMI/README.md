# PPMI Directory
# Processed PPMI Data (Sample)

This folder contains a sample output (first 10 rows) from the processed PPMI dataset used in machine learning pipelines for Parkinson’s progression modeling.

Due to PPMI data usage agreements, only a small illustrative file is included here.

## Contents

### `final_df_cleaned_sample.csv`
- **Pipeline**: UPDRS clinical score prediction using MRI, DAT-SPECT, and genotype data.
- **Contents**: Cleaned and imputed features including:
  - Normalized MRI-derived regional brain volumes (e.g., Hippocampus_Total_norm)
  - DAT-SPECT metrics (e.g., striatal binding ratios)
  - Genotype (e.g., APOE, SNCA)
  - Demographics (age, sex, education)
- **Purpose**: Used to predict motor impairment scores (UPDRS Part III) through regression models.

## Preprocessing Pipeline Overview

The complete pipeline was performed in two stages:

---

### 🔹 Stage 1: Raw Data Merging
**Notebook**: `PPMI_Preprocessing_Raw_UPDRS.ipynb`

- Merged multiple PPMI sources:
  - MRI (FreeSurfer volumes, cortical thickness)
  - DAT-SPECT imaging
  - Genotype and demographics
  - Clinical scores (e.g., UPDRS)
- Standardized patient IDs and visit codes (e.g., BL, SC)
- Left-merged data on patient ID (`PATNO`) to preserve all available information
- ✅ Output: `PPMI_Merged_Raw.csv` (intermediate file with preserved missingness)

---

### 🔹 Stage 2: Data Cleaning & Feature Engineering  
**Notebook**: `PPMI_Preprocessing_ready_UPDRS.ipynb`

- Dropped rows and columns with >40% missingness
- Imputed remaining missing values using **KNN imputation**
- Engineered normalized and aggregated volume metrics (e.g., `Putamen_Total_norm`)
- Standardized features for machine learning
- Retained clinically relevant variables for UPDRS prediction

✅ Final output: `final_df_cleaned.csv` (full dataset, not shared)  
📄 Shared sample: `final_df_cleaned_sample.csv` (first 10 rows only)

---

## Preprocessing Code Location

All preprocessing scripts and notebooks are located in:
neurodiagnoses/ml/src/data_processing/PPMI

## Disclaimer

This file contains **only a sample (top 10 rows)** of the final cleaned dataset for demonstration.  
Full datasets are protected under the PPMI data use agreement.  
To request access to full PPMI data, visit: [PPMI Data Access](https://www.ppmi-info.org/access-data-specimens/download-data)
