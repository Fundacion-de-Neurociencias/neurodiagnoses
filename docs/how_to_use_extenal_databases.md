# How to Use External Databases in Neurodiagnoses
To enhance the accuracy of our diagnostic models, Neurodiagnoses integrates data from multiple biomedical and neurological research databases. If you are a researcher, follow these steps to access, prepare, and integrate data into the Neurodiagnoses framework.

## 🔗 0. Potential Data Sources
Neurodiagnoses maintains an updated list of potential biomedical databases relevant to neurodegenerative diseases.
📌 Reference: List of Potential Databases

## 🔹 1️⃣ Register for Access
Each external database requires individual registration and access approval. Follow the official guidelines of each database provider.

Ensure that you have completed all ethical approvals and data access agreements before integrating datasets into Neurodiagnoses.
Some repositories require a Data Usage Agreement (DUA) before downloading sensitive medical data.

## 🔹 2️⃣ Download & Prepare Data
Once access is granted, download datasets while complying with data usage policies.
Ensure that the files meet Neurodiagnoses’ format requirements for smooth integration.

## ✅ Supported File Formats
Tabular Data: .csv, .tsv
Neuroimaging Data: .nii, .dcm
Genomic Data: .fasta, .vcf
Clinical Metadata: .json, .xml

## ✅ Mandatory Fields for Integration
Field Name	Description
Subject ID	Unique patient identifier
Diagnosis	Standardized disease classification
Biomarkers	CSF, plasma, or imaging biomarkers
Genetic Data	Whole-genome or exome sequencing
Neuroimaging Metadata	MRI/PET acquisition parameters

## 🔹 3️⃣ Upload Data to Neurodiagnoses
Once preprocessed, data can be uploaded to EBRAINS or GitHub.

### Option 1: Upload to EBRAINS Bucket
Location: 📂 EBRAINS Neurodiagnoses Bucket
Ensure correct metadata tagging before submission.

### Option 2: Contribute via GitHub Repository
Location: 📂 GitHub Data Repository
Create a new folder under /data/ and include dataset description.

> **Note:**  📌 Note: For large datasets, please contact the project administrators before uploading.

## 🔹 4️⃣ Integrate Data into AI Models
Once uploaded, datasets must be harmonized and formatted before AI model training.


# Steps for Data Integration
Open Jupyter Notebooks on EBRAINS to run preprocessing scripts.
Standardize neuroimaging and biomarker formats using harmonization tools.
Use machine learning models to handle missing data and feature extraction.
Train AI models with newly integrated patient cohorts.

> **Note:** 📌 Reference: Detailed instructions can be found in docs/data_processing.md.

## 📂 2️⃣ Database Sources Table
Where to Insert This:

- GitHub: 📂 docs/data_sources.md
- EBRAINS Wiki: 📂 Collabs/neurodiagnoses/Data Sources

## 🧠 Key Databases for Neurodiagnoses

| Database         | Focus Area                 | Data Type                             | Access Link       |
|------------------|-----------------------------|----------------------------------------|--------------------|
| ADNI             | Alzheimer's Disease        | MRI, PET, CSF, cognitive tests         | [ADNI](https://adni.loni.usc.edu) |
| PPMI             | Parkinson’s Disease        | Imaging, biospecimens                 | [PPMI](https://www.ppmi-info.org) |
| GP2              | Genetic Data for PD        | Whole-genome sequencing               | [GP2](https://gp2.org) |
| Enroll-HD        | Huntington’s Disease       | Clinical, genetic, imaging            | [Enroll-HD](https://enroll-hd.org) |
| GAAIN            | Alzheimer's & Cognitive Decline | Multi-source data aggregation     | [GAAIN](https://www.gaain.org) |
| UK Biobank       | Population-wide studies    | Genetic, imaging, health records      | [UK Biobank](https://www.ukbiobank.ac.uk) |
| DPUK             | Dementia & Aging           | Imaging, genetics, lifestyle factors  | [DPUK](https://portal.dementiasplatform.uk) |
| PRION Registry   | Prion Diseases             | Clinical and genetic data             | [PRION Registry](https://www.prion.ucl.ac.uk/clinical-services/clinical-studies/) |
| DECIPHER         | Rare Genetic Disorders     | Genomic variants                      | [DECIPHER](https://decipher.sanger.ac.uk) |


> **Note:** 📌 More Data Sources? If you know a relevant dataset, submit a proposal in GitHub Issues.

## 📂 3️⃣ Collaboration & Partnerships
Where to Insert This:

- GitHub: 📂 docs/collaboration.md
- EBRAINS Wiki: 📂 Collabs/neurodiagnoses/Collaborations

## 🤝 Partnering with Data Providers
Beyond using existing datasets, Neurodiagnoses seeks partnerships with data repositories to:
- ✅ Enable direct API-based data integration for real-time processing.
- ✅ Co-develop harmonized AI-ready datasets with standardized annotations.
- ✅ Secure funding opportunities through joint grant applications.

# 📬 Interested in Partnering?
If you represent a research consortium or database provider, reach out to explore data-sharing agreements.

📧 Contact: info@neurodiagnoses.com

# ✅ Final Notes
Neurodiagnoses continuously expands its data ecosystem to support AI-driven clinical decision-making. Researchers and institutions are encouraged to contribute new datasets and methodologies.

# 🔗 For additional technical documentation:

- 📂 GitHub Repository
- 📂 EBRAINS Collaboration Page

📌 If you experience issues integrating data, open a GitHub Issue or consult the EBRAINS Neurodiagnoses Forum.

