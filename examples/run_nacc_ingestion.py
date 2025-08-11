# examples/run_nacc_ingestion.py
import json
from dataclasses import asdict

# Add project root to path for cross-module imports
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.data_ingestion.parsers.nacc_adapter import parse_nacc_data

def main():
    """Demonstrates the NACC adapter by parsing a sample file and printing the result."""
    
    nacc_sample_file = 'data/simulated/nacc_sample_data.csv'
    
    # Use the adapter to get a list of standardized patient objects
    patient_cohort = parse_nacc_data(nacc_sample_file)
    
    if patient_cohort:
        print("\n--- STANDARDIZED OUTPUT (First Patient) ---")
        # Convert the first patient's dataclass object to a dictionary for pretty printing
        first_patient_dict = asdict(patient_cohort[0])
        print(json.dumps(first_patient_dict, indent=2))
        
        # You can now iterate through the cohort and use these standardized objects
        # as input for the processing and modeling pipelines.
        print(f"\nThis standardized cohort of {len(patient_cohort)} patients is now ready for the AI models.")

if __name__ == '__main__':
    main()
