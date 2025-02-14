# Neurodiagnoses: AI-Powered CNS Diagnosis Framework

Neurodiagnoses is an open-source AI diagnostic framework for complex central nervous system (CNS) disorders. It integrates multi-modal biomarkers, neuroimaging, and AI-based annotation to improve precision diagnostics and advance research into the underlying pathophysiology of neurological diseases.

## AI-Assisted Diagnosis Approaches

Neurodiagnoses provides two complementary diagnostic models:

### 1. Probabilistic Diagnosis (Differential Diagnosis)

- Generates multiple possible diagnoses, each with an associated probability percentage.
- Useful for differential diagnosis and ranking possible conditions.
- Example Output:
  - 80% Prion Disease
  - 15% Autoimmune Encephalitis
  - 5% Neurodegenerative Disorder

### 2. Tridimensional Diagnosis (Structured)

- Provides structured diagnostic outputs based on three axes:
  - **Axis 1: Etiology** (e.g., genetic, autoimmune, prion, vascular, toxic, inflammatory)
  - **Axis 2: Molecular Markers** (e.g., CSF biomarkers, PET findings, EEG patterns, MRI signatures)
  - **Axis 3: Neuroanatomoclinical Correlations** (e.g., regional atrophy, functional impairment, metabolic alterations)
- This structured model enhances precision medicine and biomarker-guided diagnosis.

### Research Applications: CNS Computational Modeling

- Neurodiagnoses also integrates a research-oriented framework that enables CNS computational modeling.
- This approach includes **multi-omics data integration** (proteomics, genomics, lipidomics, transcriptomics), neuroimaging, and digital health records.
- It supports personalized simulations of disease progression, biomarker discovery, and computational modeling for therapeutic target identification.

Both diagnostic models are designed to operate in parallel, allowing clinical interpretation while also providing insights for research purposes.

---

## Project Contributors

Neurodiagnoses is developed and maintained by [Fundación de Neurociencias](https://www.fneurociencias.org), a non-profit organization dedicated to advancing neuroscience research and innovation.

### Supporting Partners:

- **Fundación de Neurociencias** – Research, clinical validation, and project funding.
- **EBRAINS Collaboratory** – AI-driven neuroscience computing and federated data management.
- **Open-Source AI Community** – Developers, researchers, and clinicians collaborating on AI model development.

---

## Contributing to the Project

We welcome contributions from AI researchers, neuroscientists, and clinicians. Ways to contribute:

- Report issues or feature requests via GitHub Issues.
- Submit pull requests for new functionalities or bug fixes.
- Engage in discussions related to methodology and technical improvements.

### Workflow Overview

The Neurodiagnoses process follows these phases:

1. **Data Acquisition & Integration:** Multi-modal datasets (e.g., ADNI, GP2, PPMI) are sourced and stored in EBRAINS or GitHub repositories.
2. **Data Preprocessing & Feature Engineering:** Cleaning, normalization, and transformation of data for AI model training.
3. **Model Training & Evaluation:** AI models are trained on structured datasets using EBRAINS Jupyter Notebooks and evaluated for performance.
4. **AI-Powered Diagnostic Annotation:** The system produces both probabilistic and tridimensional diagnostic outputs with interpretability enhancements (e.g., SHAP, Grad-CAM).
5. **Data Visualization & Clinical Interpretation:** AI-generated results are structured into interactive reports for clinical and research analysis.
6. **Continuous Model Optimization:** Feedback loops enable the refinement of models based on new data and expert review.

---

## Project Resources

- **EBRAINS Documentation:** [Neurodiagnoses on EBRAINS](https://wiki.ebrains.eu/bin/view/Collabs/neurodiagnoses/)
- **GitHub Repository:** [Neurodiagnoses on GitHub](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses)

---

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/Fundacion-de-Neurociencias/neurodiagnoses.git
