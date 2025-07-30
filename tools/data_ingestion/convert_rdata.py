# tools/data_ingestion/convert_rdata.py
import pyreadr
import os
import pandas as pd

def convert_pathology_matrix(rdata_path, output_dir='data/cornblath'):
    """
    Reads the .RData file, extracts the patient IDs (projid) from the index,
    and saves the pathology matrix as a CSV.
    """
    print(f"Reading RData file from: {rdata_path}")

    try:
        result = pyreadr.read_r(rdata_path)
        df_name = list(result.keys())[0]
        pathology_df = result[df_name]

        # --- FIX: The patient IDs are in the DataFrame's index ---
        # We convert the index to a regular column named 'projid'.
        pathology_df.index.name = 'projid'
        pathology_df.reset_index(inplace=True)

        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "pathology_matrix.csv")

        # Save the corrected DataFrame to CSV
        pathology_df.to_csv(output_path, index=False)

        print(f"Successfully converted and saved data to: {output_path}")
        print(f"DataFrame shape: {pathology_df.shape}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    source_file_path = r'C:\Users\usuario\Downloads\SourceData\FigS9a_SourceData_PathMatrix.RData'

    if not os.path.exists(source_file_path):
        print(f"ERROR: Source file not found at '{source_file_path}'")
    else:
        convert_pathology_matrix(rdata_path=source_file_path)