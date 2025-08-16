import os
import argparse
import json
from pathlib import Path
from groq import Groq
from pydantic import BaseModel, Field, ValidationError
from typing import Literal, Optional, List
import textwrap

# --- Pydantic Schema (la mantenemos, es perfecta) ---
class KnowledgeEntry(BaseModel):
    axis: Literal[1, 2, 3] = Field(..., description="The evidence axis: 1 (Etiology/Genetic), 2 (Molecular Profile), or 3 (Phenotypic Profile).")
    biomarker_name: str = Field(..., description="The specific name of the biomarker, gene, or clinical metric (e.g., 'CSF p-tau181', 'APOE4', 'MMSE Score').")
    statistic_type: Literal[
        "sensitivity", "specificity", "accuracy", "auc",
        "odds_ratio", "hazard_ratio", "relative_risk",
        "correlation_coefficient", "prior_probability", "c-index", "c-index"
    ] = Field(..., description="The type of statistical measure reported.")
    value: float = Field(..., description="The numerical point estimate of the statistic.")
    confidence_interval: Optional[List[float]] = Field(None, description="The lower and upper bounds of the 95% confidence interval. Example: [0.81, 0.89]")
    sample_size: Optional[int] = Field(None, description="The total sample size (n) used to calculate the statistic.")
    cohort_description: str = Field(..., description="A brief description of the cohort used for the measurement (e.g., 'AD vs Healthy Controls', 'FTD patients').")
    primary_disease: str = Field(..., description="The main neurodegenerative disease being studied (e.g., 'Alzheimer\'s Disease', 'Parkinson\'s Disease', 'FTD').")
    source_snippet: str = Field(..., description="The exact text snippet from the paper that contains and supports this extracted data.")

def create_extraction_prompt(chunk, schema_json):
    """Creates a detailed prompt for the LLM."""
    return textwrap.dedent(f"""
    You are an expert biomedical data extractor. Your task is to analyze the following text chunk and extract structured information based on the provided JSON schema.
    RULES:
    1. Your entire response MUST be a single, valid JSON array of objects.
    2. Adhere strictly to the JSON schema.
    3. The `source_snippet` field must be the EXACT text from the paper that justifies the extraction.
    4. If no relevant information is found, return an empty JSON array: [].
    5. Do not include markdown fences (```json), explanations, or any text outside of the JSON array.
    6. Ensure the output is a single root-level JSON array, not a JSON object containing an array. For example: [ {{"key": "value"}} ], NOT {{"data": [ {{"key": "value"}} ] }}.

    JSON SCHEMA: {schema_json}

    TEXT CHUNK TO ANALYZE:
    ---
    {chunk}
    ---
    """)

def main():
    parser = argparse.ArgumentParser(description="Extract structured knowledge using the Groq API.")
    parser.add_argument("--input-md", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model-name", type=str, default="llama3-8b-8192")
    args = parser.parse_args()

    # --- INICIALIZACIÓN DEL CLIENTE DE GROQ ---
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY environment variable not found.")
        print("Please set the secret in your Codespace and reload the window.")
        return
    client = Groq(api_key=api_key)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_jsonl_path = args.output_dir / f"{args.input_md.stem}.jsonl"
    document_text = args.input_md.read_text(encoding='utf-8')
    
    schema_json = json.dumps(KnowledgeEntry.model_json_schema(), indent=2)
    all_extracted_data = []

    print(f"INFO: Processing document with Groq and model {args.model_name}...")
    prompt = create_extraction_prompt(document_text, schema_json)
        
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=args.model_name,
            temperature=0.0,
            response_format={"type": "json_object"},
        )
        
        response_content = chat_completion.choices[0].message.content
        extracted_chunk_data = json.loads(response_content)

        if isinstance(extracted_chunk_data, dict):
            for key, value in extracted_chunk_data.items():
                if isinstance(value, list):
                    extracted_chunk_data = value
                    break

        for item in extracted_chunk_data:
            try:
                KnowledgeEntry.model_validate(item)
                all_extracted_data.append(item)
            except ValidationError as e:
                print(f"WARNING: Pydantic validation failed for an item: {e}")

        print(f"INFO: Successfully extracted and validated {len(all_extracted_data)} items.")

    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")

    if all_extracted_data:
        with open(output_jsonl_path, 'w', encoding='utf-8') as f:
            for item in all_extracted_data:
                f.write(json.dumps(item) + '\n')
        print(f"SUCCESS: Knowledge base file created at {output_jsonl_path}")

if __name__ == "__main__":
    main()
