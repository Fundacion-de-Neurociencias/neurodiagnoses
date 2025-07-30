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

## 🔗 Dependencies

- sentence-transformers
- rdflib, thefuzz, PubMedBERT
- gradio, scikit-learn, pymed, pandas, huggingface_hub

## 📌 Source Inspiration

Based on:
Pardo et al. (2025) *Enhancing Omics Cohort Discovery through Ontology-Augmented Embedding Models*
https://github.com/JoseAdrian3/NeuroEmbed
