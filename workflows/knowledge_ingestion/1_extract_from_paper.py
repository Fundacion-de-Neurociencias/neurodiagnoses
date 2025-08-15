# -*- coding: utf-8 -*-
"""
Knowledge Ingestion Pipeline: Step 1 - Paper Extraction
(Refactored to use a local LLM via Ollama)
"""
import os
import sys
import argparse
import langextract as lx
import textwrap
import pypdf

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

def get_text_from_pdf(local_path: str) -> str:
    print("Reading PDF content locally...")
    text = ""
    with open(local_path, 'rb') as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "n"
    print(f"Extracted {len(text)} characters from PDF.")
    return text

def run_extraction(source_document: str, output_dir: str):
    print(f"--- Starting extraction from: {source_document} ---")

    document_content = get_text_from_pdf(source_document)

    prompt = textwrap.dedent("""        Extract protein biomarker performance data for neurodegenerative diseases (PD, AD, ALS).
        From tables or text, identify the protein name, the Hazard Ratio (HR) and 95% Confidence Interval (CI),
        the associated p-value, the primary disease, and any mentioned cross-disease associations.
        Ensure extractions are grounded in the exact source text.
        """)
    examples = [
        lx.data.ExampleData(
            text="TPPP2 showed a HR of 0.70 (0.61-0.80) with a p-value of 7.06E-08",
            extractions=[
                lx.data.Extraction(
                    extraction_class="biomarker_finding",
                    extraction_text="TPPP2 showed a HR of 0.70 (0.61-0.80) with a p-value of 7.06E-08",
                    attributes={
                        "protein": "TPPP2", "hazard_ratio": 0.70, "ci_lower": 0.61, "ci_upper": 0.80,
                        "p_value": "7.06E-08", "primary_disease": "PD"
                    }
                )
            ]
        )
    ]

    print("Running LangExtract with local Ollama model... (This may take several minutes)")
    result = lx.extract(
        text_or_documents=document_content,
        prompt_description=prompt,
        examples=examples,
        model_id="llama3:8b-instruct-q4_K_M",  # Use the model we just downloaded
        model_url="http://localhost:11434", # Default Ollama endpoint
        # These flags are often needed for local models
        fence_output=False,
        use_schema_constraints=False
    )

    os.makedirs(output_dir, exist_ok=True)
    source_name = os.path.splitext(os.path.basename(source_document))[0]
    output_basename = f"{output_dir}/{source_name}_extractions"
    jsonl_path = f"{output_basename}.jsonl"
    html_path = f"{output_basename}.html"

    print(f"Saving extracted data to: {jsonl_path}")
    lx.io.save_annotated_documents([result], output_name=jsonl_path, output_dir=".")

    print(f"Generating interactive visualization: {html_path}")
    html_content = lx.visualize(jsonl_path)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"n--- Extraction complete! Review results in {html_path} ---")

def main():
    parser = argparse.ArgumentParser(description="Extract structured knowledge from a scientific paper.")
    parser.add_argument("--url", required=True, help="Local path to the PDF.")
    parser.add_argument("--output_dir", default="data/ingested_knowledge", help="Directory to save results.")
    args = parser.parse_args()
    
    run_extraction(source_document=args.url, output_dir=args.output_dir)

if __name__ == "__main__":
    main()
