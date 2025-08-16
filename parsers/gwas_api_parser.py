import json
import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description="Parse GWAS Catalog API JSON to a TSV file.")
    parser.add_argument("--input-json", required=True, help="Path to the input raw JSON file.")
    parser.add_argument("--output-csv", required=True, help="Path for the output TSV file.")
    args = parser.parse_args()

    print(f"INFO: Reading raw JSON from {args.input_json}...")
    with open(args.input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    associations = data.get('_embedded', {}).get('associations', [])
    print(f"INFO: Found {len(associations)} associations to process.")

    processed_data = []
    for assoc in associations:
        # Extracting data with fallbacks for missing keys
        risk_allele = assoc.get('strongestRiskAlleles', [{}])[0].get('riskAlleleName', 'N/A')
        gene = assoc.get('authorReportedGenes', [{}])[0].get('geneName', 'N/A')
        
        # Flattening the nested 'loci' structure to get SNP ID
        snp_id = 'N/A'
        if assoc.get('loci'):
            locus = assoc['loci'][0]
            strongest_variant = locus.get('strongestRiskAlleles', [{}])[0]
            snp_id_parts = strongest_variant.get('variantId', 'rs0').split('_')
            snp_id = snp_id_parts[0] if snp_id_parts else 'N/A'
            
        processed_data.append({
            'DISEASE_TRAIT': assoc.get('traitName', ['N/A'])[0],
            'SNP_ID': snp_id,
            'P_VALUE': assoc.get('pValue', 'N/A'),
            'ODDS_RATIO': assoc.get('orPerCopyNum'), # Can be None
            'BETA': assoc.get('betaNum'), # Can be None
            'RISK_ALLELE': risk_allele,
            'REPORTED_GENE': gene,
        })
        
    df = pd.DataFrame(processed_data)
    print(f"INFO: Writing processed data to {args.output_csv}...")
    df.to_csv(args.output_csv, sep='\t', index=False)
    print("SUCCESS: TSV file created.")

if __name__ == "__main__":
    main()
