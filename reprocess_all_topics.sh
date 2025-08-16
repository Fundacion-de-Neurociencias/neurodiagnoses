TOPICS_FILE="data/knowledge_base/topics.csv"
ORCHESTRATOR_SCRIPT="workflows/knowledge_ingestion/7_knowledge_orchestrator.py"

# --- PASO 1: Resetear el manifiesto de tópicos para re-procesar todo ---
echo "INFO: Resetting the Topic Manifest to re-process all topics..."
# Reemplaza cualquier estado por 'pending', ignorando la cabecera
sed -i '2,$s/processed/pending/g; 2,$s/no_source_found/pending/g; 2,$s/error/pending/g' "$TOPICS_FILE"
echo "SUCCESS: Topic Manifest has been reset."

# --- PASO 2: Ejecutar el Orquestador Autónomo Definitivo ---
echo "INFO: Executing the final, corrected Autonomous Knowledge Orchestrator..."
python workflows/knowledge_ingestion/knowledge_orchestrator.py

# --- PASO 3: Verificación Final y Completa ---
echo "INFO: Orchestration complete. Verifying the final state of the Knowledge Base..."
echo -e "\n--- Estado Final del Manifiesto de Tópicos ---"
column -s, -t < "$TOPICS_FILE" || echo "Fichero vacío o no generado."
echo -e "\n--- Base de Conocimiento del Eje 1 (Genética) ---"
column -s, -t < "data/knowledge_base/axis1_likelihoods.csv" || echo "Fichero vacío o no generado."
echo -e "\n--- Base de Conocimiento del Eje 2 (Molecular) ---"
column -s, -t < "data/knowledge_base/axis2_likelihoods.csv" || echo "Fichero vacío o no generado."
echo -e "\n--- Base de Conocimiento del Eje 3 (Fenotipo) ---"
column -s, -t < "data/knowledge_base/axis3_likelihoods.csv" || echo "Fichero vacío o no generado."