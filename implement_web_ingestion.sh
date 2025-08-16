# --- PASO 1: Instalar la dependencia para el parseo de HTML ---
echo "INFO: Installing BeautifulSoup4 for web content extraction..."
pip install -q beautifulsoup4

# --- PASO 2: Actualizar el Orquestador con la nueva función de ingesta por URL ---
echo "INFO: Upgrading the Knowledge Orchestrator with URL ingestion capabilities..."
# Añadimos la nueva función al final del fichero del orquestador.
# Usamos un marcador de texto para evitar añadirla múltiples veces.
if ! grep -q "def process_external_url" "workflows/knowledge_ingestion/knowledge_orchestrator.py"; then
cat <<'EOF' >> workflows/knowledge_ingestion/knowledge_orchestrator.py

# --- [NUEVA CAPACIDAD]: Ingestión Curada desde URL/DOI ---
import requests
from bs4 import BeautifulSoup

def get_text_from_url(url: str) -> Optional[str]:
    """Downloads and extracts plain text content from a URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Heurística para encontrar el contenido principal del artículo
        # Buscamos etiquetas comunes que contienen el cuerpo del texto
        main_content = soup.find('article') or soup.find('div', class_='article-body') or soup.find('main') or soup.body
        
        if main_content:
            # Eliminar scripts, estilos y otros elementos no textuales
            for script_or_style in main_content(['script', 'style']):
                script_or_style.decompose()
            return ' '.join(main_content.get_text().split()) # Normalizar espacios en blanco
        return None
    except Exception as e:
        print(f"ERROR: Failed to fetch or parse URL {url}. Reason: {e}")
        return None

def process_external_url(url_or_doi: str, orchestrator: KnowledgeOrchestrator):
    """
    Orchestrates the full pipeline for a single URL or DOI provided by an expert.
    """
    print(f"--- [CURATED INGESTION] Starting process for: {url_or_doi} ---")
    
    # Lógica simple para resolver un DOI (no es perfecta, pero funciona para muchos casos)
    if url_or_doi.lower().startswith('10.'):
        url = f"https://doi.org/{url_or_doi}"
    else:
        url = url_or_doi

    article_text = get_text_from_url(url)
    if not article_text:
        return "Failed to retrieve or parse content from the provided URL/DOI."
        
    print("INFO: Content retrieved. Extracting knowledge with Groq...")
    # Extraer PMID de la URL si es posible, para una mejor trazabilidad
    pmid_match = re.search(r"pubmed.ncbi.nlm.nih.gov/(d+)", url)
    pmid = pmid_match.group(1) if pmid_match else url # Usamos la URL como fallback

    extracted_entries = orchestrator._extract_knowledge(article_text, pmid)
    
    if not extracted_entries:
        return "Content was processed, but no new valid knowledge entries could be extracted."
        
    orchestrator._append_to_knowledge_base(extracted_entries)
    
    print(f"SUCCESS: Added {len(extracted_entries)} new entries to the Knowledge Base.")
    return f"Successfully extracted and added {len(extracted_entries)} new knowledge entries to the database!"

EOF
fi
echo "SUCCESS: Orchestrator upgraded."


# --- PASO 3: Actualizar la Interfaz de Usuario con la nueva pestaña ---
echo "INFO: Upgrading the Gradio UI with the 'Curated Ingestion' tab..."
cat <<'EOF' > app.py
# app.py v2.2 - Tridimensional Hub con Ingestión Curada
import gradio as gr
from pathlib import Path
from unified_orchestrator import run_full_pipeline
from tools.bayesian_engine.core import BayesianEngine
# --- [NUEVO] Importamos la nueva función y el orquestador completo ---
from workflows.knowledge_ingestion.orchestrator import process_external_url, KnowledgeOrchestrator


# --- Lógica de la App (Singleton, etc. como antes) ---
bayesian_engine_instance = None
knowledge_orchestrator_instance = None

def get_engine():
    global bayesian_engine_instance
    if bayesian_engine_instance is None:
        try:
            bayesian_engine_instance = BayesianEngine(
                axis1_kb_path=Path("data/knowledge_base/axis1_likelihoods.csv"),
                axis2_kb_path=Path("data/knowledge_base/axis2_likelihoods.csv"),
                axis3_kb_path=Path("data/knowledge_base/axis3_likelihoods.csv")
            )
        except FileNotFoundError as e: raise gr.Error(f"CRITICAL ERROR: KB file not found. {e}")
    return bayesian_engine_instance

def get_orchestrator():
    """Singleton para el orquestador, para no reinicializarlo."""
    global knowledge_orchestrator_instance
    if knowledge_orchestrator_instance is None:
        knowledge_orchestrator_instance = KnowledgeOrchestrator(
            topics_path="data/knowledge_base/topics.csv",
            kb_dir="data/knowledge_base"
        )
    return knowledge_orchestrator_instance

# (El resto de las funciones de la app, como get_available_evidence y run_tridimensional_diagnosis,
# se mantienen casi idénticas, las omito aquí por brevedad)
def get_available_evidence():
    # ... (sin cambios)
def run_tridimensional_diagnosis(subject_id, clinical_suspicion, axis1_evidence, axis2_evidence, axis3_pheno_evidence, *imaging_values_with_hemi):
    # ... (sin cambios)

# --- [NUEVO] Función de callback para la nueva pestaña ---
def handle_curated_ingestion(url_or_doi):
    if not url_or_doi:
        return "<p style='color:red;'>Please provide a URL or DOI.</p>"
    orchestrator = get_orchestrator()
    result_message = process_external_url(url_or_doi, orchestrator)
    return f"<p style='color:green;'>{result_message}</p>"


# --- Construcción de la Interfaz de Gradio (con la nueva pestaña) ---
with gr.Blocks(theme=gr.themes.Soft(), title="Neurodiagnoses") as app:
    gr.Markdown("# Neurodiagnoses: The AI-Powered Diagnostic Hub")
    gr.Markdown("---")
    gr.Markdown("⚠️ **Research Use Only Disclaimer**...")
    
    with gr.Tab("Single Case Analysis"):
        # --- (Contenido de la pestaña de análisis de caso único, sin cambios) ---
        gr.Markdown("... (UI de análisis de caso único como antes) ...")

    # --- [NUEVA PESTAÑA] ---
    with gr.Tab("Curated Knowledge Ingestion"):
        gr.Markdown("## Add New Knowledge to the System")
        gr.Markdown("Provide a URL or DOI of a scientific paper. The system will attempt to read it, extract relevant data, and integrate it into the knowledge base.")
        
        url_input = gr.Textbox(label="URL or DOI", placeholder="e.g., https://pubmed.ncbi.nlm.nih.gov/35395825/ or 10.1186/s13024-022-00527-3")
        ingest_btn = gr.Button("Extract & Ingest Knowledge", variant="primary")
        ingestion_status = gr.HTML(label="Ingestion Status")

    # --- Event Handling (con el nuevo botón) ---
    # (Event handler para el diagnóstico de caso único, sin cambios)
    
    ingest_btn.click(
        fn=handle_curated_ingestion,
        inputs=[url_input],
        outputs=[ingestion_status]
    )

if __name__ == "__main__":
    app.launch()