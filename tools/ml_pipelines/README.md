**ML pipelines for stratifying neurological biomarkers and predicting disease progression using multi-modal data from ADNI and PPMI cohorts.**

## Project Overview
This research initiative as part of a Master thesis with Fundació de Neurosciences, develops non-invasive diagnostic tools for Alzheimer's and Parkinson's diseases. Our work focuses on:

1. **CSF Biomarker Stratification**  
   Predicting ABETA, pTau, and tTau positivity using:
   - MRI imaging features
   - Cognitive assessments
   - Demographic data
   - Genotypic markers  
   *(ADNI cohort)*

2. **Motor Score Prediction (UPDRS III)**
   Forecasting Parkinson's disease progression(UPDRS III motor scores) using:
   - DAT-SPECT imaging
   - MRI features
   - Genotypic data  
   *(PPMI cohort)*

4. **AD prediction with shallow ANNs**
   Exploring the masking by clinical data of other features predicting AD:
   - MRI imaging features
   - Cognitive assessments
   - Demographic data
   - Genotypic markers  
   *(ADNI cohort)*

## Key Features
- Multi-modal data integration (imaging + clinical + genetic)
- Biomarker ratio analysis for clinical trial triage
- Predictive modeling of disease progression

## Project Structure

- **data/**
  - ADNI/ - Alzheimer's data
    - processed/ - Processed datasets
  - PPMI/ - Parkinson's data
    - processed/ - Processed datasets
  - README.md - Data documentation
  
- **docs/**
  - clinical_background/ - Clinical context
  - methods/ - Research methodologies
  - results/ - Experimental findings
  - README.md - Documentation overview

- **notebooks/**
  - data_processing/ - Transformation notebooks
  - demos/ - Demonstration notebooks
  - exploratory/ - EDA notebooks
  - README.md - Notebooks guide

- **src/**
  - data_processing/ - Data pipelines
    - ADNI/ - ADNI processing scripts
    - PPMI/ - PPMI processing scripts
  - evaluation/ - Model evaluation
  - modelling/ - ML models
    - adni_csf_prediction.py - CSF biomarker prediction
    - adni_ad_diagnosis.py - Alzheimer's diagnosis
    - ppmi_regression.py - UPDRS III regression

- **Files**
  - .gitignore - Untracked files
  - Dockerfile - Container config
  - Makefile - Automation
  - README.md - Project overview
  - requirements.txt - Dependencies
 
  ## Data Sources
| Cohort | Description | Data Types | Access |
|--------|-------------|------------|--------|
| [ADNI](http://adni.loni.usc.edu/) | Alzheimer's Disease Neuroimaging Initiative | MRI, CSF biomarkers, Cognitive scores, Genetics | [Apply for access](http://adni.loni.usc.edu/data-samples/access-data/) |
| [PPMI](https://www.ppmi-info.org/) | Parkinson's Progression Markers Initiative | DAT-SPECT, MRI, UPDRS scores, Genetics | [Apply for access](https://www.ppmi-info.org/access-data-specimens/download-data) |

*Note: This repository contains only code and documentation. Actual patient data must be obtained through official channels.*

## Key Findings
Machine learning models trained on multimodal,non-invasive data can approximate CSF biomarker status and motor score symptom severity with clinically meaningful performance. Our tau positivity pipelines passed the minimum threshold AUC > 0.85 for application as a preliminary screening tool in clinical trial triage. In the PPMI pipelines, Integrating DAT-SPECT and genotypic features outperformed MRI only models and is close to clinical utility benchmark.

Contact
Nick Osaghae - nickosaghae@gmail.com

Project Link:https://github.com/Nick-osa/neurodiagnoses/tree/production-ml/ml
