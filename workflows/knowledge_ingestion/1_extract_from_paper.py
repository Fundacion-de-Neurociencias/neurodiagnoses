# -*- coding: utf-8 -*-
"""
Knowledge Ingestion Pipeline: Step 1 - Paper Extraction

This script uses the 'langextract' library to perform a structured extraction
of biomarker performance data from a given scientific paper (text or URL).
"""

import os
import sys
import argparse
import langextract as lx
import textwrap

# Add project root to path for cross-module imports
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

def run_extraction(source_document_url: str, output_dir: str):
    """
    Configures and runs the LangExtract pipeline on a scientific paper.
    """
    print(f"--- Starting extraction from: {source_document_url} ---")

    # 1. Define the extraction task with a clear prompt
    prompt = textwrap.dedent("""
        Extract biomarker performance metrics for neurodegenerative diseases.
        Focus on sensitivity, specificity, AUC, hazard ratio (HR), cutoff values,
        the biomarker name, the target disease, and the sample type (CSF or plasma).
        Ensure extractions are grounded in the exact source text.
        """)

    # 2. Provide high-quality few-shot examples to guide the LLM
    examples = [
        lx.data.ExampleData(
            text="The pTau181/Abeta42 ratio in CSF showed an AUC of 0.92 for distinguishing AD from controls.",
            extractions=[
                lx.data.Extraction(
                    extraction_class="biomarker_performance",
                    extraction_text="pTau181/Abeta42 ratio in CSF showed an AUC of 0.92 for distinguishing AD",
                    attributes={
                        "biomarker_name": "pTau181/Abeta42 ratio",
                        "sample_type": "CSF",
                        "metric": "AUC",
                        "value": 0.92,
                        "disease": "AD"
                    }
                )
            ]
        ),
        lx.data.ExampleData(
            text="For DLB, 59% were positive for the pTau/Abeta42+ profile, compared to 26% of controls.",
            extractions=[
                 lx.data.Extraction(
                    extraction_class="biomarker_performance",
                    extraction_text="DLB, 59% were positive for the pTau/Abeta42+ profile",
                    attributes={
                        "biomarker_name": "pTau/Abeta42+ profile",
                        "metric": "sensitivity", # Approximate sensitivity
                        "value": 0.59,
                        "disease": "DLB"
                    }
                )
            ]
        )
    ]

    # 3. Run the extraction process
    # Note: Requires a configured API key for Gemini/Vertex AI. See LangExtract docs.
    print("Running LangExtract... (This may take several minutes for a full paper)")
    result = lx.extract(
        text_or_documents=source_document_url,
        prompt_description=prompt,
        examples=examples,
        model_id="gemini-1.5-flash-001", # A good default model
        extraction_passes=2,    # Improves recall
        max_workers=10,         # Parallel processing
    )

    # 4. Save and visualize the results
    os.makedirs(output_dir, exist_ok=True)
    source_name = os.path.basename(source_document_url).split('.')[0]
    output_basename = f"{output_dir}/{source_name}_extractions"

    jsonl_path = f"{output_basename}.jsonl"
    html_path = f"{output_basename}.html"

    print(f"Saving extracted data to: {jsonl_path}")
    lx.io.save_annotated_documents([result], output_name=jsonl_path, output_dir=".")

    print(f"Generating interactive visualization: {html_path}")
    html_content = lx.visualize(jsonl_path)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("\n--- Extraction complete! ---")
    print(f"Review the results by opening the HTML file: {html_path}")


def main():
    parser = argparse.ArgumentParser(description="Extract biomarker data from a scientific paper using LangExtract.")
    parser.add_argument("--url", required=True, help="URL to the full text of the scientific paper.")
    parser.add_argument("--output_dir", default="data/ingested_knowledge", help="Directory to save the extracted results.")
    args = parser.parse_args()
    
    run_extraction(source_document_url=args.url, output_dir=args.output_dir)

if __name__ == "__main__":
    main()
