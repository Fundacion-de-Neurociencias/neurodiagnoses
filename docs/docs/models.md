# AI Models in Neurodiagnoses

## Overview
Neurodiagnoses integrates advanced AI models to analyze multi-modal data, including neuroimaging, biomarkers, and clinical assessments, for enhanced CNS disease diagnosis.

## AI Model Categories

### 1. **Probabilistic Diagnosis Model**
   - Uses machine learning to assign probabilities to multiple CNS disorders.
   - Based on supervised learning with labeled datasets.
   - Example algorithms: Random Forest, XGBoost, Bayesian Networks.

### 2. **Tridimensional Diagnosis Model**
   - Classifies disorders based on:
     - **Etiology**: Genetic, autoimmune, vascular, prion, toxic, metabolic.
     - **Molecular Markers**: CSF biomarkers, EEG, neuroinflammation.
     - **Neuroanatomoclinical Correlations**: MRI atrophy, PET, functional impairment.
   - Uses deep learning models such as CNNs for neuroimaging and transformers for clinical text processing.

### 3. **Biomarker Prediction Model**
   - Predicts missing biomarker values using regression-based imputation.
   - Example techniques: KNN Imputation, Gaussian Processes, Bayesian Estimation.

### 4. **Neuroimaging Feature Extraction**
   - Extracts features from MRI, PET, EEG using:
     - Convolutional Neural Networks (CNNs).
     - Graph-based learning for connectivity analysis.
     - fMRI-based functional connectivity modeling.

### 5. **Clinical Decision Support System (CDSS)**
   - Provides AI-driven diagnostic suggestions.
   - Incorporates explainable AI (SHAP analysis) for interpretability.
   - Outputs structured reports with confidence levels.

## Model Training & Deployment

### **Data Sources**
- EBRAINS Data Bucket
- External datasets (ADNI, PPMI, GP2, Enroll-HD, UK Biobank)

### **Training Pipeline**
1. **Data Preprocessing**: Normalization, augmentation, feature extraction.
2. **Model Training**: Supervised/unsupervised learning using GPU-accelerated frameworks.
3. **Evaluation**: AUROC, F1-score, sensitivity/specificity analysis.
4. **Deployment**: Optimized models stored in `/models/` for real-time inference.

### **Federated Learning Integration**
- Secure AI training across multiple institutions.
- Privacy-preserving techniques (Differential Privacy, Homomorphic Encryption).

## How to Use the Models

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Fundacion-de-Neurociencias/Neurodiagnoses.git
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run AI models for inference:**
   ```bash
   python predict.py --input patient_data.csv --model tridimensional
   ```

## Contributing
- Improve model performance by contributing new datasets.
- Enhance explainability by integrating additional visualization techniques.
- Implement new AI architectures for disease stratification.

For detailed model documentation, visit the [GitHub Wiki](https://github.com/Fundacion-de-Neurociencias/Neurodiagnoses/wiki).
