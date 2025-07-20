# Neurodiagnoses  

## 📌 What is Neurodiagnoses?  
Neurodiagnoses is an **AI-powered diagnostic framework** designed for **probabilistic modeling, multimodal data integration, and disease progression prediction** in **complex central nervous system (CNS) conditions**.  

The project combines **machine learning, probabilistic reasoning, neuroimaging, biomarkers, and clinical assessments** to enhance diagnostic precision and enable **early-stage disease detection**.  

## 🚀 Key Functionalities  
- **Probabilistic Diagnoses** – AI-based diagnostic modeling using probabilistic approaches.  
- **Tridimensional Annotation** – Integration of neuroimaging, genetic, and clinical data.  
- **Interactive Visualization** – User-friendly interfaces for research and clinical applications.
- **Genetic (Axe 1) Prediction** – Modeling the risk of genetic aetiology. [![CLI Annotator](https://img.shields.io/badge/CLI-Annotation-blue)](tools/annotator/annotate.py)
- **Biomarker (Axe 2) Prediction** – AI-driven estimation of biomarker status and progression.  
- **Phenotypic (Axe 3) Prediction** – Modeling the phenotype, neuroanatomical basis, age of onset, and progression.

# Neurodiagnoses: Biomarker-Agnostic Machine Learning Model

🚀 **Current Achievements:**
- ✅ Developed a biomarker-agnostic machine learning model using `RandomForestClassifier`.
- ✅ Trained the model on simulated data and saved it as `model.pkl`.
- ✅ Uploaded the trained model to Hugging Face:  
  [Neurodiagnoses Hugging Face Repo](https://huggingface.co/fneurociencias/neurodiagnoses-agnostic-ml)
- ✅ Created an API using FastAPI and Uvicorn for real-time predictions.
- ✅ Successfully tested the API locally at `http://127.0.0.1:8000/docs`.
### 🧠 ML Pipelines for Axis 3 (Phenotypic Annotation)

This module implements machine learning pipelines for phenotypic annotation, integrating neuroimaging, clinical, and cognitive data.

📂 **Location:**  
`tools/ml_pipelines/pipelines_axis3.py`

#### 🚀 Features:
- Preprocessing of features such as hippocampal volume, cortical thickness, MMSE scores.  
- RandomForestClassifier-based phenotypic annotation.  
- Ready to integrate with Neurodiagnoses API for interactive usage.

#### 🛠 How to Use:
1. Import the pipeline:
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
2. Future updates will include ADNI and PPMI pipelines for advanced phenotypic progression modeling.

## 📖 Documentation and Resources  
- 🌐 **Website:** [neurodiagnoses.com](https://neurodiagnoses.com/)  
- 📂 **GitHub Repository:** [Neurodiagnoses on GitHub](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses)  
- 🧠 **eBrains Collaboration:** [Neurodiagnoses on eBrains](https://wiki.ebrains.eu/bin/view/Collabs/neurodiagnoses/)  

## 🎯 How to Contribute  
Neurodiagnoses is an **open-source project**, and we welcome contributors from various fields, including **AI, neuroscience, biomedical research, and software development**.  

### **Ways to Contribute:**  
1. **Review the documentation** in GitHub and eBrains.  
2. **Choose an area of interest** (machine learning, neuroimaging, biomarker analysis, software development).  
3. **Follow open issues** in GitHub and collaborate on development, research, or testing.  

### **Contribution Areas:**  
- **📖 Documentation and Organization** – Improving guides, standardizing procedures.  
- **🧠 AI Model Development** – Implementing probabilistic models, biomarker predictors.  
- **📊 Data Integration** – Processing neuroimaging, biomarkers, and clinical data.  
- **🖥️ Platform Development** – APIs, backend, and visualization tools.  
- **🔬 Research and Validation** – Benchmarking models, cross-validating with external datasets.  

## 📌 Getting Started  
To start contributing:  
1. **Fork the repository** and explore the issues section.  
2. **Join discussions** on eBrains and GitHub.  
3. **Clone the project** and start working on tasks aligned with your expertise.  

🔹 **Next Steps:**
- Deploy API on a cloud service for public access.
- Implement authentication for security.

📢 *Contributions are welcome!*
If you have any questions, feel free to reach out through the discussion platform at https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/discussions

---

🛠 **Neurodiagnoses is an open-source project promoted by Fundación de Neurociencias, powered by EBRAINS, GitHub, and the open science community.**  

## CLI Annotation Tool (`annotator`)

A command-line tool that automatically generates a **tridimensional diagnostic annotation** based on structured clinical data (etiology, molecular pathology, and neuroanatomical-clinical correlation).

### Location
```
tools/annotator/annotate.py
tools/annotator/caso.json
```

### How to Use

1. Make sure Python is installed and accessible via Terminal.
2. Navigate to the project folder:
```bash
cd tools/annotator
```
3. Run the tool with your input file:
```bash
python annotate.py --input caso.json --timestamp 2025-06 --output anotacion.txt
```

- `--input`: Path to a `.json` file with clinical features.
- `--timestamp`: Label for the annotation (e.g., month/year).
- `--output`: File to write the output annotation string.

### Output Example
```text
[2025-06]: Sporadic (APOE4 carrier, hypertension, hypercholesterolemia) / amyloid beta, tau; NfL, GFAP, vascular dysfunction markers / right hippocampus: visual memory deficits; parietal lobe: visuospatial impairment; prefrontal cortex: executive dysfunction
```

This tool is part of the probabilistic diagnostic pipeline of **Neurodiagnoses**, helping researchers simulate, annotate, and benchmark real or synthetic cases.
