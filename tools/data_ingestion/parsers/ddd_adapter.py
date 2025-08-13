import json

import pandas as pd


def parse_ddd_csv(file_path):
    """
    Parses the DDD validation CSV file and converts each row into a patient JSON-like dictionary.
    """
    df = pd.read_csv(file_path)
    patients_data = []

    for index, row in df.iterrows():
        causal_gene = row["causal_gene"]
        hpo_phenotypes = row["hpo_phenotypes"].split(
            ";"
        )  # Split phenotypes by semicolon

        patient_id = f"DDD_{index + 1:03d}"

        patient_json = {
            "patient_id": patient_id,
            "causal_gene": causal_gene,  # This is the ground truth for evaluation
            "phenotypes": hpo_phenotypes,
        }
        patients_data.append(patient_json)

    return patients_data


if __name__ == "__main__":
    # Example usage:
    sample_file_path = "data/ddd/ddd_validation_sample.csv"
    parsed_patients = parse_ddd_csv(sample_file_path)
    for patient in parsed_patients:
        print(json.dumps(patient, indent=2))
