import os
import argparse
from pathlib import Path
import langextract as lx
import textwrap
from pydantic import BaseModel, Field
from typing import Literal, Optional, List
from langextract.providers.ollama import OllamaLanguageModel

# --- Pydantic Schema Definition (Version 2 - Enhanced for Uncertainty) ---
class KnowledgeEntry(BaseModel):
    """
    A single, atomic piece of evidence extracted from a scientific paper,
    including data for uncertainty quantification.
    """
    axis: Literal[1, 2, 3] = Field(..., description="The evidence axis: 1 (Etiology/Genetic), 2 (Molecular Profile), or 3 (Phenotypic Profile).")
    biomarker_name: str = Field(..., description="The specific name of the biomarker, gene, or clinical metric (e.g., 'CSF p-tau181', 'APOE4', 'MMSE Score').")
    statistic_type: Literal[
        "sensitivity", "specificity", "accuracy", "auc",
        "odds_ratio", "hazard_ratio", "relative_risk",
        "correlation_coefficient", "prior_probability"
    ] = Field(..., description="The type of statistical measure reported.")
    value: float = Field(..., description="The numerical point estimate of the statistic.")
    confidence_interval: Optional[List[float]] = Field(None, description="The lower and upper bounds of the 95% confidence interval. Crucial for uncertainty modeling. Example: [0.81, 0.89]")
    sample_size: Optional[int] = Field(None, description="The total sample size (n) used to calculate the statistic. Highly valuable for modeling distributions.")
    cohort_description: str = Field(..., description="A brief description of the cohort used for the measurement (e.g., 'AD vs Healthy Controls', 'FTD patients').")
    primary_disease: str = Field(..., description="The main neurodegenerative disease being studied (e.g., 'Alzheimer\'s Disease', 'Parkinson\'s Disease', 'FTD').")
    source_snippet: str = Field(..., description="The exact text snippet from the paper that contains and supports this extracted data.")

def main():
    """
    Main function to run the knowledge extraction pipeline.
    """
    parser = argparse.ArgumentParser(description="Extract structured knowledge from a Markdown file using an LLM.")
    parser.add_argument(
        "--input-md",
        type=Path,
        required=True,
        help="Path to the input Markdown file."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory to save the output .jsonl and .html files."
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default="tinyllama",
        help="The name of the Ollama model to use."
    )
    args = parser.parse_args()

    print(f"INFO: Starting knowledge extraction process for: {args.input_md}")

    # --- Ensure output directory exists ---
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_base_name = args.input_md.stem
    output_jsonl_path = args.output_dir / f"{output_base_name}.jsonl"
    output_html_path = args.output_dir / f"{output_base_name}.html"

    # --- Load the source document ---
    try:
        with open(args.input_md, 'r', encoding='utf-8') as f:
            document_text = f.read()
        print(f"INFO: Successfully loaded Markdown file ({len(document_text)} characters).")
    except FileNotFoundError:
        print(f"ERROR: Input file not found at {args.input_md}")
        return

    # --- Define the extraction prompt and examples ---
    prompt = textwrap.dedent("""
        Extract protein biomarker performance data for neurodegenerative diseases (PD, AD, ALS).
        From tables or text, identify the protein name, the Hazard Ratio (HR) and 95% Confidence Interval (CI),
        the associated p-value, the primary disease, and any mentioned cross-disease associations.
        Ensure extractions are grounded in the exact source text.
        Return the output as a JSON array of objects, where each object conforms to the KnowledgeEntry schema.
        """)
    examples = [
        lx.data.ExampleData(
            text="TPPP2 showed a HR of 0.70 (0.61-0.80) with a p-value of 7.06E-08.",
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

    # --- Initialize Ollama Language Model ---
    ollama_model = OllamaLanguageModel(
        model_id=args.model_name,
        model_url="http://localhost:11434",
        timeout=600, # Increased timeout for potentially long extractions
        fence_output=True,
        use_schema_constraints=False
    )

    # --- Run the Extraction ---
    print(f"INFO: Running extraction with model: {args.model_name}. This may take some time...")
    results = lx.extract(
        text_or_documents=document_text,
        prompt_description=prompt,
        examples=examples,
        model=ollama_model, # Pass the OllamaLanguageModel instance
    )
    print(f"INFO: Extraction complete. Found {len(results.extractions)} potential knowledge entries.")

    # --- Save the Results ---
    if results.extractions:
        # Save as JSONL
        with open(output_jsonl_path, 'w', encoding='utf-8') as f:
            for entry in results.extractions:
                f.write(entry.model_dump_json() + '\n')
        print(f"INFO: Structured data saved to: {output_jsonl_path}")

        # Save HTML visualization
        html_content = lx.visualize(results) # Pass the AnnotatedDocument directly
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"INFO: Visualized results saved to: {output_html_path}")
    else:
        print("WARNING: No structured knowledge entries were extracted. The output files will be empty.")


if __name__ == "__main__":
    main()