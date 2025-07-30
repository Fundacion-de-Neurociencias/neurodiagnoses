# Diagnosis Workflow for Neurodiagnoses

## Overview
Neurodiagnoses follows a structured AI-driven diagnostic workflow to analyze multi-modal clinical data and generate precise diagnostic reports. The workflow integrates probabilistic and tridimensional classification approaches, ensuring both traditional and structured diagnostics for central nervous system (CNS) disorders.

## Step-by-Step Diagnosis Workflow

### 1️⃣ Data Acquisition & Preprocessing
- **Input Sources**: Data is acquired from neuroimaging (MRI, PET, EEG), molecular biomarkers (CSF, plasma), genetic datasets, and clinical records.
- **Data Standardization**: Raw data is converted into standardized formats (.csv, .json, .h5) and harmonized for model compatibility.
- **Integration with EBRAINS & Clinica.run**: Data processing is performed using the EBRAINS Medical Informatics Platform (MIP) and Clinica.run for neuroimaging analysis.

### 2️⃣ AI Model Processing & Feature Extraction
- **Feature Engineering**: The system extracts relevant biomarkers, neuroimaging parameters, and genetic indicators.
- **Multi-Modal AI Models**:
  - Deep learning models for MRI/PET-based feature extraction.
  - Machine learning classifiers for biomarker and genetic analysis.
  - Natural language processing (NLP) for clinical text analysis.

### 3️⃣ Probabilistic & Tridimensional Diagnosis Generation
- **Probabilistic Diagnosis**:
  - Assigns probability scores to multiple potential diagnoses.
  - Uses Bayesian models and ensemble learning for risk estimation.
- **Tridimensional Diagnosis**:
  - Classifies disorders based on three key axes:
    - **Etiology** (genetic, autoimmune, vascular, etc.)
    - **Molecular Biomarkers** (CSF, PET, EEG, MRI markers)
    - **Neuroanatomoclinical Correlations** (structural and functional impairments)
- **Explainability & Confidence Scores**:
  - Results are annotated with SHAP interpretability for transparency.
  - Confidence intervals provide clinicians with AI prediction reliability.

### 4️⃣ Structured Report Generation
- **Diagnostic Reports**: AI-generated results are structured into standardized diagnostic summaries.
- **Clinician Review & Validation**:
  - Specialists evaluate AI-generated diagnoses.
  - Feedback loops refine model performance and adjust classification parameters.

### 5️⃣ Continuous Model Improvement
- **Retraining with New Data**: Regular updates incorporating new patient datasets.
- **Federated Learning Integration**: AI models improve through multi-center collaborations while maintaining data privacy.
- **Collaboration & Open-Source Contributions**:
  - Researchers contribute new features, refine diagnostics, and publish findings.
  - Integration with GitHub and EBRAINS for continuous improvements.

## Next Steps
- **Expand the scope of clinical validation studies.**
- **Enhance real-time AI inference for clinical applications.**
- **Optimize federated learning to maintain privacy while improving model performance.**

For detailed technical implementation, refer to [docs/models.md](models.md) and [docs/data_integration.md](data_integration.md).
