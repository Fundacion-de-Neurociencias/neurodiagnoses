PARSER_SCRIPT="parsers/gwas_api_parser.py"

# --- Parche: Corregir el nombre del argumento en el script ---
echo "INFO: Patching gwas_api_parser.py to correct argument name..."
sed -i 's/--output-tsv/--output-csv/g' "$PARSER_SCRIPT"
echo "SUCCESS: Parser patched."

# --- Re-ejecución del Paso 2 ---
echo "INFO: Re-executing the corrected Axis 1 (Genetics) parser..."
python "$PARSER_SCRIPT"     --input-json "data/raw/genomics/gwas_api_sample_AD.json"     --output-csv "data/knowledge_base/axis1_likelihoods.csv"
echo "SUCCESS: Axis 1 KB has been successfully regenerated."