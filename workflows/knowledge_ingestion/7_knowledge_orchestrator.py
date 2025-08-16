import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file
from dotenv import load_dotenv

load_dotenv()
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

# --- Pydantic Schema ---
class KnowledgeEntry(BaseModel):
    axis: Literal[1, 2, 3] = Field(..., description="The evidence axis: 1 (Etiology/Genetic), 2 (Molecular Profile), or 3 (Phenotypic Profile).")
    biomarker_name: str = Field(..., description="The specific name of the biomarker, gene, or clinical metric.")
    statistic_type: Literal[
        "sensitivity", "specificity", "accuracy", "auc",
        "odds_ratio", "hazard_ratio", "relative_risk",
        "correlation_coefficient", "prior_probability", "c-index"
    ] = Field(..., description="The type of statistical measure reported.")
    value: float = Field(..., description="The numerical point estimate of the statistic.")
    confidence_interval: Optional[List[float]] = Field(None, description="The lower and upper bounds of the 95% confidence interval.")
    sample_size: Optional[int] = Field(None, description="The total sample size (n) used to calculate the statistic.")
    cohort_description: str = Field(..., description="A brief description of the cohort used.")
    primary_disease: str = Field(..., description="The main neurodegenerative disease being studied.")
    source_snippet: str = Field(..., description="The exact text snippet from the paper that contains this data.")

class KnowledgeOrchestrator:
    def __init__(self, topics_path, summaries_dir, kb_dir, model_name="llama3-8b-8192"):
        self.topics_path = Path(topics_path)
        self.summaries_dir = Path(summaries_dir)
        self.kb_dir = Path(kb_dir)
        self.model_name = model_name
        self.groq_client = self._initialize_groq_client()
        self.topics_df = self._load_topics()

    def _initialize_groq_client(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not found.")
        return Groq(api_key=api_key)

    def _load_topics(self):
        if not self.topics_path.exists():
            raise FileNotFoundError(f"Topic manifest not found at {self.topics_path}")
        return pd.read_csv(self.topics_path)

    def _get_summary_for_topic(self, topic_query: str) -> Optional[str]:
        """
        Simulates calling an evidence API. For this PoC, it looks for a
        local markdown file named after a simplified version of the topic query.
        """
        # Simplistic mapping for this PoC
        if "blood biomarkers for Alzheimer's" in topic_query:
            summary_file = self.summaries_dir / "open_evidence_biomarkers.md"
            if summary_file.exists():
                print(f"INFO: [API Simulation] Found local summary for topic: '{topic_query}'")
                return summary_file.read_text(encoding='utf-8')
        print(f"WARNING: [API Simulation] No local summary found for topic: '{topic_query}'")
        return None

    def _extract_knowledge(self, text: str) -> List[dict]:
        """Uses Groq to extract structured knowledge from text."""
        schema_json = json.dumps(KnowledgeEntry.model_json_schema(), indent=2)
        prompt = self._create_extraction_prompt(text, schema_json)
        all_extracted_data = []
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                temperature=0.0,
                response_format={"type": "json_object"},
            )
            response_content = chat_completion.choices[0].message.content
            extracted_json = json.loads(response_content)
            
            # Find the list within the JSON object
            extracted_list = next((v for v in extracted_json.values() if isinstance(v, list)), [])

            for item in extracted_list:
                try:
                    validated_item = KnowledgeEntry.model_validate(item)
                    all_extracted_data.append(validated_item.model_dump())
                except ValidationError as e:
                    print(f"WARNING: Pydantic validation failed for an item: {e}")
            return all_extracted_data
        except Exception as e:
            print(f"ERROR: Groq extraction failed: {e}")
            return []
            
    def _append_to_knowledge_base(self, new_entries: List[dict]):
        """Appends new, validated entries to the corresponding axis CSV files."""
        if not new_entries:
            return
            
        headers = ['axis', 'biomarker_name', 'statistic_type', 'value', 'ci_lower', 'ci_upper', 'sample_size', 'cohort_description', 'primary_disease', 'source_snippet']
        
        # Group entries by axis
        entries_by_axis = {1: [], 2: [], 3: []}
        for entry in new_entries:
            entries_by_axis[entry['axis']].append(entry)

        for axis, entries in entries_by_axis.items():
            if not entries: continue
            
            kb_path = self.kb_dir / f"axis{axis}_likelihoods.csv"
            is_new_file = not kb_path.exists()
            
            print(f"INFO: Appending {len(entries)} new entries to {kb_path}...")
            with open(kb_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                if is_new_file:
                    writer.writeheader()
                for entry in entries:
                    # Flatten the CI for CSV
                    ci = entry.pop('confidence_interval', None)
                    entry['ci_lower'] = ci[0] if ci and len(ci) > 0 else ''
                    entry['ci_upper'] = ci[1] if ci and len(ci) > 1 else ''
                    writer.writerow(entry)

    def run(self):
        """Main execution loop for the orchestrator."""
        print("--- [KNOWLEDGE BASE ORCHESTRATOR - START] ---")
        
        pending_topics = self.topics_df[self.topics_df['status'] == 'pending']
        if pending_topics.empty:
            print("INFO: No pending topics to process. Knowledge base is up to date.")
            return

        for index, topic in pending_topics.iterrows():
            topic_query = topic['topic_query']
            print(f"nProcessing topic: '{topic_query}'")
            
            summary_text = self._get_summary_for_topic(topic_query)
            if not summary_text:
                continue

            extracted_entries = self._extract_knowledge(summary_text)
            print(f"INFO: Extracted {len(extracted_entries)} valid entries.")
            
            self._append_to_knowledge_base(extracted_entries)
            
            # Update status in the dataframe
            self.topics_df.loc[index, 'status'] = 'processed'
            self.topics_df.loc[index, 'last_updated'] = datetime.now().strftime('%Y-%m-%d')

        # Save the updated topics manifest
        self.topics_df.to_csv(self.topics_path, index=False)
        print("n--- [KNOWLEDGE BASE ORCHESTRATOR - FINISH] ---")
        print("SUCCESS: Topic manifest and knowledge base have been updated.")

    def _create_extraction_prompt(self, chunk, schema_json):
        # (Re-added this helper method for clarity)
        return textwrap.dedent(f"""
        You are an expert biomedical data extractor. Your task is to analyze the following text chunk and extract structured information based on the provided JSON schema.
        RULES:
        1. Your entire response MUST be a single, valid JSON object containing one key, whose value is a JSON array of objects. Example: {{"data": [...]}}
        2. Adhere strictly to the JSON schema for the objects in the array.
        3. The `source_snippet` field must be the EXACT text that justifies the extraction.
        4. If no relevant information is found, return an empty array: {{"data": []}}.
        5. Do not include markdown fences (```json) or any text outside the main JSON object.

        JSON SCHEMA FOR ARRAY OBJECTS: {schema_json}
        TEXT CHUNK TO ANALYZE: --- {chunk} ---
        """)

if __name__ == "__main__":
    orchestrator = KnowledgeOrchestrator(
        topics_path="data/knowledge_base/topics.csv",
        summaries_dir="data/ingested_knowledge/summaries",
        kb_dir="data/knowledge_base"
    )
    orchestrator.run()