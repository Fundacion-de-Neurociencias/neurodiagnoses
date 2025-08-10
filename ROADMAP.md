# 🧠 Neurodiagnoses — Semantic Retriever Module

This document outlines the integration of a **semantic retrieval system** based on the methodology described in "NeuroEmbed" (Pardo et al., 2025), adapted for the Neurodiagnoses.Knowledge branch.

## 🔍 Objective

Enable semantic cohort/sample discovery using:
- Ontology-based metadata normalization
- Synonym augmentation
- Natural language query (NLQ) embedding
- Fine-tuning of a PubMedBERT-like model

## 📁 Submodule Structure: neurodiagnoses/semantic_retriever/

semantic_retriever/
├── normalize_metadata.py
├── generate_QA_dataset.py
├── fine_tune_embedder.py
├── run_gradio_interface.py
└── README.md

## 🧭 Phases

1. Ontology mapping
2. QA Dataset generation
3. Embedder fine-tuning
4. Interface deployment

---

## Módulo de Diagnóstico Probabilístico (Prueba de Concepto)

Se ha añadido un nuevo módulo de IA para el diagnóstico probabilístico basado en el **Eje 2 (Perfil Molecular)**. Este módulo es una implementación inspirada en el paper "Protein-based Diagnosis and Analysis of Co-pathologies".

### Cómo Ejecutar la Simulación

Para ejecutar la prueba de concepto y obtener un diagnóstico simulado, sigue estos pasos:

1.  **Configurar el Entorno Virtual (si se trabaja localmente):**
    ```bash
    # Si no lo has hecho ya, crea el entorno
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Entrenar el Modelo de Ejemplo (si no existe):**
    ```bash
    # El script principal requiere un modelo entrenado. Para crear uno de ejemplo:
    python -c "from neurodiagnoses_code.axis_2.classifier import train_model; train_model()"
    ```

4.  **Ejecutar el Diagnóstico:**
    ```bash
    python run_neurodiagnosis.py
    ```

## 🔗 Dependencies

- sentence-transformers
- rdflib, thefuzz, PubMedBERT
- gradio, scikit-learn, pymed, pandas, huggingface_hub

## 📌 Source Inspiration

Based on:
Pardo et al. (2025) *Enhancing Omics Cohort Discovery through Ontology-Augmented Embedding Models*
https://github.com/JoseAdrian3/NeuroEmbed
