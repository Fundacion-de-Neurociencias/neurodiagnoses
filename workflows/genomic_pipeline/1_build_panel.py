# workflows/genomic_pipeline/1_build_panel.py
import subprocess

import pandas as pd

# --- CONFIGURATION ---
INPUT_VCF = "data/simulated/sample_wgs_data.vcf"
OUTPUT_PANEL_PREFIX = "workflows/genomic_pipeline/ND-Panel-v1-prephase"
PHASED_PANEL_FILE = "workflows/genomic_pipeline/ND-Panel-v1.phased.panel"


def build_reference_panel():
    """
    Simulates the process of building a reference panel from WGS data,
    inspired by the methodology in Cheng et al. (2025).

    This process involves:
    1. A simulated Quality Control (QC) step.
    2. A simulated Phasing step (using a placeholder command).
    3. Saving the final panel artifact.
    """
    print(f"--- Starting Reference Panel Build from '{INPUT_VCF}' ---")

    # 1. --- Simulated Quality Control ---
    print("--> STEP 1: Performing simulated Quality Control (QC)...")
    # In a real pipeline, this would use tools like plink or bcftools
    # to filter by HWE, allele count, missingness, etc.
    # Here, we'll just read and re-save the data to simulate a QC pass.
    vcf_data = []
    with open(INPUT_VCF, "r") as f:
        for line in f:
            if not line.startswith("##"):
                vcf_data.append(line.strip().split("\t"))

    df = pd.DataFrame(vcf_data[1:], columns=vcf_data[0])
    df_filtered = df[df["FILTER"] == "PASS"]  # Example: keep only PASS variants

    qc_output_path = f"{OUTPUT_PANEL_PREFIX}.qc.vcf"
    df_filtered.to_csv(qc_output_path, sep="\t", index=False)
    print(f"  > QC passed. Filtered VCF saved to '{qc_output_path}'")

    # 2. --- Simulated Phasing ---
    print("\n--> STEP 2: Performing simulated Haplotype Phasing...")
    # This step would use a tool like SHAPEIT4. We will simulate this with a
    # simple command placeholder.
    phasing_command = (
        f"echo 'Simulating SHAPEIT4 on {qc_output_path} > {PHASED_PANEL_FILE}'"
    )
    print(f"  > Running command: {phasing_command}")
    subprocess.run(phasing_command, shell=True, check=True)
    # Create a dummy output file to represent the result
    with open(PHASED_PANEL_FILE, "w") as f:
        f.write("# This file represents a phased haplotype reference panel.\n")
        f.write("# In a real scenario, it would be in a format like .m3vcf.\n")
    print(f"  > Phasing complete. Panel saved to '{PHASED_PANEL_FILE}'")

    print("\n--- Reference Panel Build Finished Successfully ---")


if __name__ == "__main__":
    build_reference_panel()
