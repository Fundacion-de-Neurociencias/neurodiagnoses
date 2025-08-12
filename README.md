#  Neurodiagnoses: An AI-Powered Framework for Neurodegenerative Disorders

[![GitHub last commit](https://img.shields.io/github/last-commit/Fundacion-de-Neurociencias/neurodiagnoses)](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/Fundacion-de-Neurociencias/neurodiagnoses)](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/issues)
[![License](https://img.shields.io/github/license/Fundacion-de-Neurociencias/neurodiagnoses)](LICENSE)

**Neurodiagnoses** is an AI-powered, open-source framework designed to integrate multi-modal data and advanced computational models to enhance the diagnostic precision and prognostic understanding of complex neurodegenerative diseases (NDDs).

This project moves beyond traditional, static disease labels towards a **probabilistic, tridimensional diagnostic system** that reflects the biological and clinical complexity of each patient.

> **⚠️ Research Use Only Disclaimer**
> This entire project is a research prototype and is **NOT a medical device**. It has not been validated for clinical use, nor does it have FDA/EMA approval. It **must not** be used for clinical diagnosis or patient management.

---

##  Live Interactive Demo

The easiest way to interact with the Neurodiagnoses prototype is through our live Gradio application, hosted on Hugging Face Spaces. This interface allows for both single-patient analysis and batch processing of research cohorts.

**➡️ [Launch Interactive Neurodiagnoses App](https://huggingface.co/spaces/fneurociencias/Neurodiagnoses)**

---

## ️ Project Overview & Vision

The core vision of Neurodiagnoses is to create a unified, modality-agnostic system capable of learning a deep, disease-agnostic representation of a patient's neurological state. This is achieved by processing diverse inputs through a sophisticated pipeline to generate flexible, clinically relevant outputs.

### High-Level Architecture
```mermaid
graph TD
    subgraph Inputs["A. Dynamic Input Layer"]
        A1[Clinical Data] 
        A2[Imaging Data]
        A3[Biomarker Data]
        A4[Genetic Data]
    end
    
    subgraph Processing["B. Modality-Agnostic Processing"]
        B1[Feature Extraction]
        B2[Biomarker Encoding]
        B3[Missing Data Handler]
    end
    
    subgraph Core["C. Core AI Architecture"]
        C1[Transformer Encoder]
        C2[Disease-Agnostic Representation]
        C3[Uncertainty Quantification]
    end
    
    subgraph Outputs["D. Flexible Output Layer"]
        D1[Disease Classification]
        D2[Biomarker Status Prediction]
        D3[Prognosis & Progression Modeling]
        D4[Risk Prediction (asymptomatic)]
    end
    
    Inputs --> Processing
    Processing --> Core
    Core --> Outputs
```

---

##  Scientific Foundation & Future Development

The development of Neurodiagnoses is guided by state-of-the-art research. Our next phase focuses on implementing two advanced capabilities: Risk Prediction and Prognosis Modeling.

### 1. Risk Prediction Module (`workflows/risk_prediction/`)
-   **Goal:** To predict the age-associated risk of disease onset in asymptomatic individuals.
-   **Inspiration:** This module is inspired by the methodologies of **Akdeniz et al. (2025)** and **Bellou et al. (2025)**. It will focus on developing and validating a **Polygenic Hazard Score (PHS)**. The implementation will follow the best-performing strategy of using **APOE status + a remaining PRS** derived from our high-density imputed genotype data.

### 2. Prognosis Module (`tools/ml_pipelines/prognosis/`)
-   **Goal:** To predict the trajectory of cognitive decline in diagnosed patients using longitudinal data.
-   **Inspiration:** This module is inspired by the work of **Colautti et al. (2025)** and **Milà Alomà et al. (2025)**. It will go beyond baseline data to incorporate crucial temporal features, such as the **age at biomarker positivity** and the **"amyloid-tau interval"**. The models will be stratified by `sex` and `APOE-ε4` status to account for their known effects on progression, with a strong emphasis on **Explainable AI (SHAP)** to identify the key drivers of progression.

## ⚙️ Getting Started for Developers
