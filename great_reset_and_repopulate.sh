KB_DIR="data/knowledge_base"
RAW_GENOMICS="data/raw/genomics/gwas_catalog_sample_AD.tsv"
RAW_IMAGING="data/raw/imaging/neuroscience_sample.csv"

# --- FASE 1: Limpieza Total de la Base de Conocimiento ---
echo "INFO: Performing a 'Great Reset'. Deleting old KB files..."
rm -f ${KB_DIR}/*.csv
# Dejamos el topics.csv que es nuestro manifiesto
mv ${KB_DIR}/topics.csv ${KB_DIR}/topics.csv.bak
rm -f ${KB_DIR}/*.csv
mv ${KB_DIR}/topics.csv.bak ${KB_DIR}/topics.csv
echo "SUCCESS: Knowledge Base has been wiped clean."

# --- FASE 2: Re-poblar la KB con nuestros parsers (Vía 2) ---
echo "INFO: Re-populating Axis 1 (Genetics) via high-throughput parser..."
python parsers/gwas_api_parser.py --input-json "data/raw/genomics/gwas_api_sample_AD.json" --output-csv "${KB_DIR}/axis1_likelihoods.csv"

echo "INFO: Re-populating Axis 3 (Neuroimaging) via high-throughput parser..."
python parsers/adni_imaging_parser.py --input-csv "$RAW_IMAGING" --output-csv "${KB_DIR}/axis3_likelihoods.csv"

echo "SUCCESS: Vía 2 data ingestion complete."

# --- FASE 3: Enriquecer la KB con nuestro orquestador (Vía 1) ---
echo "INFO: Enriching the new KB with the Autonomous Orchestrator..."
python workflows/knowledge_ingestion/7_knowledge_orchestrator.py

# --- FASE 4: Verificación ---
echo "INFO: Master Regeneration complete. Verifying the new, clean Knowledge Base..."
ls -lh ${KB_DIR}

echo -e "\n--- [ Contenido Final de axis3_likelihoods.csv ] ---"
column -s, -t < "${KB_DIR}/axis3_likelihoods.csv"
echo "--------------------------------------------------------"
