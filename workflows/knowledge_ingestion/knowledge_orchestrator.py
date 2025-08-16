import os
import json
import csv
from pathlib import Path
from groq import Groq
from pydantic import BaseModel, Field, ValidationError
from typing import Literal, Optional, List # Added Optional and List
import textwrap
import pandas as pd
from datetime import datetime
import time
import re
from Bio import Entrez
from dotenv import load_dotenv
import requests # Added requests
from bs4 import BeautifulSoup # Added BeautifulSoup

load_dotenv()

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
        Entrez.email = "info@fneurociencias.org"

    def _initialize_groq_client(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key: raise ValueError("GROQ_API_KEY environment variable not found.")
        return Groq(api_key=api_key)

    def _load_topics(self):
        if not self.topics_path.exists(): raise FileNotFoundError(f"Topic manifest not found at {self.topics_path}")
        return pd.read_csv(self.topics_path)
    
    def _get_summary_for_topic(self, topic_query: str) -> Optional[str]:
        """Simulates calling an evidence API. Maps a topic query to a local summary file."""
        print(f"INFO: [API Simulation] Searching for summary for topic: '{topic_query}'...")
        topic_query_lower = topic_query.lower()
        if "apoe" in topic_query_lower:
            summary_file = Path("data/ingested_knowledge/summaries/genetics_APOE_summary.md")
        elif "nincds-adrda" in topic_query_lower:
            summary_file = Path("data/ingested_knowledge/summaries/criteria_NINCDS_ADRDA_summary.md")
        else:
            summary_file = None
        
        if summary_file and summary_file.exists():
            print(f"INFO: [API Simulation] Found matching summary file: {summary_file.name}")
            return summary_file.read_text(encoding="utf-8")
        
        print(f"WARNING: [API Simulation] No local summary file found for this topic.")
        return None

    def _extract_knowledge(self, text: str, source_info: str) -> List[dict]:
        schema_json = json.dumps(KnowledgeEntry.model_json_schema(), indent=2)
        prompt = self._create_extraction_prompt(text, schema_json)
        extracted_data = []
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                temperature=0.0
            )
            response_content = chat_completion.choices[0].message.content
            
            # Log the raw response content for debugging
            print(f"DEBUG: Raw Groq response for topic '{source_info}':\n{response_content[:500]}...") # Log first 500 chars
            
            # Attempt to parse JSON, if it fails, return empty list
            try:
                # --- Parseo Defensivo con Regex ---
                match = re.search(r'[[.*?]]', response_content, re.DOTALL)
                if not match:
                    print(f"WARNING: No valid JSON array found in the LLM's response. Raw response: {response_content[:500]}...")
                    return []

                json_string = match.group(0) # group(0) coge todo el match
                json_content = json.loads(json_string)
                data_list = next((v for v in json_content.values() if isinstance(v, list)), [])
                for item in data_list:
                    try:
                        item['source_snippet'] = f"PMID:{source_info} | " + item.get('source_snippet', '')
                        validated_item = KnowledgeEntry.model_validate(item)
                        extracted_data.append(validated_item.model_dump())
                    except ValidationError as e: print(f"WARNING: Pydantic validation failed: {e}")
            except json.JSONDecodeError as e:
                print(f"ERROR: JSON decoding failed: {e}. Raw response: {response_content[:500]}...") # Log first 500 chars
                return [] # Return empty list if JSON parsing fails

            return extracted_data
        except Exception as e: print(f"ERROR: Groq extraction or parsing failed: {e}"); return []

    def _append_to_knowledge_base(self, new_entries: List[dict]):
        if not new_entries: return
        headers = ['axis', 'biomarker_name', 'statistic_type', 'value', 'ci_lower', 'ci_upper', 'sample_size', 'cohort_description', 'primary_disease', 'source_snippet']
        entries_by_axis = {1: [], 2: [], 3: []}
        for entry in new_entries:
            axis = int(entry.get('axis', 0))
            if axis in entries_by_axis: entries_by_axis[axis].append(entry)

        for axis, entries in entries_by_axis.items():
            if not entries: continue
            kb_path = self.kb_dir / f"axis{axis}_likelihoods.csv"
            is_new = not kb_path.exists() or os.path.getsize(kb_path) == 0
            with open(kb_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
                if is_new: writer.writeheader()
                for entry in entries:
                    ci = entry.pop('confidence_interval', None)
                    entry['ci_lower'] = ci[0] if ci else ''; entry['ci_upper'] = ci[1] if ci else ''
                    writer.writerow(entry)

    def run(self):
        print(f"--- [AUTONOMOUS KNOWLEDGE ORCHESTRATOR v2.2 - START] ---")
        topics_to_process = self.topics_df[self.topics_df['status'].fillna('pending') == 'pending'].copy()
        if topics_to_process.empty: print("INFO: No pending topics to process."); return

        for index, topic in topics_to_process.iterrows():
            print(f"\nProcessing topic: '{topic['topic_query']}'")
            summary_text = self._get_summary_for_topic(topic['topic_query'])
            if not summary_text:
                self.topics_df.loc[index, 'status'] = 'no_source_found'
                continue
            
            pmid_match = re.search(r"PMID: (\d+)", summary_text)
            pmid = pmid_match.group(1) if pmid_match else "N/A"
            extracted = self._extract_knowledge(summary_text, pmid)
            print(f"INFO: Extracted {len(extracted)} valid entries from PubMed.")
            self._append_to_knowledge_base(extracted)
            
            self.topics_df.loc[index, 'status'] = 'processed'
            self.topics_df.loc[index, 'last_updated'] = datetime.now().strftime('%Y-%m-%d')
            time.sleep(1)

        self.topics_df.to_csv(self.topics_path, index=False)
        print(f"\n--- [AUTONOMOUS KNOWLEDGE ORCHESTRATOR - FINISH] ---")

    def _create_extraction_prompt(self, chunk, schema_json):
        return textwrap.dedent(f"""
            Analyze the following text and extract all relevant biomedical statistics according to the JSON schema. Your response must contain a valid JSON array of objects, starting with '[' and ending with ']'. Do not include any other text, explanations, or markdown.
            JSON SCHEMA: {schema_json}
            TEXT TO ANALYZE:
            ---
            {chunk}
            ---
            """)

if __name__ == "__main__":
    orchestrator = KnowledgeOrchestrator(
        topics_path="data/knowledge_base/topics.csv",
        kb_dir="data/knowledge_base"
    )
    orchestrator.run()