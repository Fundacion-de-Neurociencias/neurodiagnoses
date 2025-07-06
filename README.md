# Neurodiagnoses  

## 📌 What is Neurodiagnoses?  
Neurodiagnoses is an **AI-powered diagnostic framework** designed for **probabilistic modeling, multimodal data integration, and disease progression prediction** in **complex central nervous system (CNS) conditions**.  

The project combines **machine learning, probabilistic reasoning, neuroimaging, biomarkers, and clinical assessments** to enhance diagnostic precision and enable **early-stage disease detection**.  

## 🚀 Key Functionalities  
- **Probabilistic Diagnoses** – AI-based diagnostic modeling using probabilistic approaches.  
- **Tridimensional Annotation** – Integration of neuroimaging, genetic, and clinical data.  
- **Interactive Visualization** – User-friendly interfaces for research and clinical applications.  
- **Biomarker Prediction** – AI-driven estimation of biomarker status and progression.  
- **Disease Prediction** – Modeling of disease onset, conversion, and progression using ML.  

# Neurodiagnoses: Biomarker-Agnostic Machine Learning Model

🚀 **Current Achievements:**
- ✅ Developed a biomarker-agnostic machine learning model using `RandomForestClassifier`.
- ✅ Trained the model on simulated data and saved it as `model.pkl`.
- ✅ Uploaded the trained model to Hugging Face:  
  [Neurodiagnoses Hugging Face Repo](https://huggingface.co/fneurociencias/neurodiagnoses-agnostic-ml)
- ✅ Created an API using FastAPI and Uvicorn for real-time predictions.
- ✅ Successfully tested the API locally at `http://127.0.0.1:8000/docs`.




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
