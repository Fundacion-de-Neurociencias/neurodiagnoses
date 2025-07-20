# modeling Directory

# Modeling Pipelines Overview

This directory contains the core machine learning pipelines for neurodiagnostic prediction tasks. Each subfolder represents a distinct research pipeline focused on specific neurological disorders and biomarkers.

## Key Pipelines
| Pipeline | Cohort | Prediction Task | Primary Features |
|----------|--------|-----------------|------------------|
| [AD Alzheimer's Classification](ADNI_Alzheimers_Classification) | ADNI | AD stage (CN/MCI/Dementia) | MRI volumes, Clinical scores, APOE4 |
| [CSF Biomarker Prediction](ADNI_CSF_Biomarker_Prediction) | ADNI | tTau/pTau/ABETA positivity | MRI features, Cognitive assessments, Demographics |
| [Motor Score Prediction](PPMI_Motor_Score_Prediction) | PPMI | UPDRS-III motor scores | DAT-SPECT, MRI volumes, Genotype |

## Common Methodological Framework
- **Interpretability**: SHAP explainability integrated in all pipelines
- **Validation**: Stratified k-fold cross-validation
- **Reproducibility**: Seed-controlled randomization
- **Clinical Focus**: Sensitivity optimization for clinical trial triage

