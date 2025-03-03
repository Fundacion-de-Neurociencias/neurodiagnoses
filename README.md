# Neurodiagnostics

Neurodiagnostics is an open-source project developing a 3D diagnostic framework for complex central nervous system (CNS) diseases using artificial intelligence (AI). This project is driven by the Fundación de Neurociencias, and is powered by EBRAINS, GitHub, Hugging Face, and the community.

## Goals

* Develop a precise and scalable diagnostic system for CNS diseases.
* Integrate multimodal data (neuroimaging, biomarkers, ontologies).
* Utilize digital twins of the CNS to simulate disease progression.
* Provide structured and explainable diagnoses.

## Key Features

* **Tridimensional Diagnostic Annotation:** Structures diagnoses based on etiology (mainly genetics), molecular biomarkers, and neuroanatomical correlations.
* **Probabilistic Diagnostics:** Provides multiple possible diagnoses with associated probability percentages.
* **CNS Digital Twin Integration:** Incorporates personalized digital replicas of a patient's CNS.
* **AI-powered Annotation:** Enhances standardization and interpretability of diagnostic features.
* **Open-source platform:** Encourages collaboration and community contributions.

## Technologies Used

* Python
* TensorFlow/PyTorch
* NiBabel, Nilearn (Neuroimaging libraries)
* EBRAINS
* Hugging Face
* GitHub

## Installation and Setup

1.  Clone the repository: `git clone https://github.com/Fundacion-de-Neurociencias/neurodiagnoses.git`
2.  Create a virtual environment: `python3 -m venv venv`
3.  Activate the virtual environment: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
4.  Install dependencies: `pip install -r requirements.txt` (Provide the content of requirements.txt below)
5.  Configure EBRAINS credentials as required.

## Usage and Examples

To run the main diagnostic script:

```bash
python neurodiagnostics/main.py --input_data path/to/data --model_type 3d

Replace path/to/data with the actual path to your input data, and --model_type with either 3d or probabilistic.
