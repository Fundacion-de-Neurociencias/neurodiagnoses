import json
import csv
from pathlib import Path
import argparse

def main():
    """
    Reads extracted knowledge from a .jsonl file and transforms it into
    structured CSV files for the Bayesian engine's knowledge base.
    """
    parser = argparse.ArgumentParser(description="Transform extracted JSONL data into KB CSVs.")
    parser.add_argument("--input-jsonl", type=Path, required=True, help="Path to the input .jsonl file.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory to save the output CSV files.")
    args = parser.parse_args()

    # Define the headers for our knowledge base files. They include metadata for explainability.
    headers = [
        "biomarker_name",
        "statistic_type",
        "value",
        "ci_lower",
        "ci_upper",
        "sample_size",
        "primary_disease",
        "cohort_description",
        "source_snippet"
    ]

    # Create a dictionary to hold the data for each axis, read from the JSONL
    kb_data = {1: [], 2: [], 3: []}

    print(f"INFO: Reading data from {args.input_jsonl}...")
    if not args.input_jsonl.exists():
        print(f"ERROR: Input file not found at {args.input_jsonl}")
        return

    with open(args.input_jsonl, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line)
                axis = entry.get("axis")
                if axis in kb_data:
                    kb_data[axis].append(entry)
            except json.JSONDecodeError:
                print(f"WARNING: Skipping malformed JSON line: {line.strip()}")

    total_entries = sum(len(v) for v in kb_data.values())
    print(f"INFO: Successfully loaded {total_entries} entries.")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Process and write data for each axis to its corresponding CSV file
    for axis, entries in kb_data.items():
        if not entries:
            print(f"INFO: No entries found for Axis {axis}. Skipping CSV creation.")
            continue

        output_csv_path = args.output_dir / f"axis{axis}_likelihoods.csv"
        print(f"INFO: Writing {len(entries)} entries for Axis {axis} to {output_csv_path}...")

        with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for entry in entries:
                confidence_interval = entry.get("confidence_interval")
                row = {
                    "biomarker_name": entry.get("biomarker_name"),
                    "statistic_type": entry.get("statistic_type"),
                    "value": entry.get("value"),
                    "ci_lower": confidence_interval[0] if confidence_interval and len(confidence_interval) > 0 else "",
                    "ci_upper": confidence_interval[1] if confidence_interval and len(confidence_interval) > 1 else "",
                    "sample_size": entry.get("sample_size", ""),
                    "primary_disease": entry.get("primary_disease"),
                    "cohort_description": entry.get("cohort_description"),
                    "source_snippet": entry.get("source_snippet")
                }
                writer.writerow(row)
    
    print("SUCCESS: Knowledge base CSV files have been created/updated.")

if __name__ == "__main__":
    main()
