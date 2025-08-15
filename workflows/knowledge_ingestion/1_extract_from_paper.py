# -*- coding: utf-8 -*-
"""
Knowledge Ingestion Pipeline: Step 1 - Paper Extraction
(Upgraded for the full Tridimensional Knowledge Schema)
"""

import os
import sys
import argparse
import langextract as lx
import textwrap
import pypdf

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

def get_text_from_pdf(local_path: str) -> str:
    """Reads a local PDF file and extracts its text content."""
    print("Reading PDF content locally...")
    text = ""
    with open(local_path, 'rb') as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "n"
    print(f"Extracted {len(text)} characters from PDF.")
    return text

def run_extraction(source_document: str, output_dir: str):
    """
    Configures and runs the LangExtract pipeline on a scientific paper.
    """
    print(f"--- Starting extraction from: {source_document} ---")

    if source_document.startswith(('http://', 'https://')):
        document_content = source_document
    elif os.path.exists(source_document):
        document_content = get_text_from_pdf(source_document)
    else:
        raise FileNotFoundError(f"The specified file was not found: {source_document}")

    # 1. Define the comprehensive extraction task based on our agreed schema
    prompt = textwrap.dedent("""        You are an expert biomedical data extractor. From the provided scientific paper,
        extract all evidence related to the diagnosis of neurodegenerative diseases (AD, PD, DLB, FTD).
        For each piece of evidence, extract all available metadata and performance metrics.
        Follow the schema provided in the examples precisely.
        """)

    # 2. Provide rich few-shot examples covering all three axes
    examples = [
        lx.data.ExampleData(
            text="For the APOE4 single allele, the odds ratio for AD was 3.7 (95% CI: 3.2-4.1) in the ADNI cohort.",
            extractions=[
                lx.data.Extraction(
                    extraction_class="knowledge_entry",
                    extraction_text="APOE4 single allele, the odds ratio for AD was 3.7 (95% CI: 3.2-4.1) in the ADNI cohort",
                    attributes={
                        "evidence_type": "genetic_marker",
                        "marker_name": "APOE4_1_allele",
                        "target_disease": "AD",
                        "metric_type": "Odds Ratio",
                        "metric_value": 3.7,
                        "metric_ci_lower": 3.2,
                        "metric_ci_upper": 4.1,
                        "cohort_name": "ADNI"
                    }
                )
            ]
        ),
        lx.data.ExampleData(
            text="The pTau/Abeta42 ratio (>0.023) in CSF identified AD with a sensitivity of 85% (CI: 81-89%) and specificity of 70% (CI: 65-75%) using Roche Elecsys.",
            extractions=[
                 lx.data.Extraction(
                    extraction_class="knowledge_entry",
                    extraction_text="pTau/Abeta42 ratio (>0.023) in CSF identified AD with a sensitivity of 85% (CI: 81-89%) and specificity of 70% (CI: 65-75%)",
                    attributes={
                        "evidence_type": "molecular_biomarker",
                        "marker_name": "pTau/Abeta42 ratio",
                        "target_disease": "AD",
                        "sens": 0.85,
                        "sens_ci_lower": 0.81,
                        "sens_ci_upper": 0.89,
                        "spec": 0.70,
                        "spec_ci_lower": 0.65,
                        "spec_ci_upper": 0.75,
                        "cutoff_value": 0.023,
                        "cutoff_direction": ">",
                        "sample_type": "CSF",
                        "measurement_platform": "Roche Elecsys"
                    }
                )
            ]
        )
    ]

    # 3. Run the extraction process
    print("Running LangExtract... (This may take several minutes)")
    result = lx.extract(
        text_or_documents=document_content,
        prompt_description=prompt,
        examples=examples,
        model_id="gemini-1.5-flash-latest",
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
    
    print("n--- Extraction complete! ---")
    print(f"Review the results by opening the HTML file in a browser: {html_path}")


def main():
    parser = argparse.ArgumentParser(description="Extract structured knowledge from a scientific paper.")
    parser.add_argument("--url", required=True, help="URL or local path to the PDF.")
    parser.add_argument("--output_dir", default="data/ingested_knowledge", help="Directory to save results.")
    args = parser.parse_args()
    
    run_extraction(source_document=args.url, output_dir=args.output_dir)

if __name__ == "__main__":
    main()
