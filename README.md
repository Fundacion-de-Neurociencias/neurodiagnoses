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

**➡️ [Launch Interactive Neurodiagnoses App](https://hugging face.co/spaces/fneurociencias/Neurodiagnoses)**

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
