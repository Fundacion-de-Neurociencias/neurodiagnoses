# Unified AI Modeling Workflow

This directory contains scripts for the unified, disease-agnostic AI modeling workflow, which aims to convert heterogeneous patient data into a unified sequence of discrete tokens and feed it into a Transformer-based architecture.

## Scripts

### `1_tokenize_patient_data.py`

This script tokenizes heterogeneous patient data (biomarkers, genetics, clinical scores) into a unified sequence of discrete tokens, suitable for input into a Transformer-based architecture.

**Usage:**

```bash
python 1_tokenize_patient_data.py \
    --data_path data/processed/analysis_ready_dataset.parquet \
    --output_path data/processed/tokenized_patient_sequences.json
```

**Arguments:**

*   `--data_path`: Path to the analysis-ready dataset. (default: `data/processed/analysis_ready_dataset.parquet`)
*   `--output_path`: Path to save the tokenized sequences. (default: `data/processed/tokenized_patient_sequences.json`)

### `2_build_transformer_model.py`

This script defines and builds a conceptual Transformer-based neural network architecture for unified disease modeling.

**Usage:**

```bash
python 2_build_transformer_model.py \
    --vocab_size 10000 \
    --maxlen 200 \
    --embed_dim 32 \
    --num_heads 2 \
    --ff_dim 32
```

**Arguments:**

*   `--vocab_size`: Size of the vocabulary. (default: `10000`)
*   `--maxlen`: Maximum sequence length. (default: `200`)
*   `--embed_dim`: Embedding dimension. (default: `32`)
*   `--num_heads`: Number of attention heads. (default: `2`)
*   `--ff_dim`: Feed forward dimension. (default: `32`)

