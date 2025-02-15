# Neurodiagnoses: AI-Powered CNS Diagnosis Framework

Neurodiagnoses is an open-source AI diagnostic framework for complex central nervous system (CNS) disorders. It integrates multi-modal biomarkers, neuroimaging, and AI-based annotation to improve precision diagnostics and advance research into the underlying pathophysiology of neurological diseases.

## **🌍 Ecosystem & Integrations**
Neurodiagnoses AI leverages **three core platforms**:

1️⃣ **[GitHub](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses)** → Stores all scripts, pipelines, and model training workflows.  
2️⃣ **[EBRAINS](https://wiki.ebrains.eu/bin/view/Collabs/neurodiagnoses/)** → Provides **HPC resources, neuroimaging, EEG, and biomarker data** for AI training.  
3️⃣ **[Hugging Face](https://huggingface.co/ManMenGon/neurodiagnoses-ai)** → Hosts **pre-trained AI models & datasets** for easy deployment.

---

## **AI-Assisted Diagnosis Approaches**
Neurodiagnoses provides two complementary diagnostic models:

### **1️⃣ Probabilistic Diagnosis (Differential Diagnosis)**
- Generates multiple possible diagnoses, each with an associated probability percentage.
- Useful for differential diagnosis and ranking possible conditions.
- Example Output:
  - 80% Prion Disease
  - 15% Autoimmune Encephalitis
  - 5% Neurodegenerative Disorder

### **2️⃣ Tridimensional Diagnosis (Structured)**
- Provides structured diagnostic outputs based on three axes:
  - **Axis 1: Etiology** (e.g., genetic, autoimmune, prion, vascular, toxic, inflammatory)
  - **Axis 2: Molecular Markers** (e.g., CSF biomarkers, PET findings, EEG patterns, MRI signatures)
  - **Axis 3: Neuroanatomoclinical Correlations** (e.g., regional atrophy, functional impairment, metabolic alterations)
- This structured model enhances precision medicine and biomarker-guided diagnosis.

### **Research Applications: CNS Computational Modeling**
- Neurodiagnoses also integrates a research-oriented framework that enables CNS computational modeling.
- This approach includes **multi-omics data integration** (proteomics, genomics, lipidomics, transcriptomics), neuroimaging, and digital health records.
- It supports personalized simulations of disease progression, biomarker discovery, and computational modeling for therapeutic target identification.

Both diagnostic models are designed to operate in parallel, allowing clinical interpretation while also providing insights for research purposes.

---

## **📊 Project Components**
### **1️⃣ Data Processing (EBRAINS)**
- Raw **EEG, MRI, and biomarker data** is stored and processed in EBRAINS.
- **Feature extraction pipelines** convert raw data into structured datasets.
- **Federated learning techniques** are used for multi-center data training.

### **2️⃣ AI Model Training & Hosting (Hugging Face)**
- Pre-trained models are **fine-tuned on Hugging Face Notebooks**.
- Model artifacts are stored on **Hugging Face Model Hub**.
- Public & private models are **accessible via the Hugging Face API**.

### **3️⃣ Codebase & Pipelines (GitHub)**
- **All scripts and training workflows** are hosted on GitHub.
- **Continuous integration (CI/CD)** for model updates and deployment.

---

## **🚀 Getting Started**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Fundacion-de-Neurociencias/neurodiagnoses.git
cd neurodiagnoses
