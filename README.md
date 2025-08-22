# Neurodiagnoses: An AI-Powered Ecosystem for Neurodegenerative Disorders

[![GitHub last commit](https://img.shields.io/github/last-commit/Fundacion-de-Neurociencias/neurodiagnoses)](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/Fundacion-de-Neurociencias/neurodiagnoses)](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Project Vision & Roadmap: [See our ROADMAP.md](ROADMAP.md)**

**Neurodiagnoses** is an AI-powered, open-source ecosystem designed to integrate multi-modal data and advanced computational models to enhance the diagnostic precision, risk assessment, and prognostic understanding of complex neurodegenerative diseases (NDDs).

> **⚠️ Research Use Only Disclaimer**
> This project is a research prototype and is **NOT a medical device**. It must not be used for clinical diagnosis.

---

## ️ A Dual-System Architecture: Diagnosis & Prognosis

The Neurodiagnoses ecosystem combines a "glass-box" Bayesian engine for deep diagnosis and "black-box" Machine Learning pipelines for prognosis and risk prediction.

> **A detailed technical breakdown of all components is available in the private engine repository:**
> - **[Master Architecture Document](neurodiagnoses-engine/ARCHITECTURE.md)**
> - **[Component Manifest](neurodiagnoses-engine/MANIFEST.md)**
> - **[Operations Playbook](neurodiagnoses-engine/PLAYBOOK.md)**

```mermaid
graph TD
    subgraph Inputs
        A1[Axis 1: Etiology]
        A2[Axis 2: Molecular Pathology]
        A3[Axis 3: Phenotype]
    end
    subgraph "Neurodiagnoses Core"
        C1(Bayesian Diagnostic Engine)
        C2(ML Prognostic & Risk Pipelines)
    end
    subgraph "Output: Neurodegenerative Signature"
        D1[Classical Differential]
        D2[Tridimensional Annotation]
        P1[Prognosis & Risk Score]
    end
    A1 & A2 & A3 --> C1 & C2;
    C1 --> D1 & D2;
    C2 --> P1;
```
⚙️ Getting Started for Developers
This project is architected to run within GitHub Codespaces, which provides a consistent and reproducible development environment.

1. Launch the Environment
Create a new codespace from the main page of the neurodiagnoses repository on GitHub.

2. Initialize Submodules
Our ecosystem uses Git submodules to manage the private neurodiagnoses-engine and the standalone scikg projects. After the Codespace builds, initialize them with this command:

```bash
git submodule update --init --recursive
```

3. Install Dependencies
Install all required Python packages from the master requirements file:

```bash
pip install -r requirements.txt
```

4. Configure API Keys
The knowledge harvesting and generation pipelines require API keys. Copy the template file and add your key:

```bash
cp neurodiagnoses-engine/api-keys.env.template neurodiagnoses-engine/api-keys.env
# Now, open neurodiagnoses-engine/api-keys.env and add your Gemini API key.
```

5. Launch the Application
The main user interface is a Gradio application. Launch it with:

```bash
python app.py
```

Once running, navigate to the PORTS tab in your Codespace terminal, find the entry for port 7860, and click the globe icon (🌐) to open the application in a new browser tab.

How to Contribute
This is an open-source project. Please see our CONTRIBUTING.md file for details and explore the open issues. Join our GitHub Discussions to get involved.
