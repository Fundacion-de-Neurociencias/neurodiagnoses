import ollama
import json
from pathlib import Path
from dolphin import DocParser

def run_nkc_poc():
    """
    Ejecuta el pipeline completo de la Prueba de Concepto:
    PDF -> Dolphin -> Ollama -> Salida Estructurada.
    """
    pdf_path = Path("tests/poc_nkc/sample_paper_LATE.pdf")
    print(f"--- [INICIO] Procesando el fichero: {pdf_path.name} ---")

    # --- Etapa 1: Procesamiento del PDF con Dolphin ---
    print("n[DOLPHIN] Analizando la estructura del documento...")
    try:
        parser = DocParser()
        # El método parse devuelve un iterador, lo convertimos a una lista
        doc_elements = list(parser.parse(pdf_path))
        
        # Extraemos solo el texto para simplificar el prompt
        doc_text = " ".join([elem.text for elem in doc_elements if hasattr(elem, 'text')])
        
        print(f"[DOLPHIN] Éxito. Se han extraído {len(doc_elements)} elementos del documento.")
        # Mostramos los primeros 500 caracteres para ver el resultado
        print(f"[DOLPHIN] Vista previa del texto: {doc_text[:500]}...")
    except Exception as e:
        print(f"[DOLPHIN] ERROR: Ha fallado el procesamiento del PDF. {e}")
        return

    # --- Etapa 2: Extracción de Conocimiento con Ollama ---
    print("n[OLLAMA] Enviando el texto extraído al LLM local (llama3:8b)...")
    
    prompt = f"""
    You are a biomedical data scientist. Your task is to extract the single most significant finding from the following scientific text regarding the neuropathology of LATE.
    Format the output as a single, valid JSON object. Do not add any explanation.

    ## JSON FORMAT ##
    {{
      "evidence_input": "A_unique_ID_for_this_finding",
      "marker_type": "Primary or Secondary",
      "pathway_affected": "The specific proteinopathy or pathway",
      "interpretation": "A status like 'Positive' or a brief description",
      "primary_disease": "The main disease this finding relates to",
      "source_paper": "LATE_Consensus_Paper_2019"
    }}

    ## TEXT TO ANALYZE ##
    ---
    {doc_text}
    ---
    
    ## EXTRACTED JSON ##
    """

    try:
        response = ollama.chat(
            model='llama3:8b',
            messages=[{'role': 'user', 'content': prompt}],
            format='json'
        )
        
        extracted_json = json.loads(response['message']['content'])
        print("[OLLAMA] Éxito. El LLM ha extraído la siguiente evidencia estructurada:")
        print(json.dumps(extracted_json, indent=2))

    except Exception as e:
        print(f"[OLLAMA] ERROR: Ha fallado la extracción con el LLM. {e}")
        return
        
    print("n--- [FIN] PoC del pipeline NKC completada con éxito. ---")


if __name__ == '__main__':
    # Asegurarse de que el servidor de Ollama esté corriendo
    try:
        ollama.ps()
        print("INFO: El servidor de Ollama está activo.")
    except Exception:
        print("CRITICAL ERROR: No se puede conectar con el servidor de Ollama.")
        print("Asegúrate de haberlo iniciado con el comando: ollama serve")
        exit(1)
        
    run_nkc_poc()

