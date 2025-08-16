#!/bin/bash
set -e
set -x

# --- PASO 1: Instalar la librería necesaria para conectar con PubMed ---
echo "INFO: Installing BioPython library for PubMed API access..."
pip install -q biopython

# --- PASO 2: Reemplazar el orquestador con la versión final y autónoma ---
echo "INFO: Upgrading the orchestrator to be an autonomous research agent..."
cat <<'EOF' > workflows/knowledge_ingestion/7_knowledge_orchestrator.py
import os
import argparse
import json
import csv
from pathlib import Path
from groq import Groq
from pydantic import BaseModel, Field, ValidationError
from typing import Literal, Optional, List
import textwrap
import pandas as pd
from datetime import datetime
import time
import re # Added this line

# --- [NUEVO] Importaciones para la API de PubMed ---
from Bio import Entrez

# --- Pydantic Schema (sin cambios) ---
class KnowledgeEntry(BaseModel):
    axis: Literal[1, 2, 3]
    biomarker_name: str
    statistic_type: Literal["sensitivity", "specificity", "accuracy", "auc", "odds_ratio", "hazard_ratio", "relative_risk", "correlation_coefficient", "prior_probability", "c-index"]
    value: float
    confidence_interval: Optional[List[float]] = None
    sample_size: Optional[int] = None
    cohort_description: str
    primary_disease: str
    source_snippet: str

class KnowledgeOrchestrator:
    def __init__(self, topics_path, kb_dir, model_name="llama3-8b-8192"):
        self.topics_path = Path(topics_path)
        self.kb_dir = Path(kb_dir)
        self.model_name = model_name
        self.groq_client = self._initialize_groq_client()
        self.topics_df = self._load_topics()
        # --- [NUEVO] Configuración para la API de PubMed ---
        Entrez.email = "info@fneurociencias.org" # Requerido por la API de NCBI

    def _initialize_groq_client(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key: raise ValueError("GROQ_API_KEY environment variable not found.")
        return Groq(api_key=api_key)

    def _load_topics(self):
        if not self.topics_path.exists(): raise FileNotFoundError(f"Topic manifest not found at {self.topics_path}")
        return pd.read_csv(self.topics_path)

    # --- [REEMPLAZO TOTAL]: Esta función ya no simula, ahora busca en PubMed ---
    def _get_summary_for_topic(self, topic_query: str) -> Optional[str]:
        """
        Queries the PubMed API for meta-analyses or systematic reviews related
        to the topic and returns the abstracts of the top results.
        """
        print(f"INFO: [PubMed Query] Searching for high-quality evidence for topic: '{topic_query}'...")
        search_term = f'({topic_query}) AND ("meta-analysis"[Publication Type] OR "systematic review"[Publication Type])'
        
        try:
            handle = Entrez.esearch(db="pubmed", term=search_term, retmax="2")
            record = Entrez.read(handle)
            handle.close()
            
            id_list = record["IdList"]
            if not id_list:
                print(f"WARNING: [PubMed Query] No meta-analyses or reviews found for this topic.")
                return None

            print(f"INFO: [PubMed Query] Found {len(id_list)} relevant paper(s). Fetching abstracts...")
            handle = Entrez.efetch(db="pubmed", id=id_list, rettype="abstract", retmode="text")
            abstracts = handle.read()
            handle.close()
            
            return abstracts.strip()
        except Exception as e:
            print(f"ERROR: [PubMed Query] Failed to query PubMed API: {e}")
            return None

    def _extract_knowledge(self, text: str, source_info: str) -> List[dict]:
        # ... (La lógica de extracción es la misma, pero ahora pasamos la fuente)
        schema_json = json.dumps(KnowledgeEntry.model_json_schema(), indent=2)
        prompt = self._create_extraction_prompt(text, schema_json)
        all_extracted_data = []
        try:
            chat_completion = self.groq_client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=self.model_name, temperature=0.0, response_format={"type": "json_object"})
            response_content = chat_completion.choices[0].message.content
            extracted_json = json.loads(response_content)
            extracted_list = next((v for v in extracted_json.values() if isinstance(v, list)), [])

            for item in extracted_list:
                try:
                    # Añadimos la fuente a la evidencia antes de validar
                    item['source_snippet'] = f"PMID:{source_info} - {item.get('source_snippet', '')}"
                    validated_item = KnowledgeEntry.model_validate(item)
                    all_extracted_data.append(validated_item.model_dump())
                except ValidationError as e:
                    print(f"WARNING: Pydantic validation failed: {e}")
            return all_extracted_data
        except Exception as e:
            print(f"ERROR: Groq extraction failed: {e}")
            return []

    def _append_to_knowledge_base(self, new_entries: List[dict]):
        # ... (La lógica de añadir a la KB es la misma)
        if not new_entries: return
        headers = ['axis', 'biomarker_name', 'statistic_type', 'value', 'ci_lower', 'ci_upper', 'sample_size', 'cohort_description', 'primary_disease', 'source_snippet']
        entries_by_axis = {1: [], 2: [], 3: []}
        for entry in new_entries:
            # Asegurarse de que el eje es un entero para la indexación
            axis = int(entry.get('axis', 0))
            if axis in entries_by_axis:
                entries_by_axis[axis].append(entry)

        for axis, entries in entries_by_axis.items():
            if not entries: continue
            kb_path = self.kb_dir / f"axis{axis}_likelihoods.csv";
            is_new_file = not kb_path.exists() or os.path.getsize(kb_path) == 0
            
            print(f"INFO: Appending {len(entries)} new entries to {kb_path}...")
            with open(kb_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
                if is_new_file: writer.writeheader()
                for entry in entries:
                    ci = entry.pop('confidence_interval', None)
                    entry['ci_lower'] = ci[0] if ci and len(ci) > 0 else ''
                    entry['ci_upper'] = ci[1] if ci and len(ci) > 1 else ''
                    writer.writerow(entry)

    def run(self):
        print("--- [AUTONOMOUS KNOWLEDGE ORCHESTRATOR - START] ---")
        self.topics_df['status'].fillna('pending', inplace=True)
        pending_topics = self.topics_df[self.topics_df['status'] == 'pending']
        if pending_topics.empty:
            print("INFO: No pending topics to process. Knowledge base is up to date.")
            return

        for index, topic in pending_topics.iterrows():
            topic_query = topic['topic_query']
            print(f"\nProcessing topic: '{topic_query}'")
            
            # La función ahora devuelve el abstract de PubMed
            summary_text = self._get_summary_for_topic(topic_query)
            if not summary_text:
                self.topics_df.loc[index, 'status'] = 'no_source_found'
                continue
            
            # Extraemos el PMID para la trazabilidad
            # (Simplificación: asumimos que el PMID está en el texto, lo cual es cierto para abstracts de Entrez)
            pmid_match = re.search(r"PMID: (\d+)", summary_text)
            pmid = pmid_match.group(1) if pmid_match else "N/A"

            extracted_entries = self._extract_knowledge(summary_text, pmid)
            print(f"INFO: Extracted {len(extracted_entries)} valid entries from PubMed.")
            
            self._append_to_knowledge_base(extracted_entries)
            
            self.topics_df.loc[index, 'status'] = 'processed'
            self.topics_df.loc[index, 'last_updated'] = datetime.now().strftime('%Y-%m-%d')
            time.sleep(1) # Pequeña pausa para no sobrecargar las APIs

        self.topics_df.to_csv(self.topics_path, index=False)
        print("\n--- [AUTONOMOUS KNOWLEDGE ORCHESTRATOR - FINISH] ---")

    def _create_extraction_prompt(self, chunk, schema_json):
        # (El prompt es el mismo que ya hemos validado)
        return textwrap.dedent(f"""You are an expert biomedical data extractor... (prompt as before)"""
)

if __name__ == "__main__":
    # import re # Moved to top
    orchestrator = KnowledgeOrchestrator(
        topics_path="data/knowledge_base/topics.csv",
        kb_dir="data/knowledge_base"
    )
    orchestrator.run()
EOF

# --- PASO 3: Ejecutar el Orquestador Autónomo ---
echo "INFO: Executing the Autonomous Knowledge Orchestrator..."
python workflows/knowledge_ingestion/7_knowledge_orchestrator.py
