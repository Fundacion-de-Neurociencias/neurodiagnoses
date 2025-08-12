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

## ️ High-Level Architecture

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

##  Current State: A Functional 3-Axis Prototype
The current implementation is a functional end-to-end prototype that validates the 3-axis diagnostic philosophy, orchestrated by the `unified_orchestrator.py` script.

- ✅ **Axis 1 (Etiology):** A rules-based engine enhanced by a state-of-the-art genomics imputation pipeline in [`/workflows/genomic_pipeline/`](workflows/genomic_pipeline/).
- ✅ **Axis 2 (Molecular):** A research-grade ML pipeline in [`/tools/ml_pipelines/pipelines_axis2_molecular.py`](tools/ml_pipelines/pipelines_axis2_molecular.py) that provides co-pathology probability vectors.
- ✅ **Axis 3 (Phenotype):** An advanced "Severity Mapper" in [`/tools/ml_pipelines/pipelines_axis3_severity_mapping.py`](tools/ml_pipelines/pipelines_axis3_severity_mapping.py) that uses XGBoost and SHAP.

---

##  Key Functionalities
- **Probabilistic Annotation** – AI-based diagnostic modeling using probabilistic networks.
- **Tridimensional Annotation** – Integration of neuroimaging, genetic, and clinical data.
- **Interactive Visualization** – User-friendly interfaces for research and clinical applications.
- **Biomarker Prediction** – AI-driven estimation of biomarker status and progression.
- **Disease Prediction** – Modeling of disease onset, conversion, and progression using ML.

---

##  How to Contribute
This is an open-source project. Please see our `CONTRIBUTING.md` file for details.