import sys
from pathlib import Path
import pprint
import os

# Añadimos los directorios necesarios al path para las importaciones
sys.path.append(str(Path(__file__).parent.parent.absolute()))
sys.path.append(str(Path(__file__).parent.parent.absolute() / "neurodiagnoses-engine"))

from workflows.knowledge_ingestion.knowledge_orchestrator import KnowledgeOrchestrator

def run_test():
    """
    Verifica que el Orquestador v2.0 y su función de procesamiento de URL
    se pueden instanciar y llamar correctamente.
    """
    print("--- [INICIO] Prueba del Orquestador de Conocimiento v2.0 ---")

    # Simulamos la presencia de una clave de API para que el constructor no falle
    os.environ["GOOGLE_API_KEY"] = "SIMULATED_KEY_FOR_TESTING"
    
    # 1. Instanciar el orquestador
    orchestrator = KnowledgeOrchestrator(
        topics_path=Path("neurodiagnoses-engine/data/knowledge_base/topics.csv"),
        kb_dir=Path("neurodiagnoses-engine/data/knowledge_base")
    )
        
    # 2. Definir una URL y un esquema de prueba
    test_url = "https://doi.org/10.1038/s41588-024-01939-9"
    test_schema = { "type": "object", "properties": { "factor": {"type": "string"}, "description": {"type": "string"} } }
    
    print(f"n--- Probando la extracción desde: {test_url} ---")
    
    # 3. Ejecutar la función de procesamiento de URL (que contiene la llamada simulada)
    extracted_data = orchestrator.process_url_with_gemini(
        url=test_url,
        schema=test_schema
    )
    
    # 4. Imprimir y verificar el resultado simulado
    print("n--- [RESULTADO DE LA EXTRACCIÓN SIMULADA] ---")
    pprint.pprint(extracted_data)
    
    assert isinstance(extracted_data, list)
    assert len(extracted_data) > 0
    assert "factor" in extracted_data[0]
    print("n--- [VERIFICACIÓN OK] ---")

    print("n--- [FIN] Prueba del Orquestador v2.0 completada con éxito. ---")
    
    # Limpiamos la variable de entorno simulada
    del os.environ["GOOGLE_API_KEY"]

if __name__ == "__main__":
    run_test()
