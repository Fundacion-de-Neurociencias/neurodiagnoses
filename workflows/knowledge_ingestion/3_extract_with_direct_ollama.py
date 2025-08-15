import argparse
import json
from pathlib import Path
import ollama
from pydantic import BaseModel, Field, ValidationError
from typing import Literal, Optional, List
import textwrap

# --- Pydantic Schema ---
# Defines the structure of the data we want to extract.
class KnowledgeEntry(BaseModel):
    axis: Literal[1, 2, 3] = Field(..., description="The evidence axis: 1 (Etiology/Genetic), 2 (Molecular Profile), or 3 (Phenotypic Profile).")
    biomarker_name: str = Field(..., description="The specific name of the biomarker, gene, or clinical metric (e.g., 'CSF p-tau181', 'APOE4', 'MMSE Score').")
    statistic_type: Literal[
        "sensitivity", "specificity", "accuracy", "auc",
        "odds_ratio", "hazard_ratio", "relative_risk",
        "correlation_coefficient", "prior_probability"
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
    You are an expert biomedical data extractor. Your task is to analyze the following text chunk from a scientific paper and extract structured information based on the provided JSON schema.

    RULES:
    1. Extract ALL matching entities from the text.
    2. Adhere strictly to the JSON schema provided.
    3. The `source_snippet` field must be the EXACT, UNMODIFIED text from the paper that justifies the extraction.
    4. If no relevant information is found in the chunk, return an empty JSON array: [].
    5. Your entire response must be a single, valid JSON array of objects, and nothing else. Do not include any explanations or introductory text.

    JSON SCHEMA:
    ```json
    {schema_json}
    ```

    TEXT CHUNK TO ANALYZE:
    ---
    {chunk}
    ---

    Respond with the JSON array now.
    """)

def main():
    parser = argparse.ArgumentParser(description="Extract structured knowledge directly using Ollama.")
    parser.add_argument("--input-md", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model-name", type=str, default="tinyllama")
    parser.add_argument("--chunk-size", type=int, default=4000)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_jsonl_path = args.output_dir / f"{args.input_md.stem}.jsonl"
    document_text = args.input_md.read_text(encoding='utf-8')
    
    schema_json = json.dumps(KnowledgeEntry.model_json_schema(), indent=2)
    all_extracted_data = []

    text_chunks = [document_text[i:i + args.chunk_size] for i in range(0, len(document_text), args.chunk_size)]

    for i, chunk in enumerate(text_chunks):
        print(f"INFO: Processing chunk {i+1}/{len(text_chunks)}...")
        prompt = create_extraction_prompt(chunk, schema_json)
        
        try:
            response = ollama.chat(
                model=args.model_name,
                messages=[{'role': 'user', 'content': prompt}],
                format='json',
                options={'temperature': 0.0}
            )
            
            response_content = response['message']['content']
            extracted_chunk_data = json.loads(response_content)
            
            # Validate each extracted object with Pydantic
            for item in extracted_chunk_data:
                try:
                    KnowledgeEntry.model_validate(item)
                    all_extracted_data.append(item)
                except ValidationError as e:
                    print(f"WARNING: Pydantic validation failed for an item in chunk {i+1}: {e}")

            print(f"INFO: Successfully extracted and validated {len(extracted_chunk_data)} items from chunk {i+1}.")

        except json.JSONDecodeError:
            print(f"WARNING: LLM output for chunk {i+1} was not valid JSON. Skipping.")
        except Exception as e:
            print(f"ERROR: An unexpected error occurred on chunk {i+1}: {e}")

    print(f"\nINFO: Total of {len(all_extracted_data)} knowledge entries extracted from the document.")

    if all_extracted_data:
        with open(output_jsonl_path, 'w', encoding='utf-8') as f:
            for item in all_extracted_data:
                f.write(json.dumps(item) + '\n')
        print(f"SUCCESS: Knowledge base file created at {output_jsonl_path}")

if __name__ == "__main__":
    main()
