TOPICS_FILE="data/knowledge_base/topics.csv"
ORCHESTRATOR_SCRIPT="workflows/knowledge_ingestion/7_knowledge_orchestrator.py"

# --- PASO 1: Resetear el manifiesto de tópicos a 'pending' ---
echo "INFO: Resetting the Topic Manifest to re-process all topics..."
# Reemplaza 'processed' o 'no_source_found' por 'pending', ignorando la cabecera
sed -i '2,$s/processed/pending/g; 2,$s/no_source_found/pending/g' "$TOPICS_FILE"
echo "SUCCESS: Topic Manifest has been reset."


# --- PASO 2: Aplicar el parche de la API de Groq al orquestador ---
echo "INFO: Patching the orchestrator to remove the conflicting 'response_format' parameter..."
# Busca la línea que contiene 'response_format' y la elimina
sed -i '/response_format={"type": "json_object"}/d' "$ORCHESTRATOR_SCRIPT"
echo "SUCCESS: Orchestrator has been patched."


# --- PASO 3: Ejecutar el Orquestador Autónomo Corregido ---
echo "INFO: Executing the final, patched Autonomous Knowledge Orchestrator..."
python "$ORCHESTRATOR_SCRIPT"


# --- PASO 4: Verificación Final ---
echo "INFO: Orchestration complete. Verifying the final state of the Knowledge Base..."
echo "--- Final content of topics.csv ---"
column -s, -t < "$TOPICS_FILE"
echo "--- Final content of axis1_likelihoods.csv ---"
column -s, -t < "data/knowledge_base/axis1_likelihoods.csv" || echo "File is empty or does not exist."
echo "--- Final content of axis2_likelihoods.csv ---"
column -s, -t < "data/knowledge_base/axis2_likelihoods.csv" || echo "File is empty or does not exist."
echo "--- Final content of axis3_likelihoods.csv ---"
column -s, -t < "data/knowledge_base/axis3_likelihoods.csv" || echo "File is empty or does not exist."