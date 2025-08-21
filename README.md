# Neurodiagnoses: An AI-Powered Ecosystem for Neurodegenerative Disorders

[![GitHub last commit](https://img.shields.io/github/last-commit/Fundacion-de-Neurociencias/neurodiagnoses)](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses/commits/main)

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

---
## ⚙️ Getting Started for Developers

... (El resto del README se mantiene sin cambios) ...