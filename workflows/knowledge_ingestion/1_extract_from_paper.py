# -*- coding: utf-8 -*-
"""
Knowledge Ingestion Pipeline: Step 1 - Paper Extraction

This script uses the 'langextract' library to perform a structured extraction
of biomarker performance data from a given scientific paper (text or URL).
(Updated with a specialized prompt for proteomics papers)
"""

import os
import sys
import argparse
import langextract as lx
import textwrap
import time
import requests
import io
from pypdf import PdfReader

# Add project root to path for cross-module imports
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

def get_pdf_text(url: str) -> str:
    """Downloads a PDF from a URL and extracts its text content."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        pdf_file = io.BytesIO(response.content)
        reader = PdfReader(pdf_file)
        text = "".join(page.extract_text() for page in reader.pages)
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        sys.exit(1)

def run_extraction(source_document_url: str, output_dir: str):
    """
    Configures and runs the LangExtract pipeline on a scientific paper.
    """
    print(f"--- Starting extraction from: {source_document_url} ---")

    # 1. Define a more specific and robust extraction task
    prompt = textwrap.dedent("""
        Extract protein biomarker performance data for neurodegenerative diseases (PD, AD, ALS).
        From tables or text, identify the protein name, the Hazard Ratio (HR) and 95% Confidence Interval (CI),
        the associated p-value, the primary disease, and any mentioned cross-disease associations.
        Ensure extractions are grounded in the exact source text.
        """)

    # 2. Provide high-quality few-shot examples that match the target paper's format
    examples = [
        lx.data.ExampleData(
            text="TPPP2 showed a HR of 0.70 (0.61-0.80) with a p-value of 7.06E-08 and strong replication.",
            extractions=[
                lx.data.Extraction(
                    extraction_class="biomarker_finding",
                    extraction_text="TPPP2 showed a HR of 0.70 (0.61-0.80) with a p-value of 7.06E-08",
                    attributes={
                        "protein": "TPPP2",
                        "hazard_ratio": 0.70,
                        "ci_lower": 0.61,
                        "ci_upper": 0.80,
                        "p_value": "7.06E-08",
                        "primary_disease": "PD"
                    }
                )
            ]
        ),
        lx.data.ExampleData(
            text="RSPO2 was associated with a HR of 1.19 (1.10-1.29) for PD, and showed overlap with AD and ALS.",
            extractions=[
                 lx.data.Extraction(
                    extraction_class="biomarker_finding",
                    extraction_text="RSPO2 was associated with a HR of 1.19 (1.10-1.29) for PD, and showed overlap with AD and ALS",
                    attributes={
                        "protein": "RSPO2",
                        "hazard_ratio": 1.19,
                        "ci_lower": 1.10,
                        "ci_upper": 1.29,
                        "primary_disease": "PD",
                        "cross_disease_association": "AD, ALS"
                    }
                )
            ]
        )
    ]

    # 3. Download and chunk the document
    print("Downloading and extracting text from PDF...")
    full_text = get_pdf_text(source_document_url)
    chunk_size = 10000  # characters
    chunks = [full_text[i:i + chunk_size] for i in range(0, len(full_text), chunk_size)]
    print(f"Document split into {len(chunks)} chunks.")

    # 4. Run the extraction process in chunks to avoid rate limiting
    all_annotations = []
    print("Running LangExtract on chunks... (This may take several minutes)")
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        result = lx.extract(
            text_or_documents=chunk,
            prompt_description=prompt,
            examples=examples,
            model_id="gemini-1.5-flash-latest",
            extraction_passes=1, # Single pass per chunk
        )
        print(f"Type of result: {type(result)}")
        print(f"Result object: {result}")
        print(dir(result))
        if result and hasattr(result, 'annotations') and result.annotations:
            all_annotations.extend(result.annotations)
        print(f"Chunk {i+1} processed. Waiting 1 second...")
        time.sleep(1) # Wait to avoid rate limiting

    # 5. Combine results and save
    final_result = lx.data.AnnotatedDocument(text=full_text, annotations=all_annotations)
    os.makedirs(output_dir, exist_ok=True)
    source_name = os.path.splitext(os.path.basename(source_document_url))[0]
    output_basename = f"{output_dir}/{source_name}_extractions"

    jsonl_path = f"{output_basename}.jsonl"
    html_path = f"{output_basename}.html"

    print(f"Saving extracted data to: {jsonl_path}")
    lx.io.save_annotated_documents([final_result], output_name=jsonl_path, output_dir=".")

    print(f"Generating interactive visualization: {html_path}")
    html_content = lx.visualize(jsonl_path)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("\n--- Extraction complete! ---")
    print(f"Review the results by opening the HTML file in a browser: {html_path}")


def main():
    parser = argparse.ArgumentParser(description="Extract biomarker data from a scientific paper using LangExtract.")
    parser.add_argument("--url", required=True, help="URL or local path to the full text/PDF of the scientific paper.")
    parser.add_argument("--output_dir", default="data/ingested_knowledge", help="Directory to save the extracted results.")
    args = parser.parse_args()
    
    run_extraction(source_document_url=args.url, output_dir=args.output_dir)

if __name__ == "__main__":
    main()