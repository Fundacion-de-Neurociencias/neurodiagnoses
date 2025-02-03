# Neurodiagnoses: AI-Powered CNS Diagnosis Framework  

Neurodiagnoses is an **open-source AI diagnostic framework** for **complex central nervous system (CNS) disorders**.  
It integrates **multi-modal biomarkers, neuroimaging, and AI-based annotation** to improve precision diagnostics.

## 🔹 Two Diagnostic Approaches  

Neurodiagnoses offers two complementary AI-assisted diagnosis systems:  

### **1️⃣ Probabilistic Diagnosis (Traditional)**  
- Generates **multiple possible diagnoses**, each with a probability percentage.  
- Useful for **differential diagnosis and ranking possible conditions.**  
- Example Output:  
80% Prion Disease
15% Autoimmune Encephalitis
5% Alzheimer's Disease

### **2️⃣ Tridimensional Diagnosis (Structured)**  
- Diagnoses are based on:  
- **Axis 1: Etiology** (genetic, autoimmune, prion, vascular, toxic)  
- **Axis 2: Molecular Markers** (biomarkers, EEG, neuroinflammation)  
- **Axis 3: Neuroanatomoclinical Correlations** (MRI atrophy, PET, functional impairment)  
- This approach enhances **precision medicine and biomarker-guided diagnosis.**  

🔹 **For every patient case, both systems will be provided, allowing AI-assisted comparison of probability-based vs. structured classification.**  

---
## 🔹 Project Partners
This project is **promoted and supported by** **[Fundación de Neurociencias](https://www.fneurociencias.org)**,  
a non-profit organization committed to **neuroscience research and innovation**.

**Collaborating Institutions & Contributors:**
- **Fundación de Neurociencias** - Research, clinical validation, and funding  
- **EBRAINS Collaboratory** - AI-powered neuroscience computing  
- **Open-Source AI Community** - Contributors developing machine learning models  

## 🤝 Contributing
We welcome contributions from researchers, AI developers, and clinicians.  
- Open an **issue** for bug reports or feature requests.  
- Submit a **pull request** for new notebooks or improvements.  
graph TD;
    A[Data Acquisition & Integration] -->|Download & Upload| B(EBRAINS Data Bucket & GitHub Storage)
    B --> |Preprocessing & Feature Engineering| C[AI Model Training]
    C --> |Train & Evaluate| D[Diagnostic Annotation System]
    D --> |Generate Tridimensional & Probabilistic Diagnosis| E[Structured Reports & Annotations]
    E --> |Clinician Review & Validation| F[Clinical Feedback & AI Evaluation]
    F --> |Model Refinement| C
    F --> |Continuous Collaboration| G[Open-Source Contributions]
    G --> |New Data & Algorithm Updates| C
    G --> |Slack/Discord & GitHub Community| H[Neuroscientists, AI Developers, Clinicians]

---
🔗 **Project Resources:**  
- **EBRAINS Wiki:** [Neurodiagnoses](https://wiki.ebrains.eu/bin/view/Collabs/neurodiagnoses/)  
- **GitHub Repository:** [Neurodiagnoses on GitHub](https://github.com/manuelmenendezgonzalez/neurodiagnoses)  

## 🚀 Get Started
1. Clone the repository: git clone https://github.com/manuelmenendezgonzalez/neurodiagnoses.git
2. Install dependencies: pip install -r requirements.txt
3. Open Jupyter Notebooks:
- [Biomarker Classifier](https://lab.jsc.ebrains.eu/hub/user-redirect/lab/tree/shared/Neurodiagnoses/biomarker_classifier.ipynb)

## 📖 License  
**Neurodiagnoses is released under the [MIT License](LICENSE)**.  
This means you are free to **use, modify, and distribute** the software, as long as credit is given to the original authors.

🔗 **Learn more about Fundación de Neurociencias:** [FNeurociencias.org](https://www.fneurociencias.org)
