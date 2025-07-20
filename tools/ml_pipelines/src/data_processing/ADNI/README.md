# ADNI Data Preprocessing

This folder contains two preprocessing pipelines for the ADNI dataset, each tailored for different downstream tasks:

---

## 1. `ADNI_ANN_model_Preprocessing.ipynb`  
**Goal**: Prepare baseline ADNI data for training Artificial Neural Networks (ANN) for diagnostic prediction.

### Key Processing Steps:
- **Filter Baseline Visits**: Select only rows with VISCODE = `'bl'`.
- **Feature Selection**: Focus on MRI features, APOE4 genotype, and clinical scores (MMSE, CDRSB).
- **Missing Data Handling**:
  - Drop rows with missing MRI volumes.
  - Impute missing values in AGE, APOE4, MMSE, and CDRSB.
- **MRI Normalization**: Normalize MRI volumes by ICV (Intracranial Volume).
- **Final Cleaning**: Drop rows with missing diagnosis (DX) after all imputations.

### Output:
`cleaned_ADNI_baseline_data.csv` — A cleaned dataset containing normalized MRI features, selected clinical/genetic features, and baseline visits only.

---

## 2. `ADNI_CSF_preprocessing.ipynb`  
**Goal**: Prepare the baseline ADNI data for CSF biomarker prediction tasks.

### Key Processing Steps:
- **Input**: `ADNIMERGE_25Apr2025.csv` (merged clinical, biomarker, imaging data).
- **Filter Baseline Visits**: Keep only baseline entries.
- **Remove Unneeded Data**: Drop Ecog score columns.
- **De-duplicate**: Keep only the first row per unique participant (`PTID`).
- **High Missingness Filtering**:
  - Drop columns with >50% missingness.
- **Missing Data Imputation**:
  - Mean imputation for continuous variables.
  - Most frequent imputation for categorical variables.

### Output:
`df_clean.csv` — A streamlined dataset with reduced missingness and one entry per participant.

---

## Notes:
- Both pipelines operate independently and serve different modeling tasks.
- Output data is stored under: `ml/data/ADNI/processed/`


