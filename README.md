# Neurodiagnoses: An AI-Powered Framework for Neurodegenerative Disorders

[![GitHub last commit](https://img.shields.io/github/last-commit/Fundacion-de-Neurociencias/neurodiagnoses)](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/Fundacion-de-Neurociencias/neurodiagnoses)](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/issues)
[![License](https://img.shields.io/github/license/Fundacion-de-Neurociencias/neurodiagnoses)](LICENSE)

**Neurodiagnoses** is an AI-powered, open-source framework designed to integrate multi-modal data and advanced computational models to enhance the diagnostic precision and prognostic understanding of complex neurodegenerative diseases (NDDs).

This project moves beyond traditional, static disease labels towards a **probabilistic, tridimensional diagnostic system** that reflects the biological and clinical complexity of each patient.

> **⚠️ Research Use Only Disclaimer**
> This entire project is a research prototype and is **NOT a medical device**. It must not be used for clinical diagnosis or patient management.

---

## Licensing

Neurodiagnoses operates under a dual-licensing model to support both open-source collaboration and commercial applications.

*   **Open-Source License:** The core project is licensed under the **MIT License**, allowing for broad use, modification, and distribution for open-source and research purposes. See the [LICENSE](LICENSE) file for details.
*   **Commercial License:** For commercial use cases, dedicated support, or advanced features, a commercial license is required. This model enables sustainable development and specialized enterprise solutions. For more information on commercial terms and contributor agreements, please refer to the [Dual License Information](DUAL_LICENSE.md) file.

---

## Project Overview & Vision

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

## Current State: A Functional 3-Axis Prototype
While the final vision is a single Transformer model, the current implementation is a functional end-to-end prototype that validates the 3-axis diagnostic philosophy. This system is orchestrated by the `unified_orchestrator.py` script.

*   **✅ Axis 1 (Etiology):** Implemented via a rules-based engine in `/models/probabilistic_annotation/axis_1_classifier.py`, which is enhanced by a state-of-the-art genomics imputation pipeline in `/workflows/genomic_pipeline/`.

*   **✅ Axis 2 (Molecular):** Implemented as a research-grade ML pipeline in `/tools/ml_pipelines/pipelines_axis2_molecular.py`. It trains models like XGBoost and provides co-pathology probability vectors, inspired by Cruchaga et al. (2025).

*   **✅ Axis 3 (Phenotype):** Implemented as an advanced "Severity Mapper" in `/tools/ml_pipelines/pipelines_axis3_severity_mapping.py`. Inspired by Murad et al. (2025), it uses XGBoost and SHAP to predict clinical severity from regional neuroimaging data.

---

---


## Future Development Inspired by Recent Research

Based on state-of-the-art research, the future development of Neurodiagnoses will focus on:

1.  **Implementation of a Polygenic Hazard Score (PHS) Module for Risk Prediction:**
    * Inspired by Akdeniz et al. (2025), a dedicated module will be developed to predict the age-associated risk of disease onset in asymptomatic individuals. This will involve implementing a PHS model (e.g., Elastic Net-regularized Cox regression) that leverages the high-density genetic data from our imputation pipeline.

2.  **Advanced Progression Modeling for Prognosis:**
    * The "Prognosis & Progression Modeling" output layer will be a core focus, using longitudinal data (data collected over time) to predict the trajectory of the disease in diagnosed patients.

3.  **Incorporation of Vascular Neuroimaging (CSVD):**
    * Inspired by Lohner et al. (2025), a dedicated pipeline will continue to be developed to quantify Cerebral Small Vessel Disease (CSVD) markers as a core component of the Axis 3 (Phenotypic) assessment.

## Repository Structure & Key Modules
This repository is a complex ecosystem. For a complete map, please consult the Project Overview Document. Below is a summary of the most critical components.

### Data & Ontology
*   `/tools/ontology/neuromarker.py`: The heart of the project. Defines the standardized `PatientRecord` and `Biomarker` classes based on the Neuromarker Ontology, a cross-disease framework that expands on CADRO.

*   `/tools/data_ingestion/`: The main pipeline for ETL (Extract, Transform, Load). Contains parsers and adapters (e.g., `nacc_adapter.py`, `cornblath_adapter.py`) to convert raw data from sources like NACC and ADNI into standardized `PatientRecord` objects.

*   `/data/`: Contains simulated datasets, ontologies (e.g., `hp.obo`), and will host processed, analysis-ready datasets.

### Workflows & Models
*   `/workflows/`: Contains high-level, multi-step pipelines.
    *   `preprocessing_pipeline/`: Unifies data from all ingestion adapters into a single, analysis-ready dataset (e.g., a Parquet file).
    *   `genomic_pipeline/`: The state-of-the-art workflow for genetic data enrichment via genotype imputation using a custom reference panel.
    *   `validation_pipeline/`: Scripts for rigorous, scientific cross-validation of models against neuropathological ground truth.

*   `/tools/ml_pipelines/`: Contains the Python classes for the individual AI models of the 3-axis prototype.

*   `/models/`: Contains a mix of legacy and current components, including the FastAPI application (`api.py`) for serving models and the final `meta_classifier` module.

### Frontend & API
*   `/docs/`: Contains all files for the static website hosted at neurodiagnoses.com.

*   `app.py`: A professional, interactive Gradio web application that serves as a user-friendly frontend for the entire project. It has separate tabs for clinical (single-patient) and research (cohort analysis) use cases. It is deployed and publicly accessible via Hugging Face Spaces.

*   `/models/api.py`: A FastAPI application that exposes the 3-axis diagnostic system as a real-time web service.

---

## Releases & Getting Started

### Latest Release
The latest official release is v0.4.0: Integrated 3-Axis Diagnostic Prototype. This release marks the successful integration of all three diagnostic axes into a single, functional proof-of-concept.

### How to Use the Prototype
The easiest way to interact with Neurodiagnoses is through the live Gradio web application:

➡️ [Launch Interactive Neurodiagnoses App on Hugging Face Spaces](https://huggingface.co/spaces/fneurociencias/Neurodiagnoses)

For developers, after cloning the repository, the main entry point to run a full simulation is:

```bash
# First, ensure all models are trained
python workflows/AI_training_training_pipeline/train_all_models.py

# Then, run the full 3-axis simulation
python examples/run_full_simulation.py
```

## How to Contribute
This is an open-source project and we welcome contributors. Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for details. Key contribution areas include data integration, model development, and validation studies.