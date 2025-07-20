# ADNI ANN Experiments – Alzheimer's Disease Classification

This folder contains a series of experiments using shallow Artificial Neural Networks (ANNs) to explore the prediction of Alzheimer's Disease (AD) stages using multimodal features from the ADNI dataset. The project is an **exploratory research effort** focused on understanding the predictive power of neuroimaging, genetic, and clinical data — both independently and in combination.

---

## 🔬 Research Motivation

While the Neurodiagnosis project had previously deployed a **Random Forest** model for clinical score prediction (e.g., UPDRS), this ANN-based extension investigates:

- How **clinical scores vs. biological features** affect model performance.
- Whether **ANNs can capture subtle nonlinearities** in AD pathology.
- How well **interpretable ML (SHAP)** can validate biological plausibility in digital biomarkers.
- The influence of **class imbalance** in AD stage classification tasks.
- What is the directional contribution of some **mri derived feature** e.g hippocampal atrophy to AD pathology?

This framework is not intended for clinical deployment but for improving understanding and transparency in ML-based AD staging.

---

## 🧪 Experiment Summaries

### **🧠 Experiment 1 – Baseline ANN with Clinical Scores**

- **Goal**: Build a minimal shallow ANN using only Hippocampus volume (normalized by ICV) + baseline clinical scores (CDRSB, MMSE) to classify AD into CN, MCI, and Dementia.
- **Result**: Achieved **92% accuracy**.
- **Concern**: Potential data leakage due to use of clinically-derived target labels.
- **Takeaway**: Clinical scores are powerful predictors but may not represent a fair generalization test.

**Classification Report Snippet**:
precision recall f1-score support
CN 0.97 0.98 0.98 160
MCI 0.78 0.90 0.84 68
AD 0.94 0.88 0.91 186


---

### **⚖️ Experiment 2 – Handling Class Imbalance + SHAP**

- **Goal**: Address Dementia class underrepresentation using **SMOTE**, and compare ANN to Logistic Regression.
- **Steps**:
  - Applied SMOTE for oversampling
  - Evaluated ANN vs. Logistic Regression
  - Introduced **SHAP** for interpretability

- **Findings**:
  - **ANN achieved ~91% accuracy**, improved Dementia recall.
  - **SHAP revealed**:
    - `CDRSB` was most impactful across all stages.
    - `MMSE` and `Hippocampus_ICV` had high weight in Dementia/MCI.
    - `APOE4` contributed least (in this feature set).

---

### **🔍 Experiment 3 – MRI & APOE Only vs. +Clinical Scores**

- **Goal**: Compare ANN performance using only **biomarkers (MRI, APOE4)** vs. **adding clinical scores**.
- **Features**:
  - Biological: `Hippocampus`, `Entorhinal`, `Ventricles`, `MidTemp`, `WholeBrain` (normalized), `APOE4`, `Age`
  - Clinical: `MMSE`, `CDRSB`

- **Insights**:
  - Biological features alone carry predictive power (moderate performance).
  - Adding `MMSE` and `CDRSB` boosts performance significantly.
  - SHAP confirmed:
    - **Low Hippocampus_ICV and WholeBrain_ICV volumes → AD pathology**
    - Clinical scores dominate feature importance when present.

Directional Relationships:
---
| Biomarker          | Directionality | Clinical Significance            |
|--------------------|----------------|-----------------------------------|
| Hippocampus_ICV    | ↓ → ↑ AD risk  | Medial temporal lobe atrophy      |
| WholeBrain_ICV     | ↓ → ↑ AD risk  | Global neurodegeneration          |
| Ventricles_ICV     | ↑ → ↑ AD risk  | Ex-vacuo ventricular enlargement  |
| APOE4              | ↑ → ↑ AD risk  | Genetic susceptibility            |



## 📁 Output
- Each experiment produces:
  - Trained model(s)
  - SHAP plots
  - Classification reports and confusion matrices
  - Feature importance insights

---

## 🧬 Notes
- Dataset used: **ADNI baseline visit**
- Label classes: `0 = CN`, `1 = MCI`, `2 = AD`
- Class imbalance addressed using **SMOTE** (Experiment 2 & 3)

---
## 📂 Folder Structure
adni_ad/
├── ANN_ADNI_Experiment1.ipynb
├── ANN_ADNI_Experiment2.ipynb
├── ANN_ADNI_Experiment3.ipynb
├── README.md ← (you are here)


# SHAP Directionality Interpretation for Dementia Prediction

This table summarizes the SHAP value directionality for MRI-derived features used in a dementia classification model, and compares them with current Alzheimer's disease (AD) literature.

| Feature              | SHAP Directionality                          | Matches Literature?        | Notes/Interpretation                                                        |
|----------------------|----------------------------------------------|----------------------------|------------------------------------------------------------------------------|
| **Hippocampus_bl_ICV** | ↓ volume → ↑ Dementia risk                  | ✅ Strong match             | Hippocampal atrophy is a hallmark of early AD pathology                     |
| **MidTemp_bl_ICV**     | ↓ volume → ↑ Dementia risk                  | ✅ Strong match             | Middle temporal lobe atrophy is associated with early AD                    |
| **WholeBrain_bl_ICV**  | ↓ volume → ↑ Dementia risk                  | ✅ Match                    | Global atrophy reflects widespread neurodegeneration                        |
| **Ventricles_bl_ICV**  | ↑ volume → ↑ Dementia risk                  | ✅ Inverse marker           | Ventricular enlargement indicates surrounding brain atrophy                 |
| **AGE**                | ↑ age → mild ↑ risk                         | ✅ Weak but consistent      | Age is a strong risk factor, but MRI features dominate in this model        |
| **Entorhinal_bl_ICV**  | ↓ volume → ↑ Dementia risk                  | ✅ Strong match             | Entorhinal cortex is one of the earliest regions affected in AD             |
| **APOE4**              | Weak effect; no clear SHAP directionality   | ⚠️ Weak signal in model     | May have stronger effects in longitudinal or larger-scale models            |
| **Fusiform_bl_ICV**    | ↓ volume → mild ↑ Dementia risk             | ✅ Plausible                | Fusiform atrophy can appear in AD, particularly in later stages            |

---

### Legend

- **↓ volume**: Lower feature value (atrophy)
- **↑ Dementia risk**: Positive SHAP value (contributes to classifying as dementia)
- **SHAP Directionality**: Interpreted from SHAP summary plot
- **Matches Literature?**: Whether the model's interpretation aligns with known AD neuropathology

---

*Interpretation based on SHAP summary plot from multimodal model trained on baseline MRI-derived features.*

### 🧠 Three-Axis Diagnostic Mapping (ADNI – Alzheimer's Disease Diagnosis)

| Axis | Category              | Key Elements                                                                 |
|------|------------------------|------------------------------------------------------------------------------|
| **1. Etiology/Risk**         | Genetic Risk            | APOE4 genotype                                                              |
|                              | Age Factor              | Age ↑                                                                       |
| **2. Molecular**             | –                       | -        |
| **3. Clinical–Anatomical**   | MRI Atrophy             | ↓ Hippocampus_ICV, ↓ WholeBrain_ICV, ↓ MidTemp_ICV, ↓ Entorhinal_ICV        |
|                              | Ventricular Expansion   | ↑ Ventricles_ICV                                                            |
|                              | Clinical Scores         | ↑ CDRSB, ↓ MMSE                                                             |
|                              | Composite Neurodegeneration | ↑ Dementia probability via SHAP contributions from above features       |

---

### 📝 Sample Annotation  
`[July 2025] Genetic risk (APOE4+, Age↑) / – / Medial temporal atrophy (↓Hippocampus, ↓Entorhinal), cognitive impairment (↑CDRSB, ↓MMSE)`



