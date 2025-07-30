# tools/data_ingestion/parsers/genomics_parser.py
import pandas as pd

def parse_genomics_data(patient_id, csv_path):
    """
    Parses a genomics summary CSV for a specific patient.
    """
    try:
        df = pd.read_csv(csv_path)
        patient_data = df[df['patient_id'] == patient_id]

        if patient_data.empty:
            return None

        output = {
            "key_markers": {},
            "variant_summary": [],
            "raw_data_paths": {"exome_vcf": f"/data/{patient_id}/exome.vcf.gz"} # Placeholder path
        }

        # Handle key markers
        if 'APOE4_alleles' in patient_data.columns:
            output["key_markers"]["APOE4_alleles"] = int(patient_data['APOE4_alleles'].iloc[0])

        # Handle list of other variants
        if 'other_variants' in patient_data.columns and pd.notna(patient_data['other_variants'].iloc[0]):
            variants = str(patient_data['other_variants'].iloc[0]).split(';')
            for variant in variants:
                if ':' in variant:
                    gene, mut = variant.split(':')
                    output["variant_summary"].append({"gene": gene, "variant": mut})
        
        return output

    except Exception as e:
        print(f"An error occurred in genomics_parser: {e}")
        return None
