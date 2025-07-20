# PPMI Data Preprocessing

This folder contains the preprocessing pipeline for the PPMI dataset, organized into two major stages:

---

## 1. `PPMI_Preprocessing_Raw_UPDRS.ipynb`  
**Stage 1 – Raw Data Merger**

### Objective:
Integrate multiple PPMI data sources into a unified baseline dataset, retaining as much information as possible for further processing.

### Input Data Sources:
- **MRI (FreeSurfer)**: Cortical thickness, subcortical volumes  
- **DAT-SPECT**: Striatal binding ratios  
- **UPDRS**: Part III motor scores  
- **Demographics**: Age, sex, education  
- **Genotype**: APOE.

### Key Processing Steps:
- Load individual raw `.csv` files.
- Select clinically relevant variables from each source.
- Standardize subject IDs and visit labels (BL/SC).
- Perform left-joins on `PATNO` to retain patient records across modalities.
- Retain missing values (no imputation yet).

### Output:
`PPMI_Merged_Raw.csv` — A merged dataset with partially missing data, preserving maximum coverage for all participants.

---

## 2. `PPMI_Preprocessing_ready_UPDRS.ipynb`  
**Stage 2 – Final Cleaning and Modeling-Ready Dataset**

### Objective:
Prepare a modeling-ready dataset focused on predicting **UPDRS Part III** scores from multimodal inputs.

### Key Processing Steps:
#### Initial Cleaning:
- Remove patients (rows) with >40% missing data.
- Drop features (columns) with >40% missing data.

#### Missing Data Imputation:
- Apply **KNN imputation** to remaining missing values.

#### Feature Engineering:
- Normalize brain region volumes (e.g., by ICV).
- Combine left/right hemisphere measures (e.g., `Hippocampus_Total_norm`).

#### Feature Selection:
- Keep only biologically and clinically meaningful features.
- Remove low-informative or redundant variables (e.g., scan IDs, raw volumes).

#### Standardization:
- Apply feature scaling to ensure uniform input distributions for modeling.

### Output:
`final_df_cleaned_sample.csv` — A clean, imputed, normalized, and standardized dataset (shape: 1716 rows × 109 features), ready for Experiment 1 (UPDRS score prediction).

---

## Notes:
- Stage 1 preserves raw data integrity, while Stage 2 ensures modeling readiness.
- Output data is saved under: `ml/data/PPMI/processed/`


