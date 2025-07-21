# tools/annotator/annotate.py
import argparse
import json
from datetime import datetime
import traceback

# Try to import both pipelines
try:
    from tools.ml_pipelines.pipelines_axis2 import Axis2Pipeline
    axis2_available = True
except ImportError:
    axis2_available = False

try:
    from tools.ml_pipelines.pipelines_axis3 import Axis3Pipeline
    axis3_available = True
except ImportError:
    axis3_available = False


def generate_etiological_annotation(data):
    return data.get("etiology", "Etiology not specified")

def generate_molecular_annotation(data):
    """Generates Axis 2 annotation, using ML if features are available."""
    if axis2_available and "axis2_features" in data:
        print("INFO: Axis 2 features found. Executing prediction pipeline...")
        pipeline = Axis2Pipeline()
        return pipeline.predict(data["axis2_features"])
    else:
        return "Molecular profile not specified"

def generate_phenotypic_annotation(data):
    """Generates Axis 3 annotation, using ML if features are available."""
    if axis3_available and "axis3_features" in data:
        print("INFO: Axis 3 features found. Executing prediction pipeline...")
        pipeline = Axis3Pipeline()
        return pipeline.predict(data["axis3_features"])
    else:
        return "Phenotype not specified"

def main():
    parser = argparse.ArgumentParser(description="Generate a tridimensional diagnostic annotation for a clinical case.")
    parser.add_argument("--input", required=True, help="Path to the input JSON file.")
    parser.add_argument("--output", required=True, help="Path to the output annotation file.")
    parser.add_argument("--timestamp", default=datetime.now().strftime('%Y-%m-%d'), help="Timestamp label for the annotation.")
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        clinical_data = json.load(f)

    # Generate each axis
    axis1 = generate_etiological_annotation(clinical_data)
    axis2 = generate_molecular_annotation(clinical_data)
    axis3 = generate_phenotypic_annotation(clinical_data)

    full_annotation = f"[{args.timestamp}]: {axis1} / {axis2} / {axis3}"

    print(f"\n✅ Annotation saved to {args.output}")
    print(f"--- GENERATED 3-AXIS ANNOTATION ---\n{full_annotation}\n-----------------------------------")

if __name__ == "__main__":
    main()