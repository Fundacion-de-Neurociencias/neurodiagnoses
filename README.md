# Neurodiagnoses: An AI-Powered Framework for Neurodegenerative Disorders

[![GitHub last commit](https://img.shields.io/github/last-commit/Fundacion-de-Neurociencias/neurodiagnoses)](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/Fundacion-de-Neurociencias/neurodiagnoses)](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/issues)
[![License](https://img.shields.io/github/license/Fundacion-de-Neurociencias/neurodiagnoses)](LICENSE)

**Neurodiagnoses** is an AI-powered, open-source framework designed to integrate multi-modal data and advanced computational models to enhance the diagnostic precision and prognostic understanding of complex neurodegenerative diseases (NDDs).

This project moves beyond traditional, static disease labels towards a **probabilistic, tridimensional diagnostic system** that reflects the biological and clinical complexity of each patient.

> **⚠️ Research Use Only Disclaimer**
> This entire project, including all models and web interfaces, is a research prototype and is **NOT a medical device**. It has not been validated for clinical use, nor does it have FDA/EMA approval. It **must not** be used for clinical diagnosis or patient management.

---

## Live Interactive Demo

The easiest way to interact with the Neurodiagnoses prototype is through our live Gradio application, hosted on Hugging Face Spaces. This interface allows for both single-patient analysis and batch processing of research cohorts.

**➡️ [Launch Interactive Neurodiagnoses App](https://huggingface.co/spaces/fneurociencias/Neurodiagnoses)**

---

## The Neurodiagnoses Framework: A 3-Axis Approach

Our core philosophy is a tridimensional diagnostic system that assesses a patient across three fundamental axes to create a holistic profile.

-   **Axis 1 (Etiology):** Focuses on the underlying causes, primarily genetic factors. It analyzes pathogenic mutations and risk alleles to determine the etiological basis of the disease.
-   **Axis 2 (Molecular Profile):** Analyzes fluid and imaging biomarkers (e.g., proteomics, CSF/plasma markers, PET scans) to identify the specific molecular pathologies present, such as amyloidopathy, tauopathy, or synucleinopathy.
-   **Axis 3 (Phenotypic Profile):** Characterizes the clinical and neuroanatomical manifestation of the disease. This includes analyzing cognitive scores and mapping the pattern of neurodegeneration across the brain.

---

## ️ High-Level Architecture

The project's vision is a unified, modality-agnostic system that processes diverse inputs through a sophisticated pipeline to generate flexible, clinically relevant outputs.

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

## Scientific Foundation
The development of Neurodiagnoses is guided by state-of-the-art research in neuroinformatics and artificial intelligence. Our current implementation is inspired by the methodologies of several key studies:

- **Genotype Imputation (Cheng et al., 2025):** Our Axis 1 is being transformed into an advanced genomics pipeline that uses a specialized reference panel to impute high-density genotypes, including structural variants, from low-density array data. This dramatically enhances our ability to detect rare risk variants.
- **Co-Pathology Proteomics (Cruchaga et al., 2025):** Our Axis 2 is modeled after this work. It uses high-performance, explainable boosting models on proteomics data to generate a probability vector for multiple diseases simultaneously, allowing for the quantification of co-pathologies in a single patient.
- **Explainable Severity Mapping (Murad et al., 2025):** Our Axis 3 is evolving into a "Severity Mapper" that uses explainable AI (XAI) to predict clinical severity from regional neuroimaging data, identifying the specific brain areas that contribute most to the diagnosis.

## ⚙️ Getting Started for Developers
This project is developed within GitHub Codespaces to ensure a consistent and reproducible environment.

### Launch the Environment:
1. Navigate to the repository's main page on GitHub.
2. Click the green `<> Code` button, go to the "Codespaces" tab, and create a new codespace.

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Run the Full Prototype:
```bash
python unified_orchestrator.py
```

### Launch the Interactive UI:
```bash
python app.py
```

## How to Contribute
This is an open-source project, and we welcome contributors. Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for details and explore the [open issues](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/issues). Join our [GitHub Discussions](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/discussions) to get involved.