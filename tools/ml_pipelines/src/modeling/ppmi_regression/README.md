# PPMI Motor Score Prediction Pipeline

This project develops machine learning models to predict Unified Parkinson's Disease Rating Scale - Part III Motor Examination scores (NP3TOT) using multi-modal data from the Parkinson's Progression Markers Initiative (PPMI). The pipeline evaluates models like Random Forests, XGBoost, LightGBM, and shallow Artificial Neural Networks (ANNs) to identify the most effective approach for predicting motor impairment from structural MRI, DAT-SPECT imaging, APOE4 genotype, and demographic data.

**Goal**: Build a robust, interpretable model to predict motor impairment (UPDRS-III/NP3TOT) using biomarkers, supporting disease monitoring and clinical trial recruitment.

## Table of Contents
- [Dataset](#dataset)
- [Experiments](#experiments)
- [Key Findings](#key-findings)
- [Tech Stack](#tech-stack)
- [Future Work](#future-work)
- [License](#license)

## Dataset
**Source**: Parkinson's Progression Markers Initiative (PPMI)

**Target**: NP3TOT (UPDRS-III motor score)

**Features**:
- **Neuroimaging**: Structural MRI-derived volumes (e.g., ventricles, white matter)
- **DAT-SPECT**: e.g Striatal binding ratios for caudate and putamen
- **Genetics**: APOE4 genotype
- **Demographics**: Age, Sex
- **Optional Clinical Score**: Hoehn and Yahr stage (NHY) in Experiment 4

## Experiments

### Experiment 1: Baseline Models (Linear Regression vs. Random Forest)
- **Dataset**: Preprocessed with imputation
- **Models**:
  - Linear Regression (Baseline)
  - Random Forest (Untuned)
- **Metrics**:
  | Model           | MAE   | MSE    | R²    |
  |-----------------|-------|--------|-------|
  | Linear Regression | 9.75  | 142.86 | 0.035 |
  | Random Forest   | 7.72  | 104.78 | 0.292 |
- **Finding**: Random Forest outperformed Linear Regression, capturing non-linear patterns in multi-modal data.

### Experiment 2: Hyperparameter Tuning (LightGBM, XGBoost, Random Forest)
- **Models**:
  - LightGBM and XGBoost (tuned via Optuna)
  - Random Forest (slightly tuned)
- **Metrics**:
  | Model           | MAE   | MSE    | RMSE  | R²    |
  |-----------------|-------|--------|-------|-------|
  | LightGBM        | 6.539 | 74.711 | 8.644 | 0.495 |
  | XGBoost         | 6.525 | 76.952 | 8.772 | 0.480 |
  | Random Forest   | 5.681 | 56.947 | 7.546 | 0.579 |
- **Finding**: Random Forest outperformed boosted models, demonstrating robustness even with minimal tuning.

### Experiment 3: Feature Engineering + Shallow ANN
- **Feature Engineering**:
  - Striatal-Entorhinal Network Interaction
  - Asymmetry-Weighted Striatal Score
  - White Matter Integrity Index
  - Age-Adjusted Striatal Binding (Nonlinear)
  - Ventricular Effect Score
- **Models**:
  - Random Forest (RandomizedSearchCV)
  - Shallow ANN (EarlyStopping)
- **Metrics**:
  | Model      | MAE   | MSE    | RMSE  | R²    |
  |------------|-------|--------|-------|-------|
  | Random Forest | 5.720 | 55.963 | 7.481 | 0.586 |
  | ANN        | 6.985 | ~      | ~     | 0.411 |
- **Finding**: Feature engineering enhanced Random Forest performance. ANN underperformed, likely due to limited data or architecture constraints.
- **Key Predictive Features** (via SHAP):
  - Putamen_Total, Putamen_Asymmetry
  - Caudate_Total, Caudate_Asymmetry
  - Asym_Striatal_Score, Age

### Experiment 4: NHY Inclusion (Clinical Score)
- **Goal**: Assess impact of including Hoehn and Yahr stage (NHY).
- **Model**: Random Forest (best configuration)
- **Metrics**:
  | Metric | Without NHY | With NHY |
  |--------|-------------|----------|
  | MAE    | 5.654       | 4.634    |
  | MSE    | 55.653      | 43.206   |
  | RMSE   | 7.460       | 6.573    |
  | R²     | 0.588       | 0.680    |
- **Finding**: NHY inclusion significantly improved performance but risked clinical score leakage. SHAP analysis showed NHY dominated predictions, potentially masking subtle biological markers.

## Key Findings
- **Model Performance**: Random Forest consistently outperformed other models across experiments.
- **Feature Importance** (via SHAP):
  - DAT-SPECT features (Putamen, Caudate) were strong predictors.
  - Age and asymmetry-based features were also significant.
- **Explainability**: SHAP was used to interpret model behavior, highlighting key predictors.
- **NHY Impact**: Including NHY improved predictions but introduced bias risk, potentially overshadowing biomarker signals.

## Tech Stack
- **Python**: Pandas, NumPy, Scikit-learn, XGBoost, LightGBM, TensorFlow/Keras
- **Hyperparameter Tuning**: Optuna
- **Explainability**: SHAP
- **Visualization**: Matplotlib, Seaborn

### 🧠 Three-Axis Diagnostic Mapping (PPMI – UPDRS Motor Score)

| Axis | Category              | Key Elements                                                                 |
|------|------------------------|------------------------------------------------------------------------------|
| **1. Etiology/Risk**         | Genetic Risk            | APOE4 genotype                                                              |
|                              | Age Factor              | Age ↑                                                                       |
| **2. Molecular**             | –                       | - |
| **3. Clinical–Anatomical**   | Dopaminergic Imaging    | Putamen_Total, Caudate_Total, Asym_Striatal_Score, Putamen_Entorhinal_Ratio |
|                              | Asymmetry Metrics       | Putamen_Asym, Caudate_Asym                                                              |
|                              | Structural MRI Volumes  | Hippocampus_Total_norm, Ventricular_Effect, lh_entorhinal, TotalGrayVol_norm |
|                              | Composite Imaging Scores| WM_Integrity, Left_choroid_plexus                           |

---

### 📝 Sample Annotation  
`[July 2025] Genetic risk (APOE4+, Age↑) / – / Dopaminergic asymmetry (Putamen_Asym↑), caudate atrophy: motor impairment`


## Future Work
- Explore ensemble models for improved performance.
- Evaluate deep learning with larger, augmented datasets.
- Perform external validation across centers or cohorts.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
