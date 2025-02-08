# Neurodiagnoses: AI-Powered CNS Diagnosis Framework

Neurodiagnoses is an open-source AI diagnostic framework for complex central nervous system (CNS) disorders. It integrates multi-modal biomarkers, neuroimaging, and AI-based annotation to improve precision diagnostics and to advance research into the underlying pathophysiology of neurological diseases.

## Two Diagnostic Approaches

Neurodiagnoses offers two complementary AI-assisted diagnosis systems:

### 1. Probabilistic Diagnosis (Traditional)
- Generates multiple possible diagnoses, each with an associated probability percentage.
- Useful for differential diagnosis and ranking possible conditions.
- Example Output:
  - 80% Prion Disease
  - 15% Autoimmune Encephalitis
  - 5% Alzheimer's Disease

### 2. Tridimensional Diagnosis (Structured)
- Provides structured diagnostic outputs based on three axes:
  - **Axis 1: Etiology** (e.g., genetic, autoimmune, prion, vascular, toxic)
  - **Axis 2: Molecular Markers** (e.g., biomarkers from CSF, PET, EEG, MRI)
  - **Axis 3: Neuroanatomoclinical Correlations** (e.g., MRI atrophy, PET findings, functional impairments)
- Enhances precision medicine and biomarker-guided diagnosis.

### Research Dimension: CNS Digital Twins
- In addition to clinical diagnostics, Neurodiagnoses incorporates a research-oriented framework that creates a "digital twin" of the CNS.
- This digital twin integrates omics data (proteomics, genomics, lipidomics, transcriptomics), multi-modal neuroimaging, and digital health records.
- It enables personalized simulations of disease progression, supports biomarker discovery, and helps identify new therapeutic targets.
- For every patient case, both the traditional (probabilistic) and structured (tridimensional) diagnosis systems are provided, alongside advanced digital twin simulations for research purposes.

---

## Project Partners

Neurodiagnoses is promoted and supported by [Fundación de Neurociencias](https://www.fneurociencias.org), a non-profit organization dedicated to advancing neuroscience research and innovation.

**Collaborating Institutions & Contributors:**
- **Fundación de Neurociencias** – Research, clinical validation, and funding.
- **EBRAINS Collaboratory** – AI-powered neuroscience computing and data storage.
- **Open-Source AI Community** – Researchers, developers, and clinicians contributing to the project.

---

## Contributing

We welcome contributions from researchers, AI developers, neuroscientists, and clinicians. To contribute:
- Open an issue for bug reports or feature requests.
- Submit a pull request for improvements or new notebooks.
- Use GitHub Discussions for technical and research-related discussions.

### Workflow Overview
The Neurodiagnoses process consists of the following phases:
1. **Data Acquisition & Integration:** External datasets (e.g., ADNI, GP2, PPMI) are downloaded and uploaded to EBRAINS Buckets or stored in GitHub.
2. **Data Preprocessing & Feature Engineering:** Data is cleaned, normalized, and formatted for AI model training; missing values are imputed.
3. **AI Model Training & Evaluation:** Models are trained using historical data in EBRAINS Jupyter Notebooks and GitHub-hosted scripts; performance is evaluated.
4. **Diagnostic Annotation System:** AI produces both probabilistic and tridimensional diagnostic outputs, with interpretability provided by tools such as SHAP.
5. **Structured Reports & Clinical Validation:** AI-generated reports are reviewed by clinicians, and feedback is used to refine the models.
6. **Continuous Improvement & Collaboration:** The system is updated regularly based on new data, research contributions, and clinical feedback.

---

## Project Resources

- **EBRAINS Wiki:** [Neurodiagnoses on EBRAINS](https://wiki.ebrains.eu/bin/view/Collabs/neurodiagnoses/)
- **GitHub Repository:** [Neurodiagnoses on GitHub](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses)

---

## Get Started

1. Clone the repository:  
   `git clone https://github.com/manuelmenendezgonzalez/neurodiagnoses.git`
2. Install dependencies:  
   `pip install -r requirements.txt`
3. Open Jupyter Notebooks (for example, the Biomarker Classifier Notebook):  
   [Biomarker Classifier Notebook](https://lab.jsc.ebrains.eu/hub/user-redirect/lab/tree/shared/Neurodiagnoses/biomarker_classifier.ipynb)

---

## License

Neurodiagnoses is released under the [MIT License](LICENSE).  
This license allows you to use, modify, and distribute the software, provided that you give appropriate credit to the original authors.

Learn more about Fundación de Neurociencias at [FNeurociencias.org](https://www.fneurociencias.org).

---

This README provides an overview of both the clinical diagnostic applications and the research-oriented expansion into CNS digital twins within Neurodiagnoses, outlining our dual approach to precision CNS diagnostics and computational neuroscience research.
