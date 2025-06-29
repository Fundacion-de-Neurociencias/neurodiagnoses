import json 
import argparse 
def load_data(input_file): 
    with open(input_file, 'r', encoding='utf-8') as f: 
        return json.load(f) 
def annotate(data, timestamp): 
    axis1 = data.get("etiology", "Unknown etiology") 
    axis2_data = data.get("molecular_pathology", {}) 
    axis3_data = data.get("neuroanatomical_clinical", {}) 
    if isinstance(axis1, dict): 
        etiology = axis1.get("type", "Unknown etiology") 
        details = ", ".join(axis1.get("risk_factors", [])) 
        axis1_str = f"{etiology} ({details})" if details else etiology 
    elif isinstance(axis1, str): 
        axis1_str = axis1 
    else: 
        axis1_str = "Unknown etiology" 
    if isinstance(axis2_data, dict): 
        primary = ", ".join(axis2_data.get("primary", [])) 
        secondary = ", ".join(axis2_data.get("secondary", [])) 
        axis2_str = f"{primary}; {secondary}" if secondary else primary 
    else: 
        axis2_str = "Unknown molecular pathology" 
    if isinstance(axis3_data, dict): 
        findings = "; ".join([f"{region}: {desc}" for region, desc in axis3_data.items()]) 
        axis3_str = findings if findings else "Unknown neuroanatomical-clinical correlation" 
    else: 
        axis3_str = "Unknown neuroanatomical-clinical correlation" 
    return f"[{timestamp}]: {axis1_str} / {axis2_str} / {axis3_str}" 
def main(): 
    parser = argparse.ArgumentParser(description="Generate 3D annotation from clinical case") 
    parser.add_argument('--input', required=True, help='Input JSON file') 
    parser.add_argument('--timestamp', required=True, help='Timestamp for the annotation') 
    parser.add_argument('--output', required=True, help='Output text file') 
    args = parser.parse_args() 
    data = load_data(args.input) 
    result = annotate(data, args.timestamp) 
    with open(args.output, 'w', encoding='utf-8') as f: 
        f.write(result + "\n") 
if __name__ == '__main__': 
    main() 
