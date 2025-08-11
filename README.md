# Neurodiagnoses

📌 **What is Neurodiagnoses?**

Neurodiagnoses is an AI-powered diagnostic framework designed for probabilistic modeling, multimodal data integration, and disease progression prediction in complex central nervous system (CNS) conditions.
The project combines machine learning, probabilistic reasoning, neuroimaging, biomarkers, and clinical assessments to enhance diagnostic precision and enable early-stage disease detection.

### Core Architecture (`src/`)

The project is being refactored into a professional Python package structure under `src/`. This ensures modularity, testability, and scalability. The key modules are:

- **`src/neurodiagnoses/ontology/`**: Defines the core data structures and controlled vocabularies (e.g., Neuromarker).
- **`src/neurodiagnoses/processing/`**: Contains modules for data ingestion, cleaning, and feature extraction from raw sources.
- **`src/neurodiagnoses/models/`**: Will contain the implementations of the core AI models (e.g., Transformer, GNNs) that operate on the standardized data.

---

🚀 **Key Functionalities**

- **Probabilistic Annotation** – AI-based diagnostic modeling using probabilistic networks.
- **Tridimensional Annotation** – Integration of neuroimaging, genetic, and clinical data.
- **Multi-Model Advanced Annotation** – Unified pipeline for comprehensive 3-axis annotation using multiple AI models.
- **Interactive Visualization** – User-friendly interfaces for research and clinical applications.
- **Biomarker Prediction** – AI-driven estimation of biomarker status and progression.
- **Disease Prediction** – Modeling of disease onset, conversion, and progression using ML.

�� **Axis Annotation Pipelines**

Neurodiagnoses implements a 3-axis annotation system to classify patients across:
- **Axis 1** – Etiology / Causative factors
- **Axis 2** – Molecular features: Aβ, pTau, tTau
- **Axis 3** – Neuroanatomical-clinical (phenotypic) presentation

You can run automatic annotation on sample patients using: `python -m tools.annotator.annotate --input data/sample_patient.json --output data/example_annotation.json`

🖼️ **Annotator UI**

Use the interactive interface to explore annotation results:
- 📄 **annotator.html**: Web-based local viewer for patient JSON files and annotations.

✨ **Multi-Model Advanced Annotator**

This new, unified pipeline integrates multiple AI models to generate a comprehensive 3-axis annotation for patient data. It combines genetic etiology prediction (Axis 1) with neuropathological phenotyping (Axis 3) to provide a coherent diagnostic output.

---

🚀 **Current Achievements:**
- ✅ Developed a biomarker-agnostic machine learning model using `RandomForestClassifier`.
- ✅ Trained the model on simulated data and saved it as `model.pkl`.
- ✅ Uploaded the trained model to Hugging Face: Neurodiagnoses Hugging Face Repo
- ✅ Created an API using FastAPI and Uvicorn for real-time predictions.
- ✅ Successfully tested the API locally at `http://127.0.0.1:8000/docs`.

📖 **Documentation and Resources**
- 🌐 **Website**: neurodiagnoses.com
- 📂 **GitHub Repository**: Neurodiagnoses on GitHub
- 🧠 **eBrains Collaboration**: Neurodiagnoses on eBrains

🎯 **How to Contribute**

Neurodiagnoses is an open-source project, and we welcome contributors. Contribution Areas include: Documentation, AI Model Development, Data Integration, Platform Development, and Research.

📌 **Getting Started**
- Fork the repository and explore the issues section.
- Join discussions on eBrains and GitHub.
- Clone the project and start working on tasks aligned with your expertise.

---

### Future Development Inspired by Recent Research

Based on recent systematic reviews and high-impact studies in the field, the future development of Neurodiagnoses will focus on two key areas:

1.  **Incorporation of Vascular Neuroimaging (CSVD):** Inspired by Lohner et al. (2025), a dedicated pipeline will be developed to quantify Cerebral Small Vessel Disease (CSVD) markers as a core component of the Axis 3 (Phenotypic) assessment, including a "Vascular Burden Score" as a prognostic output.

2.  **Advanced Multi-Pathology Classification:** Inspired by Cruchaga et al. (2025), the Axis 2 (Molecular) classifier will be upgraded to produce a co-pathology probability vector, allowing for the nuanced diagnosis of mixed pathologies. A new "at-risk" flag will be implemented for cognitively normal individuals with high-risk molecular profiles.

Methodological rigor, including mandatory external validation and transparent reporting, will be a core principle of all future model development.
