# 🧠 Neurodiagnoses

## 📌 What is Neurodiagnoses?

**Neurodiagnoses** is an **AI-powered diagnostic framework** for **probabilistic modeling, multimodal data integration, and disease progression prediction** in **complex central nervous system (CNS) conditions**.

The project combines **machine learning**, **probabilistic reasoning**, **neuroimaging**, **omics biomarkers**, and **clinical assessments** to enhance diagnostic precision and enable **early-stage disease detection**.

---

## 🚀 Key Functionalities

✅ **Probabilistic Diagnoses** – AI-based diagnostic modeling using probabilistic approaches.
✅ **Tridimensional Annotation** – Integration of neuroimaging, genetic, and clinical data.
✅ **Interactive Visualization** – User-friendly interfaces for research and clinical applications.
✅ **Genetic (Axis 1) Prediction** – Modeling the risk of genetic aetiology. [![CLI Annotator](https://img.shields.io/badge/CLI-Annotation-blue)](tools/annotator/annotate.py)
✅ **Biomarker (Axis 2) Prediction** – AI-driven estimation of biomarker status and progression.
✅ **Phenotypic (Axis 3) Prediction** – Modeling the phenotype, neuroanatomical basis, age of onset, and progression.

---

## 🧪 Machine Learning Modules

### Biomarker-Agnostic ML Model

* ✅ **RandomForestClassifier** trained on synthetic data for demonstration.
* ✅ API created using **FastAPI** and tested at `http://127.0.0.1:8000/docs`.
* ✅ Hugging Face: [Neurodiagnoses ML Model](https://huggingface.co/fneurociencias/neurodiagnoses-agnostic-ml).

---

### 🧠 ML Pipelines for Axis 3 (Phenotypic Annotation)

This module implements **machine learning pipelines** for phenotypic annotation, integrating **neuroimaging**, **clinical**, and **cognitive data**.

📂 **Location:**
`tools/ml_pipelines/pipelines_axis3.py`

#### 🚀 Features:

* Preprocessing features such as **hippocampal volume**, **cortical thickness**, **ventricular volume**, and **MMSE scores**.
* RandomForestClassifier-based phenotypic annotation.
* Integration-ready with Neurodiagnoses API for interactive usage.

#### 🛠 How to Use:

```python
from tools.ml_pipelines.pipelines_axis3 import Axis3Pipeline

pipeline = Axis3Pipeline()
input_data = {
    "hippocampal_volume": 3.2,
    "cortical_thickness": 1.8,
    "ventricular_volume": 42.5,
    "age": 68,
    "MMSE": 24
}
prediction = pipeline.predict(input_data)
print("Predicted Phenotypic Annotation:", prediction)
```

#### 📈 Advanced Pipelines (ADNI and PPMI):

The integrated **ADNI and PPMI pipelines** enable advanced disease progression modeling and biomarker prediction.

📂 **Location:**
`tools/ml_pipelines/src/`

---

## 📖 Documentation and Resources

🌐 **Website:** [neurodiagnoses.com](https://neurodiagnoses.com/)
📂 **GitHub Repository:** [Neurodiagnoses on GitHub](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses)
🧠 **eBrains Collaboration:** [Neurodiagnoses on eBrains](https://wiki.ebrains.eu/bin/view/Collabs/neurodiagnoses/)

---

## 👨‍🔬 How to Contribute

Neurodiagnoses is an **open-source project**. We welcome contributors from **AI**, **neuroscience**, **biomedical research**, and **software development**.

### Areas to Contribute:

* 📖 **Documentation** – Improve guides and standardize procedures.
* 🧠 **AI Models** – Probabilistic models, biomarker predictors.
* 📊 **Data Integration** – Neuroimaging, omics biomarkers, clinical data.
* 🖥️ **Platform Development** – APIs, backend tools, visualization.
* 🔬 **Research and Validation** – Benchmark models, cross-validate with external datasets.

📢 *Contributions are welcome! Start by forking the repo, exploring open issues, and joining the discussions:*
👉 [GitHub Discussions](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/discussions)

---

## 🛠 CLI Annotation Tool (`annotator`)

A command-line tool to generate a **tridimensional diagnostic annotation** from structured clinical data.

📂 **Location:**

```
tools/annotator/annotate.py
tools/annotator/caso.json
```

### 🚀 How to Use:

```bash
cd tools/annotator
python annotate.py --input caso.json --timestamp 2025-06 --output anotacion.txt
```

* `--input`: JSON file with clinical features.
* `--timestamp`: Label for annotation (e.g., month/year).
* `--output`: Output annotation file.

### 📝 Example Output:

```
[2025-06]: Sporadic (APOE4 carrier, hypertension, hypercholesterolemia) / amyloid beta, tau; NfL, GFAP, vascular dysfunction markers / right hippocampus: visual memory deficits; parietal lobe: visuospatial impairment; prefrontal cortex: executive dysfunction
```

This is part of Neurodiagnoses’ **probabilistic diagnostic pipeline**, supporting researchers in simulating, annotating, and benchmarking cases.

---

## 🔥 Next Steps

* 🌐 Deploy API on cloud for public access.
* 🔒 Implement user authentication.
* 🧪 Expand ML pipelines to integrate omics data and longitudinal predictions.

---

🛠 **Neurodiagnoses is an open-source project promoted by Fundación de Neurociencias, powered by EBRAINS, GitHub, and the open science community.**
