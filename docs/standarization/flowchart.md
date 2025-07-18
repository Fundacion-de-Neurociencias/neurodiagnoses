```mermaid
flowchart TD
    %% Data Acquisition & Integration
    A["Data Acquisition & Integration"]
    A -->|"Multi-modal datasets: EEG, MRI, Biomarkers"| B["Data Preprocessing & Feature Engineering"]
    
    %% AI Model Training & Evaluation
    B -->|"Cleaning, normalization, transformation"| C["AI Model Training & Evaluation"]
    C -->|"Utilizing HPC: EBRAINS and Hugging Face notebooks"| D["AI Model Generation"]

    %% AI-Powered Diagnostic Annotation
    D --> E["AI-Assisted Diagnosis"]
    E --> F["Probabilistic Diagnosis"]
    E --> G["Tridimensional Diagnosis"]
    
    %% Clinical Reports & Feedback Loop
    F --> H["Interactive Clinical Reports"]
    G --> H
    H --> I["Continuous Optimization (CI/CD & Expert Feedback)"]

    %% Ecosystem and Support Platforms
    subgraph "Ecosystem & Platforms"
      J["GitHub (Code, pipelines, CI/CD)"]
      K["EBRAINS (HPC resources, neuroimaging, federated learning)"]
      L["Hugging Face (Model Hub, fine-tuning notebooks, model API)"]
    end

    %% Integration with Platforms
    J --- C
    K --- A
    K --- C
    L --- C
```