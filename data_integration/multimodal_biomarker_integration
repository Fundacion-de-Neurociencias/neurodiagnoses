# **Neurodiagnoses: Multi-Modal Biomarker Integration**

## **Overview**
Neurodiagnoses now supports **multi-modal biomarker analysis** through AI-driven approaches, integrating **MRI, CSF, blood, and EEG** biomarkers for enhanced precision in neurodegenerative disease diagnostics. This update includes:
- **Deep Learning for MRI-based biomarker extraction** (CNNs, Autoencoders).
- **SHAP-based explainability models** for ranking CSF and blood biomarkers.
- **EEG Functional Biomarkers** using deep learning and multiplex network analysis.
- **Strict subject-level cross-validation** to prevent data leakage.

---

## **1. Data Processing Pipeline**
### **1.1 Data Ingestion**
- **Supported Modalities:**
  - MRI (NIfTI format)
  - CSF & Blood Biomarkers (CSV, JSON)
  - EEG Signals (Time-Series, EDF, CSV)
- **Preprocessing Steps:**
  - MRI: Standardization, skull-stripping, entropy-based slice selection.
  - CSF/Blood: Normalization (Z-score, Min-Max scaling), outlier removal.
  - EEG: Filtering (0.5-40Hz), artifact rejection, feature extraction.

### **1.2 Feature Selection**
- **Anchor-Graph Feature Selection**: Reduces feature redundancy across modalities.
- **Principal Component Analysis (PCA)**: Extracts dominant biomarker signals.
- **Autoencoders**: Learn compressed biomarker representations.

### **1.3 AI Models for Biomarker Classification**
| **Model** | **Modality** | **Function** |
|-----------|------------|-------------|
| **CNN (ResNet, VGG16)** | MRI | Structural biomarker classification |
| **Random Forest + SHAP** | CSF/Blood | Biomarker ranking & disease risk prediction |
| **EEG Deep Learning** | EEG | Functional biomarker classification |
| **Ensemble Model** | Multi-modal | Combines MRI, CSF, EEG for precision diagnosis |

### **1.4 Model Explainability & Validation**
- **SHAP Analysis**: Identifies most important biomarkers for classification.
- **Subject-Level Cross-Validation**: Prevents overfitting and ensures clinical generalization.
- **AUC, Accuracy, F1-Score**: Standard evaluation metrics.

---

## **2. How to Use**
### **2.1 Installation**
Clone the repository and install dependencies:
```bash
 git clone https://github.com/neurodiagnoses
 cd neurodiagnoses
 pip install -r requirements.txt
```

### **2.2 Running the Biomarker Analysis Pipeline**
Use the `analyze_biomarkers` function to run the full pipeline:
```python
from neurodiagnoses.biomarkers import analyze_biomarkers
analyze_biomarkers(data_path="data/multi_modal.csv")
```

### **2.3 SHAP Visualizations for Explainability**
```python
import shap
import matplotlib.pyplot as plt

shap_values, data = analyze_biomarkers("data/multi_modal.csv", return_shap=True)
shap.summary_plot(shap_values, data.iloc[:, 1:])
```

---

## **3. File Structure**
```bash
neurodiagnoses/
│── biomarkers.py  # Biomarker processing & AI models
│── data/          # Storage for biomarker datasets
│── models/        # Pre-trained models (CNNs, SHAP models)
│── README.md      # Main documentation
│── BIOMARKERS.md  # This file (biomarker integration details)
```

---

## **4. References & Sources**
- **Data Leakage Mitigation in MRI Classification (Thesis_2022).**
- **SHAP-enhanced Biomarker Interpretation (fnins-18-1361055.pdf).**
- **EEG Functional Biomarker Networks (1-s2.0-S1746809422006772-main.pdf).**

For further development or contributions, please submit a pull request on **[Neurodiagnoses GitHub](https://github.com/neurodiagnoses)**.

