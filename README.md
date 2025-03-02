# Neurodiagnoses: AI-Powered CNS Diagnosis Framework

Neurodiagnoses is an open-source AI diagnostic framework for complex central nervous system (CNS) disorders. It integrates multi-modal biomarkers, neuroimaging, and AI-based annotation to improve precision diagnostics and advance research into the underlying pathophysiology of neurological diseases.

## Ecosystem & Integrations

Neurodiagnoses AI operates across three core platforms:

GitHub: Stores all scripts, pipelines, and model training workflows.  
EBRAINS: Provides HPC resources, neuroimaging, EEG, and biomarker data for AI training.  
Hugging Face: Hosts pre-trained AI models & datasets for easy deployment.  

By using all three platforms, we ensure that AI models, datasets, and neuroimaging resources work seamlessly together.

## AI-Assisted Diagnosis Approaches

Neurodiagnoses provides two complementary AI-powered diagnostic models:

Probabilistic Diagnosis (Differential Diagnosis):

Generates multiple possible diagnoses, each with an associated probability percentage.  
Useful for differential diagnosis and ranking possible conditions.  
Example Output:  
80% Prion Disease  
15% Autoimmune Encephalitis  
5% Neurodegenerative Disorder  

Tridimensional Diagnosis (Structured):

Provides structured diagnostic outputs based on three axes:  
Axis 1: Etiology (e.g., genetic, autoimmune, prion, vascular, toxic, inflammatory)  
Axis 2: Molecular Markers (e.g., CSF biomarkers, PET findings, EEG patterns, MRI signatures)  
Axis 3: Neuroanatomoclinical Correlations (e.g., regional atrophy, functional impairment, metabolic alterations)  

Enhances precision medicine and biomarker-guided diagnosis.

## Research Applications: CNS Computational Modeling

Multi-omics integration (proteomics, genomics, lipidomics, transcriptomics).  
Personalized simulations of disease progression.  
Computational modeling for biomarker discovery and therapeutic target identification.  

## Project Components

Data Processing (EBRAINS):  

Raw EEG, MRI, and biomarker data is stored and processed in EBRAINS.  
Feature extraction pipelines convert raw data into structured datasets.  
Federated learning techniques ensure secure multi-center AI training.  

AI Model Training & Hosting (Hugging Face):  

Pre-trained models are fine-tuned on Hugging Face Notebooks.  
Model artifacts are stored on Hugging Face Model Hub.  
Public & private models are accessible via the Hugging Face API.  

Codebase & Pipelines (GitHub):  

All scripts and training workflows are hosted on GitHub.  
Continuous integration (CI/CD) automates model updates and deployment.  
flowchart TD
    %% Data Acquisition & Integration
    A[Data Acquisition & Recolección de Datos]
    A -->|Datasets multimodales: EEG, MRI, biomarcadores| B[Preprocesamiento & Feature Engineering]
    
    %% AI Model Training & Evaluation
    B -->|Limpieza, normalización y transformación de datos| C[Entrenamiento & Evaluación de Modelos AI]
    C -->|Uso de HPC (EBRAINS) y Notebooks (Hugging Face)| D[Generación de Modelos AI]

    %% AI-Powered Diagnostic Annotation
    D --> E[Diagnóstico Asistido por AI]
    E --> F[Modelo Probabilístico]
    E --> G[Modelo Tridimensional]
    
    %% Clinical Reports & Feedback Loop
    F --> H[Reporte Clínico Interactivo]
    G --> H
    H --> I[Optimización Continua (CI/CD, feedback clínico y de investigación)]

    %% Ecosistema y plataformas
    subgraph Ecosistema y Soporte
      J[GitHub<br/>(Código, pipelines, CI/CD)]
      K[EBRAINS<br/>(Recursos HPC, datos neuroimagen, federated learning)]
      L[Hugging Face<br/>(Model Hub, notebooks de fine-tuning, API de modelos)]
    end

    %% Integración de plataformas
    J --- C
    K --- A
    K --- C
    L --- C


## Getting Started

Clone the Repository:  

git clone https://github.com/Fundacion-de-Neurociencias/neurodiagnoses.git  
cd neurodiagnoses  

Install Dependencies:  

pip install -r requirements.txt  

Connect to Hugging Face:  

huggingface-cli login  

Train a Model:  

from transformers import AutoModelForSequenceClassification, AutoTokenizer  

model_name = "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext"  
tokenizer = AutoTokenizer.from_pretrained(model_name)  
model = AutoModelForSequenceClassification.from_pretrained(model_name)  

## Where to Find Our Models?

All models are available on Hugging Face Model Hub.  

git clone https://huggingface.co/ManMenGon/neurodiagnoses-ai  

## Project Contributors

Neurodiagnoses is developed and maintained by Fundación de Neurociencias, a non-profit organization dedicated to advancing neuroscience research.

Supporting Partners:

Fundación de Neurociencias – Research, clinical validation, and project funding.  
EBRAINS Collaboratory – AI-driven neuroscience computing and federated data management.  
Hugging Face Community – Developers, researchers, and clinicians collaborating on AI model development.  

## Project Resources

GitHub Repository: https://github.com/Fundacion-de-Neurociencias/neurodiagnoses  
Hugging Face Repo: https://huggingface.co/ManMenGon/neurodiagnoses-ai  
EBRAINS Wiki: https://wiki.ebrains.eu/bin/view/Collabs/neurodiagnoses/  

## Contribution & Collaboration

We welcome contributions from AI researchers, neuroscientists, and clinicians. Ways to contribute:

Report issues or feature requests via GitHub Issues.  
Submit pull requests for new functionalities or bug fixes.  
Engage in discussions related to methodology and technical improvements.  
Fine-tune models on Hugging Face Notebooks and contribute AI model enhancements.  

## Workflow Overview

Data Acquisition & Integration: Multi-modal datasets (e.g., ADNI, GP2, PPMI) are sourced and stored in EBRAINS or GitHub repositories.  
Data Preprocessing & Feature Engineering: Cleaning, normalization, and transformation of data for AI model training.  
Model Training & Evaluation: AI models are trained on structured datasets using Hugging Face & EBRAINS resources.  
AI-Powered Diagnostic Annotation: The system produces both probabilistic and tridimensional diagnostic outputs with interpretability enhancements (e.g., SHAP, Grad-CAM).  
Data Visualization & Clinical Interpretation: AI-generated results are structured into interactive reports for clinical and research analysis.  
Continuous Model Optimization: Feedback loops enable the refinement of models based on new data and expert review.  

## License

This project is licensed under the MIT License + Commercial
