# 🧪 Tau and Amyloid Positivity Prediction using ADNI Biomarkers

## 📚 Project Overview

This project explores the classification of **CSF biomarker positivity** for Alzheimer’s Disease (AD) using the ADNI dataset. The primary goals were:

- To predict **tTau** and **pTau** positivity (based on CSF ratio cutoffs) to assist in **early clinical trial triage**.
- To explore **ABETA positivity** prediction using simpler modeling for comparative research purposes.
- To emphasize **sensitivity** in tTau/pTau models to **minimize false negatives**, improving safety and efficacy in trial candidate selection.
- To apply **SHAP explainability** for transparency and biomarker validation.

---

## 🧠 Target Definitions

| Task           | Definition                                | Use Case                  |
|----------------|--------------------------------------------|---------------------------|
| **ABETA+**     | `ABETA < 880`                              | Exploratory research      |
| **tTau+**      | `tTau / ABETA > 0.27`                      | Clinical trial triage     |
| **pTau+**      | `pTau / ABETA > 0.023`                     | Clinical trial triage     |

---

## ⚙️ Shared Methodology

### 1. Data Preprocessing
- Cleaned biologically implausible CSF values (e.g., ABETA > 1700).
- Imputed missing values using appropriate techniques.
- Normalized MRI features by ICV (e.g., hippocampus/ICV).
- Filtered only baseline visits to reduce redundancy.

### 2. Feature Engineering

| Model Type | Key Strategies |
|------------|----------------|
| **ABETA**  | Basic demographics, APOE4, MRI volumes |
| **pTau**   | 20 best features with strong interactions: APOE4 × Age, memory × hippocampus |
| **tTau**   | Advanced interaction terms, feature normalization, and hyperparameter tuning |

Example feature interactions used:
- `APOE4 × Age`
- `APOE4 × Hippocampus`
- `MemoryComposite × Entorhinal`
- `ADAS13 × VentricularVolume`

### 3. Model Evaluation
- Used **train-test stratified split** (70/30).
- Applied **class weighting / scale_pos_weight** for imbalance.
- Prioritized **sensitivity (recall)** for pTau and tTau tasks.
- Optimized **classification thresholds** using ROC/PR analysis.

---

## 🔬 Results by Task

### 🟡 Aβ₄₂ Positivity (Research Only)
- **No hyperparameter tuning** or complex engineering.
- Basic interactions: APOE4 × Age, cognition × MRI.
- Purpose: Exploratory benchmarking only (not optimized for deployment).

### 🧠 pTau Positivity (pTau / ABETA > 0.023)

| Model             | AUC-ROC | Recall (1) | Precision (1) | F1-Score (1) | Accuracy |
|------------------|---------|------------|----------------|--------------|----------|
| Logistic Reg.    | 0.859   | 0.87       | 0.77           | 0.82         | 0.79     |
| Opt. Logistic Reg| 0.855   | 0.73       | 0.86           | 0.79         | 0.79     |
| **Random Forest**| 0.851   | 0.81       | 0.78           | 0.79         | 0.77     |
| XGBoost          | 0.838   | 0.80       | 0.75           | 0.77         | 0.75     |

**Best model**: Optimized Logistic Regression or Random Forest (balance of sensitivity and explainability)

**Clinical metrics (RF)**:
- **Sensitivity**: 0.808
- **Specificity**: 0.732
- **PPV**: 0.778
- **NPV**: 0.766

---

### 🧠 tTau Positivity (tTau / ABETA > 0.27)

| Model             | AUC-ROC | Recall (1) | Precision (1) | F1-Score (1) | Accuracy |
|------------------|---------|------------|----------------|--------------|----------|
| Logistic Reg.    | 0.846   | 0.74       | 0.83           | 0.78         | 0.78     |
| Random Forest    | 0.849   | 0.72       | 0.80           | 0.76         | 0.75     |
| **XGBoost(Best)**| **0.859** | **0.87** | 0.77           | **0.82**     | **0.79** |

**Best model**: XGBoost  
- High **recall (0.87)** critical for triage  
- Excellent overall performance with SHAP support

---

## 📊 Explainability with SHAP

SHAP was used for pTau and tTau best models to ensure **biological validity** and **clinical interpretability**.

### Key Predictive Features (Top SHAP):
- `ADAS13_bl` — global cognition
- `APOE4_AGE` — gene–age interaction
- `Memory Composite` — early episodic memory loss
- `APOE4_Hippocampus` — genetic risk × neurodegeneration
- `Ventricular Volume` — marker of atrophy progression

✅ **SHAP values showed consistent directionality** across pTau and tTau models, reinforcing trust in model outputs and feature effects.

---

## ✅ Clinical & Research Implications

| Use Case              | Deployment Potential | Comment |
|-----------------------|----------------------|---------|
| Aβ₄₂ positivity model | ❌ Research only      | No optimized pipeline used |
| pTau model            | ✅ Triage candidate   | Balanced RF model with 80% sensitivity |
| tTau model            | ✅ Triage candidate   | Best performance with XGBoost |

---

## 🔜 Future Directions

- External validation on AIBL or independent AD cohort


---

## 🧾 Citation & Acknowledgments

Data: Alzheimer’s Disease Neuroimaging Initiative (ADNI)  
SHAP: Lundberg et al. (2017) – "A Unified Approach to Interpreting Model Predictions"  
Modeling: scikit-learn, XGBoost, SHAP libraries

---
### 🧠 3-Axis Diagnostic Mapping

###  CSF Biomarker Positivity (Aβ42, tTau, pTau)

| **Axis**               | **Category**              | **Key Features Used**                                                             |
|------------------------|---------------------------|------------------------------------------------------------------------------------|
| **Axis 1: Etiology/Risk**     | Genetic Risk               | APOE4 genotype (0, 1, or 2 alleles)                                                 |
|                        | Age Factor                | Age ↑                                                                              |
| **Axis 2: Molecular**         | Core Biomarkers           | Aβ42, tTau, pTau (CSF-based, used as prediction targets)                           |
|                         |
| **Axis 3: Clinical–Anatomical** | Cognitive Assessments      | ADAS13 ↑, MoCA ↓, LDELTOTAL ↓, TRABSCOR ↑, FAQ ↑                                  |
|                        | Structural MRI            | Hippocampal volume ↓, Entorhinal volume ↓, Ventricular volume ↑                   |

---

### 🧾 Sample Annotation

`[July 2025] Genetic risk (APOE4+, age↑) / Aβ42+, pTau+, tTau+ / Atrophy (hippocampus↓), cognitive decline (ADAS13↑, LDELTOTAL↓)`

####  Directional Arrows (↑ / ↓)

Directional arrows indicate the typical relationship of a feature to disease pathology:

- **↑ (Up arrow)**: The feature is **increased** or **elevated** in association with risk or pathology.  
  _Example: `ADAS13 ↑` → Higher ADAS13 scores (worse cognition) are linked to Alzheimer's-related biomarker positivity._

- **↓ (Down arrow)**: The feature is **decreased** or **reduced** in association with pathology.  
  _Example: `Hippocampal volume ↓` → Lower hippocampal volume is commonly observed in Alzheimer's disease._

This notation provides a compact and intuitive way to represent clinical and biomarker trends across diagnostic axes.



`


