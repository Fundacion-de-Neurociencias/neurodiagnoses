import pandas as pd

try:
    df = pd.read_parquet(
        "/workspaces/neurodiagnoses/data/processed/analysis_ready_dataset.parquet"
    )
    print(df.columns.tolist())
except Exception as e:
    print(f"Error reading parquet file: {e}")
