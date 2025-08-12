#  Neurodiagnoses: An AI-Powered Framework for Neurodegenerative Disorders

[![GitHub last commit](https://img.shields.io/github/last-commit/Fundacion-de-Neurociencias/neurodiagnoses)](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/Fundacion-de-Neurociencias/neurodiagnoses)](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/issues)
[![License](https://img.shields.io/github/license/Fundacion-de-Neurociencias/neurodiagnoses)](LICENSE)

**Neurodiagnoses** is an AI-powered, open-source framework designed to integrate multi-modal data and advanced computational models to enhance the diagnostic precision, risk assessment, and prognostic understanding of complex neurodegenerative diseases (NDDs).

This project moves beyond traditional, static disease labels towards a **probabilistic, tridimensional diagnostic system** that reflects the biological and clinical complexity of each patient.

> **⚠️ Research Use Only Disclaimer**
> This entire project, including all models and web interfaces, is a research prototype and is **NOT a medical device**. It has not been validated for clinical use, nor does it have FDA/EMA approval. It **must not** be used for clinical diagnosis or patient management.

---

##  Live Interactive Demo

The easiest way to interact with the Neurodiagnoses prototype is through our live Gradio application, hosted on Hugging Face Spaces. This interface allows for both single-patient analysis and batch processing of research cohorts.

**➡️ [Launch Interactive Neurodiagnoses App](https://huggingface.co/spaces/fneurociencias/Neurodiagnoses)**

---

## ️ Project Vision & High-Level Architecture

The core vision of Neurodiagnoses is to create a unified, modality-agnostic system capable of learning a deep, disease-agnostic representation of a patient's neurological state. This is achieved by processing diverse inputs through a sophisticated pipeline to generate flexible, clinically relevant outputs.

```mermaid
graph TD
    A1[Clinical Data] --> B1[Feature Extraction]
    A2[Imaging Data] --> B1
    A3[Biomarker Data] --> B2[Biomarker Encoding]
    A4[Genetic Data] --> B1

    B1 --> C1[Transformer Encoder]
    B2 --> C1
    B3[Missing Data Handler] --> C1

    C1 --> D1[Disease Classification]
    C1 --> D2[Biomarker Status Prediction]
    C1 --> D3[Prognosis & Progression Modeling]
    C1 --> D4[Risk Prediction (asymptomatic)]
```

## Scientific Foundation & Key Modules
The development of Neurodiagnoses is guided by state-of-the-art research. The current functional prototype validates the 3-axis philosophy and is orchestrated by `unified_orchestrator.py`. Below is a map of our key capabilities and the science that inspires them.

### 1. The 3-Axis Diagnostic System
#### Axis 1 (Etiology): Focuses on the underlying causes.

Current Implementation: An advanced genomics pipeline (`/workflows/genomic_pipeline/`) enriches low-density genotype data by imputing millions of variants, including Structural Variants (SVs). This is inspired by the methodology of Cheng et al. (2025). This high-density data then feeds into our risk and classification models.

#### Axis 2 (Molecular Profile): Analyzes fluid and imaging biomarkers.

Current Implementation: A research-grade ML pipeline (`/tools/ml_pipelines/pipelines_axis2_molecular.py`) that produces co-pathology probability vectors, inspired by Cruchaga et al. (2025).

#### Axis 3 (Phenotypic Profile): Characterizes the clinical and neuroanatomical manifestation.

Current Implementation: An advanced "Severity Mapper" (`/tools/ml_pipelines/pipelines_axis3_severity_mapping.py`), inspired by Murad et al. (2025), uses XGBoost and SHAP to map regional neuroimaging data to clinical severity.

### 2. Risk & Prognosis Modeling
#### Risk Prediction Module (`/workflows/risk_prediction/`):

Goal: To predict the age-associated risk of disease onset in asymptomatic individuals.

Inspiration: Inspired by Akdeniz et al. (2025) and Bellou et al. (2025), this module implements a Polygenic Hazard Score (PHS) using APOE status combined with a broader PRS.

#### Prognosis Module (`/tools/ml_pipelines/prognosis/`):

Goal: To predict the trajectory of cognitive decline in diagnosed patients using longitudinal data.

Inspiration: Inspired by Colautti et al. (2025) and Milà Alomà et al. (25), this module incorporates crucial temporal features like the "amyloid-tau interval" and uses Explainable AI (SHAP).

### 3. Data Ingestion & Ontology
- `/tools/ontology/neuromarker.py`: The heart of the project. Defines the standardized `PatientRecord` and `Biomarker` classes, ensuring all data across the project speaks the same language.

- `/tools/data_ingestion/`: The main pipeline for ETL (Extract, Transform, Load), containing parsers and adapters for real-world datasets like NACC and ADNI.

---

## Probabilistic Approach & Co-Pathology Modeling

A core principle of Neurodiagnoses is moving away from single, categorical diagnoses towards a more realistic probabilistic framework. This is crucial for handling the clinical heterogeneity and frequent co-pathologies found in NDDs.

### Key Concepts:

1.  **Probabilistic Outputs:** Instead of a single diagnostic label, the models (especially for Axis 2) are designed to output a **probability vector** across multiple diseases (e.g., AD, PD, FTD, DLB). This is directly inspired by the methodology of **Cruchaga et al. (2025)**.

2.  **Handling Co-Pathologies:** The framework is designed to support two logic modes for interpreting probabilities, as defined in our project documentation:
    * **Independent Multi-Label Probabilities (Sum > 100%):** Each pathology is modeled independently to detect the presence or absence of multiple mechanisms simultaneously (e.g., `AD: 70%`, `LBD: 50%`). This is useful for research and understanding complex cases.
    * **Composite or Exclusive Modeling (Sum = 100%):** The probabilities are normalized to represent the most likely primary diagnosis, which is useful for clinical decision support.

3.  **Uncertainty Quantification:** The "Core AI Architecture" envisions a dedicated module for quantifying the model's confidence in its own predictions, a key step towards clinical translation.

## ⚙️ Getting Started for Developers
This project is developed within GitHub Codespaces to ensure a consistent and reproducible environment.

1. Launch the Environment
Create a new codespace from the repository's main page on GitHub.

2. Install Dependencies
In the Codespace terminal, install the required Python packages:

```bash
pip install -r requirements.txt
```
3. Run the Full Prototype
To run the complete, end-to-end 3-axis simulation, which includes pre-flight checks and model training:

```bash
python unified_orchestrator.py
```
4. Launch the Interactive UI
To start the Gradio web application for interactive use:

```bash
python app.py
```
## How to Contribute
This is an open-source project. Please see our CONTRIBUTING.md file for details and explore the open issues. Join our GitHub Discussions to get involved.
