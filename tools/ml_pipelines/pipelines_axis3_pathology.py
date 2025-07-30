# tools/ml_pipelines/pipelines_axis3_pathology.py
import pandas as pd
import os

class Axis3PathologyPipeline:
    def __init__(self, data_path='data/cornblath/pathology_matrix.csv'):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Pathology matrix not found at {data_path}")

        self.pathology_df = pd.read_csv(data_path, index_col='projid')

        # --- FIX: Ensure the index is of integer type ---
        # This prevents mismatches between the input `patient_id` (int) 
        # and the index type, which might be read as float or object.
        self.pathology_df.index = self.pathology_df.index.astype(int)

        print(f"INFO: Axis 3 Pathology Pipeline initialized with data from '{data_path}'.")

    def predict(self, patient_id):
        try:
            # The input patient_id is an integer, so now it will match the index type
            patient_scores = self.pathology_df.loc[patient_id]
        except KeyError:
            return f"Phenotype (Pathology) not available for patient {patient_id}"

        # Simple Analysis: Find top 3 regions with highest Tau pathology
        tau_columns = [col for col in patient_scores.index if 'tau' in col.lower()]
        if not tau_columns:
            return "Phenotype (Pathology) could not be determined: No tau columns found."

        top_tau_regions = patient_scores[tau_columns].nlargest(3)

        region_strings = [f"{region.replace('_tau', '')} (score: {score:.2f})" for region, score in top_tau_regions.items()]
        phenotype_description = "Neuropathology Profile (t-Tau): High burden in " + ", ".join(region_strings)

        return phenotype_description