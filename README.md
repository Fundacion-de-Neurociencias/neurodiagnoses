# Neurodiagnoses

 **What is Neurodiagnoses?**

Neurodiagnoses is an AI-powered diagnostic framework designed for probabilistic modeling, multimodal data integration, and disease progression prediction in complex central nervous system (CNS) conditions.
The project combines machine learning, probabilistic reasoning, neuroimaging, biomarkers, and clinical assessments to enhance diagnostic precision and enable early-stage disease detection.

---

### **⚠️ Disclaimer: Research Use Only**

**This entire project, including all models and web interfaces, is a research prototype. It is NOT a medical device.**
- It has **not** been validated for clinical use.
- It does **not** have FDA/EMA approval or any other regulatory certification.
- It **must not** be used for clinical diagnosis, patient management, or any medical decision-making.
- The user is solely responsible for ensuring the confidentiality and appropriate use of any data entered into the tool.

---

### ** Interactive Web Interface (Gradio App)**

To make the Neurodiagnoses prototype accessible to non-technical users, the project includes a web-based interface built with Gradio, available at our [Hugging Face Space](https://huggingface.co/spaces/fneurociencias/Neurodiagnoses). The interface provides two main workflows:

1.  **Clinical: Single-Patient Report:**
    * A comprehensive, research-grade data entry form designed for individual case analysis. It is organized into collapsible sections for demographics, advanced genetics (differentiating substitution vs. expansion variants for ~100 genes), a full battery of neuropsychological tests, fluid biomarkers (CSF/Plasma), and detailed neuroimaging data (volumetrics, visual scales, PET/SPECT). It enforces data integrity rules, such as requiring Total Intracranial Volume (TIV) for volumetric normalization.

2.  **Research: Cohort Analysis:**
    * A powerful tool for researchers to upload a full patient dataset in CSV format. The system performs a batch diagnosis on the entire cohort, providing a downloadable results table and a publication-ready methodological summary.

### ** Core Architecture & Vision**

The project's vision is to build a unified, modality-agnostic core model (e.g., a Transformer) that learns a deep representation of a patient's state, enabling a flexible set of outputs like disease classification, biomarker prediction, and progression modeling. This is built upon a standardized **Neuromarker Ontology** (`tools/ontology/neuromarker.py`) that ensures data consistency across the entire platform.

### **️ Key Modules & Pipelines**

-   **Data Ingestion (`tools/data_ingestion/`):** A robust pipeline for parsing and standardizing heterogeneous data sources (e.g., NACC, Cornblath) into the Neuromarker format.
-   **Genomics Pipeline (`workflows/genomic_pipeline/`):** An advanced workflow inspired by Cheng et al. (2025) to enrich genotype data via a custom imputation panel.
-   **ML Pipelines (`tools/ml_pipelines/`):** Contains the functional, research-grade models for the three diagnostic axes, including the proteomics-based **Axis 2** classifier and the neuroimaging-based **Axis 3** Severity Mapper with SHAP explainability.
-   **Unified Orchestrator (`unified_orchestrator.py`):** The central "brain" that integrates the outputs from all three axes into a single, cohesive diagnostic report.
-   **API (`models/api.py`):** A FastAPI server that exposes the full 3-axis diagnostic system for real-time predictions.

---

 **Documentation and Resources**
-  **Website**: neurodiagnoses.com
-  **GitHub Repository**: Neurodiagnoses on GitHub
-  **Gradio Web App**: [Interactive Demo on Hugging Face Spaces](https://huggingface.co/spaces/fneurociencias/Neurodiagnoses)
