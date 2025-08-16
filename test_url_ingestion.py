from workflows.knowledge_ingestion.knowledge_orchestrator import KnowledgeOrchestrator, process_external_url
import re # Asegurarnos de que re está importado

# 1. Crea una instancia de nuestro orquestador
my_orchestrator = KnowledgeOrchestrator(
    topics_path="data/knowledge_base/topics.csv",
    kb_dir="data/knowledge_base"
)

# 2. Define un artículo de interés (ejemplo de un meta-análisis sobre APOE4)
test_doi = "10.1001/jama.278.16.1349" 

# 3. Llama a la nueva función de ingesta
status = ingest_from_url(test_doi, my_orchestrator)

# 4. Imprime el resultado
print("\n--- TEST COMPLETE ---")
print(f"Final Status: {status}")
print("Check the contents of 'data/knowledge_base/axis1_likelihoods.csv' to verify.")
