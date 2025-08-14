# -*- coding: utf-8 -*-
"""
Knowledge Ingestion Pipeline: Step 1 - Paper Extraction
(Refactored to read local PDFs before extraction)
"""
import os
import sys
import argparse
import langextract as lx
import textwrap
import pypdf  # Import the new PDF reading library

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

def get_text_from_pdf(local_path: str) -> str:
    """Reads a local PDF file and extracts its text content."""
    print("Reading PDF content locally...")
    text = ""
    with open(local_path, 'rb') as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    print(f"Extracted {len(text)} characters from PDF.")
    return text

def run_extraction(source_document: str, output_dir: str):
    """
    Configures and runs the LangExtract pipeline on a scientific paper.
    """
    print(f"--- Starting extraction from: {source_document} ---")

    # Determine if the source is a URL or a local file
    if source_document.startswith(('http://', 'https://')):
        document_content = source_document
    elif os.path.exists(source_document):
        document_content = get_text_from_pdf(source_document)
    else:
        raise FileNotFoundError(f"The specified file was not found: {source_document}")

    # 1. Define the extraction task with a clear prompt
    prompt = textwrap.dedent("""\
        Extract protein biomarker performance data for neurodegenerative diseases (PD, AD, ALS).
        From tables or text, identify the protein name, the Hazard Ratio (HR) and 95% Confidence Interval (CI),
        the associated p-value, the primary disease, and any mentioned cross-disease associations.
        Ensure extractions are grounded in the exact source text.
        """)

    # 2. Provide high-quality few-shot examples
    examples = [
        lx.data.ExampleData(
            text="TPPP2 showed a HR of 0.70 (0.61-0.80) with a p-value of 7.06E-08 and strong replication.",
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

    # 3. Run the extraction process on the document content
    print("Running LangExtract... (This may take several minutes)")
    result = lx.extract(
        text_or_documents=document_content,
        prompt_description=prompt,
        examples=examples,
        model_id="gemini-pro",
        extraction_passes=2,
        max_workers=10,
    )

    # 4. Save and visualize the results
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
    
    print("\n--- Extraction complete! ---")
    print(f"Review the results by opening the HTML file in a browser: {html_path}")


def main():
    parser = argparse.ArgumentParser(description="Extract biomarker data from a scientific paper using LangExtract.")
    parser.add_argument("--url", required=True, help="URL or local path to the full text/PDF of the scientific paper.")
    parser.add_argument("--output_dir", default="data/ingested_knowledge", help="Directory to save the extracted results.")
    args = parser.parse_args()
    
    run_extraction(source_document=args.url, output_dir=args.output_dir)

if __name__ == "__main__":
    main()
