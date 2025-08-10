# Neurodiagnoses

 **What is Neurodiagnoses?**

Neurodiagnoses is an AI-powered diagnostic framework designed for probabilistic modeling, multimodal data integration, and disease progression prediction in complex central nervous system (CNS) conditions.
The project combines machine learning, probabilistic reasoning, neuroimaging, biomarkers, and clinical assessments to enhance diagnostic precision and enable early-stage disease detection.

### Multi-Axis Diagnostic System Implemented

- **Axis 1 (Etiology):** A rules-based classifier for genetic variants.
- **Axis 2 (Molecular):** An ML model for proteomic data.
- **Axis 3 (Phenotype):** An ML model for neuroimaging data.

The main script orchestrates all three axes to produce a unified report.

---

 **Key Functionalities**

- **Probabilistic Annotation** – AI-based diagnostic modeling using probabilistic networks.
- **Tridimensional Annotation** – Integration of neuroimaging, genetic, and clinical data.
- **Multi-Model Advanced Annotation** – Unified pipeline for comprehensive 3-axis annotation using multiple AI models.
- **Interactive Visualization** – User-friendly interfaces for research and clinical applications.
- **Biomarker Prediction** – AI-driven estimation of biomarker status and progression.
- **Disease Prediction** – Modeling of disease onset, conversion, and progression using ML.

 **Axis Annotation Pipelines**

Neurodiagnoses implements a 3-axis annotation system to classify patients across:
- **Axis 1** – Etiology / Causative factors
- **Axis 2** – Molecular features: Aβ, pTau, tTau
- **Axis 3** – Neuroanatomical-clinical (phenotypic) presentation

You can run automatic annotation on sample patients using:
`python -m tools.annotator.annotate --input data/sample_patient.json --output data/example_annotation.json`

More examples:
- `data/sample_patient.json` → Axis 2
- `data/sample_patient_axis3.json` → Axis 3
- `data/sample_patient_full.json` → Combined axis annotation

Outputs are saved to corresponding `example_annotation_*.json` files. Predictions use pre-trained models stored in `/models`.

️ **Annotator UI**

Use the interactive interface to explore annotation results:
-  **annotator.html**: Web-based local viewer for patient JSON files and annotations.

Open in browser and load a JSON patient file to visualize axis-by-axis classification.

 **Legacy Advanced Multi-Modal Annotator (Deprecated)**

This module was an earlier iteration of the advanced annotation framework. Its functionalities have been superseded by the new Multi-Model Advanced Annotator.

✨ **Multi-Model Advanced Annotator**

This new, unified pipeline integrates multiple AI models to generate a comprehensive 3-axis annotation for patient data. It combines genetic etiology prediction (Axis 1) with neuropathological phenotyping (Axis 3) to provide a coherent diagnostic output.
- **Axis 1 (Etiology) Prediction:** Utilizes a Deep Learning model to predict the most probable genetic causes from a simulated list of HPO phenotypes.
- **Axis 3 (Neuropathology) Prediction:** Employs a data analysis pipeline to generate a phenotypic description from real neuropathology data.
- **Axis 2 (Molecular Profile):** Currently a placeholder, awaiting full omics data integration.

**How to Run:**
`python -m tools.advanced_annotator.run_advanced_annotation`

---

 **Current Achievements:**
- ✅ Developed a biomarker-agnostic machine learning model using `RandomForestClassifier`.
- ✅ Trained the model on simulated data and saved it as `model.pkl`.
- ✅ Uploaded the trained model to Hugging Face: Neurodiagnoses Hugging Face Repo
- ✅ Created an API using FastAPI and Uvicorn for real-time predictions.
- ✅ Successfully tested the API locally at `http://127.0.0.1:8000/docs`.

 **Documentation and Resources**
-  **Website**: neurodiagnoses.com
-  **GitHub Repository**: Neurodiagnoses on GitHub
-  **eBrains Collaboration**: Neurodiagnoses on eBrains

 **How to Contribute**

Neurodiagnoses is an open-source project, and we welcome contributors from various fields.
- **Contribution Areas:** Documentation, AI Model Development, Data Integration, Platform Development, Research and Validation.

 **Getting Started**
- Fork the repository and explore the issues section.
- Join discussions on eBrains and GitHub.
- Clone the project and start working on tasks aligned with your expertise.

 **Next Steps:**
- Deploy API on a cloud service for public access.
- Implement authentication for security.