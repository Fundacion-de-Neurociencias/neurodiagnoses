# -*- coding: utf-8 -*-
"""
Knowledge Ingestion Pipeline: Step 1 - Preprocess PDF to Markdown
(Refactored to read from a central knowledge source registry)
"""
import os
import sys
import pandas as pd
import requests
from pathlib import Path
from pymupdf4llm import to_markdown
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SOURCES_CSV = "data/reference/knowledge_sources.csv"
OUTPUT_DIR = "data/ingested_knowledge/markdown"

def download_file(url, filename):
    """Downloads a file from a URL if it doesn't exist locally."""
    if not os.path.exists(filename):
        print(f"Downloading from {url}...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        try:
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(response.content)
            print("Download complete.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Download failed for {url}. Reason: {e}")
            return False
    else:
        print(f"PDF file '{filename}' already exists locally. Skipping download.")
        return True

def preprocess_pdf(pdf_path: str, output_dir: str):
    """Converts a local PDF file to a clean Markdown file."""
    print(f"--- Starting PDF to Markdown conversion for: {pdf_path} ---")
    md_filename = Path(pdf_path).stem + ".md"
    md_path = Path(output_dir) / md_filename
    md_text = to_markdown(pdf_path)
    md_path.write_text(md_text, encoding="utf-8")
    print(f"✅ Successfully converted PDF to Markdown: {md_path}")
    return str(md_path)

def main():
    """
    Main function to orchestrate the preprocessing of all pending papers.
    """
    print("--- Starting Knowledge Preprocessing Pipeline ---")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    try:
        sources_df = pd.read_csv(SOURCES_CSV)
    except FileNotFoundError:
        print(f"ERROR: Source registry not found at {SOURCES_CSV}")
        return

    pending_papers = sources_df[sources_df['status'] == 'pending']
    print(f"Found {len(pending_papers)} papers to process.")

    for index, row in pending_papers.iterrows():
        source_id = row['source_id']
        pdf_url = row['pdf_url']
        local_filename = f"{source_id}.pdf"
        
        print(f"nProcessing: {source_id} ({pdf_url})")
        
        # Update last attempt time
        sources_df.loc[index, 'last_attempt'] = datetime.now().isoformat()
        
        if download_file(pdf_url, local_filename):
            try:
                preprocess_pdf(local_filename, OUTPUT_DIR)
                sources_df.loc[index, 'status'] = 'preprocessed'
            except Exception as e:
                print(f"ERROR: Failed to convert {local_filename} to Markdown. Reason: {e}")
                sources_df.loc[index, 'status'] = 'preprocess_failed'
        else:
            sources_df.loc[index, 'status'] = 'download_failed'
            
    # Save the updated status back to the CSV
    sources_df.to_csv(SOURCES_CSV, index=False)
    print("n--- Knowledge Preprocessing Pipeline Finished ---")
    print(f"Updated status in {SOURCES_CSV}")

if __name__ == "__main__":
    main()
