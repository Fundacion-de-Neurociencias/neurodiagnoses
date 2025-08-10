# Neurodiagnoses

## 📌 What is Neurodiagnoses?

Neurodiagnoses is an **AI-powered diagnostic framework** designed for **probabilistic modeling, multimodal data integration, and disease progression prediction** in **complex central nervous system (CNS) conditions**.

The project combines **machine learning, probabilistic reasoning, neuroimaging, biomarkers, and clinical assessments** to enhance diagnostic precision and enable **early-stage disease detection**.

## 🚀 Key Functionalities

* **Probabilistic Annotation** – AI-based diagnostic modeling using probabilistic networks.
* **Tridimensional Annotation** – Integration of neuroimaging, genetic, and clinical data.
* **Multi-Model Advanced Annotation** – Unified pipeline for comprehensive 3-axis annotation using multiple AI models.
* **Interactive Visualization** – User-friendly interfaces for research and clinical applications.
* **Biomarker Prediction** – AI-driven estimation of biomarker status and progression.
* **Disease Prediction** – Modeling of disease onset, conversion, and progression using ML.

---

## 🧠 Axis Annotation Pipelines

Neurodiagnoses implements a **3-axis annotation system** to classify patients across:

* **Axis 1** – *Etiology / Causative factors*
* **Axis 2** – *Molecular features: Aβ, pTau, tTau*
* **Axis 3** – *Neuroanatomical-clinical (phenotypic) presentation*

You can run automatic annotation on sample patients using:

```bash
python -m tools.annotator.annotate --input data/sample_patient.json --output data/example_annotation.json
```

More examples:

* `data/sample_patient.json` → Axis 2
* `data/sample_patient_axis3.json` → Axis 3
* `data/sample_patient_full.json` → Combined axis annotation

Outputs are saved to corresponding `example_annotation_*.json` files.
Predictions use pre-trained models stored in `/models`.

---

## 🖼 Annotator UI

Use the interactive interface to explore annotation results:

* 📄 `annotator.html`: Web-based local viewer for patient JSON files and annotations.

Open in browser and load a JSON patient file to visualize axis-by-axis classification.

---

## 🚧 Legacy Advanced Multi-Modal Annotator (Deprecated)

This module was an earlier iteration of the advanced annotation framework. Its functionalities have been superseded by the new **Multi-Model Advanced Annotator**.

**Location:** `tools/advanced_annotator/`
**Components:**

* `data_ingestion/`: Parses clinical, imaging, and genetic sources into standardized JSON.
* `run_advanced_annotation.py`: Loads and flattens patient profiles into feature vectors.
* `train_model.py`: Trains advanced ML models (e.g., XGBoost) using multi-modal features.

This pipeline enabled thousands of features per patient and supported precision diagnostics at scale.

---

## ✨ Multi-Model Advanced Annotator

This new, unified pipeline integrates multiple AI models to generate a comprehensive 3-axis annotation for patient data. It combines genetic etiology prediction (Axis 1) with neuropathological phenotyping (Axis 3) to provide a coherent diagnostic output.

**Functionality:**

1.  **Axis 1 (Etiology) Prediction:** Utilizes a Deep Learning model (`tools/phenotype_to_genotype/model.py`) to predict the most probable genetic causes from a simulated list of HPO phenotypes.
2.  **Axis 3 (Neuropathology) Prediction:** Employs a data analysis pipeline (`tools/ml_pipelines/pipelines_axis3_pathology.py`) to generate a phenotypic description from real neuropathology data.
3.  **Axis 2 (Molecular Profile):** Currently a placeholder, awaiting full omics data integration.

**How to Run:**

To execute the multi-model advanced annotator and generate a full 3-axis annotation for a sample patient, run the following command from the project root:

```bash
python -m tools.advanced_annotator.run_advanced_annotation
```

This will process the sample patient data (`patient_database/ND_001.json`) and output a structured annotation to the console.

**Example Output:**

```
--- FINAL MULTI-MODEL ANNOTATION ---
[YYYY-MM-DD]: Predicted Etiology (Probabilistic): [1. GEN_1: XX%], [2. GEN_2: YY%] / Molecular Profile (Requires Full Omics Data) / Neuropathology Profile (t-Tau): High burden in REGION_1 (score: X.XX), REGION_2 (score: Y.YY)
------------------------------------
```

This module represents a significant step towards comprehensive and automated neurodiagnostic assistance.

---

# Neurodiagnoses: Biomarker-Agnostic Machine Learning Model

🚀 **Current Achievements:**

* ✅ Developed a biomarker-agnostic machine learning model using `RandomForestClassifier`.
* ✅ Trained the model on simulated data and saved it as `model.pkl`.
* ✅ Uploaded the trained model to Hugging Face:
  [Neurodiagnoses Hugging Face Repo](https://huggingface.co/fneurociencias/neurodiagnoses-agnostic-ml)
* ✅ Created an API using FastAPI and Uvicorn for real-time predictions.
* ✅ Successfully tested the API locally at `http://127.0.0.1:8000/docs`.

---

## 📖 Documentation and Resources

* 🌐 **Website:** [neurodiagnoses.com](https://neurodiagnoses.com/)
* 📂 **GitHub Repository:** [Neurodiagnoses on GitHub](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses)
* 🧠 **eBrains Collaboration:** [Neurodiagnoses on eBrains](https://wiki.ebrains.eu/bin/view/Collabs/neurodiagnoses/)

---

## 🎯 How to Contribute

Neurodiagnoses is an **open-source project**, and we welcome contributors from various fields, including **AI, neuroscience, biomedical research, and software development**.

### **Ways to Contribute:**

1. **Review the documentation** in GitHub and eBrains.
2. **Choose an area of interest** (machine learning, neuroimaging, biomarker analysis, software development).
3. **Follow open issues** in GitHub and collaborate on development, research, or testing.

### **Contribution Areas:**

* 📖 **Documentation and Organization** – Improving guides, standardizing procedures.
* 🧠 **AI Model Development** – Implementing probabilistic models, biomarker predictors.
* 📊 **Data Integration** – Processing neuroimaging, biomarkers, and clinical data.
* 🖥️ **Platform Development** – APIs, backend, and visualization tools.
* 🔬 **Research and Validation** – Benchmarking models, cross-validating with external datasets.

---

## 📌 Getting Started

To start contributing:

1. **Fork the repository** and explore the issues section.
2. **Join discussions** on eBrains and GitHub.
3. **Clone the project** and start working on tasks aligned with your expertise.

🔹 **Next Steps:**

* Deploy API on a cloud service for public access.
* Implement authentication for security.

📢 *Contributions are welcome!*
If you have any questions, feel free to reach out through the discussion platform at [https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/discussions](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/discussions)

---

🛠 **Neurodiagnoses is an open-source project promoted by Fundación de Neurociencias, powered by EBRAINS, GitHub, and the open science community.**

### Multi-Axis Diagnostic System Implemented
- **Axis 1 (Etiology):** A rules-based classifier for genetic variants.
- **Axis 2 (Molecular):** An ML model for proteomic data.
- **Axis 3 (Phenotype):** An ML model for neuroimaging data.
- The main  script orchestrates all three axes to produce a unified report.

### Multi-Axis Diagnostic System Implemented
- **Axis 1 (Etiology):** A rules-based classifier for genetic variants.
- **Axis 2 (Molecular):** An ML model for proteomic data.
- **Axis 3 (Phenotype):** An ML model for neuroimaging data.
- The main  script orchestrates all three axes to produce a unified report.

### Multi-Axis Diagnostic System Implemented
- **Axis 1 (Etiology):** A rules-based classifier for genetic variants.
- **Axis 2 (Molecular):** An ML model for proteomic data.
- **Axis 3 (Phenotype):** An ML model for neuroimaging data.
- The main  script orchestrates all three axes to produce a unified report.
