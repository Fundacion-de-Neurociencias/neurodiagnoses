# Neurodiagnoses: An AI-Powered Ecosystem for Neurodegenerative Disorders

[![GitHub last commit](https://img.shields.io/github/last-commit/Fundacion-de-Neurociencias/neurodiagnoses)](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/Fundacion-de-Neurociencias/neurodiagnoses)](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/issues)
[![License](https://img.shields.io/github/license/Fundacion-de-Neurociencias/neurodiagnoses)](LICENSE)

**Neurodiagnoses** is an AI-powered, open-source ecosystem designed to integrate multi-modal data and advanced computational models to enhance the diagnostic precision, risk assessment, and prognostic understanding of complex neurodegenerative diseases (NDDs).

This project moves beyond traditional, static disease labels towards a probabilistic system on classic diagnoses and a tridimensional diagnostic annotation -alternative or complementary to classic diagnoses- that reflects the biological and clinical complexity of each patient.

> **⚠️ Research Use Only Disclaimer**
> This entire project, including all models and web interfaces, is a research prototype and is **NOT a medical device**. It has not been validated for clinical use, nor does it have FDA/EMA approval. It **must not** be used for clinical diagnosis or patient management.

---

## ️ Project Vision & High-Level Architecture

The core vision of Neurodiagnoses is to create a unified, modality-agnostic system capable of learning a deep, disease-agnostic representation of a patient's neurological state. This is achieved by processing diverse inputs through a sophisticated pipeline to generate flexible, clinically relevant outputs.

```mermaid
graph TD
    A1[Axis 1: Etiology (Genetics)] --> C1(Bayesian Inference Engine);
    A2[Axis 2: Molecular Profile (Biomarkers)] --> C1;
    A3[Axis 3: Phenotype (Clinical & Imaging)] --> C1;

    C1 --> D1[Differential Diagnosis Report];
    D1 --> D2[Posterior Probabilities];
    D1 --> D3[Credibility Intervals];
    D1 --> D4[Explainable Evidence Trail];
````

-----

## Scientific Foundation & Core Architecture

The scientific foundation of Neurodiagnoses has evolved towards a fully transparent, "glass-box" approach, centered around a **probabilistic, evidence-based Bayesian inference engine**. This moves away from opaque "black-box" models and allows for a fully traceable and explainable diagnostic process.

### 1. The Dynamic Knowledge Base

The engine is powered by a human-readable and machine-readable Knowledge Base. This is not a static database; it's a dynamic ecosystem designed to grow continuously through a dual-pathway pipeline:

  - **Vía 1 (Autonomous Synthesis):** An autonomous agent periodically scans public academic databases (like **PubMed**) for new high-quality evidence (e.g., meta-analyses, clinical guidelines). It then uses a Large Language Model to extract and integrate this knowledge automatically.
  - **Vía 2 (High-Throughput ETL):** For large, granular datasets (e.g., genomics, imaging atlases), the ecosystem uses dedicated parsers and data transformation tools to ingest and process large data files into structured, actionable knowledge.

### 2. The Bayesian Engine: The Reasoning Core

The `BayesianEngine` is the brain of the system. Its key features are:

  - **Tridimensional Evidence:** It is designed to ingest and reason upon likelihoods from all three diagnostic axes: **Axis 1 (Etiology)**, **Axis 2 (Molecular Profile)**, and **Axis 3 (Phenotype)**.
  - **Differential Diagnosis:** The engine evaluates multiple disease hypotheses in parallel, generating a ranked list of probabilities.
  - **Uncertainty Quantification:** It performs Monte Carlo simulations to calculate not just a single probability, but a **95% Credibility Interval**, providing an honest assessment of the confidence in its own conclusions.

### 3. Expert-in-the-Loop: Curated Knowledge Ingestion

A key feature of the ecosystem is the ability for experts to enrich the Knowledge Base directly. The user interface includes a dedicated tab for **"Curated Knowledge Ingestion,"** allowing a user to provide a URL or DOI of a relevant scientific paper. The system will then automatically scrape, process, and integrate the extracted knowledge.

-----

## ⚙️ Getting Started for Developers

This project is developed within GitHub Codespaces to ensure a consistent and reproducible environment.

### 1. Launch the Environment

Create a new codespace from the repository's main page on GitHub.

### 2. Install Dependencies

In the Codespace terminal, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Launch the Interactive UI

The main entry point to the ecosystem is the Gradio application. This interface allows you to perform tridimensional diagnoses on virtual cases and add new knowledge to the system.

```bash
python app.py
```

After running the command, navigate to the **`PORTS`** tab in your Codespace terminal, find the entry for port `7860`, and click the globe icon (🌐) to open the application in your browser.

-----

## How to Contribute

This is an open-source project. Please see our `CONTRIBUTING.md` file for details and explore the open issues. Join our GitHub Discussions to get involved.
