# tools/tridimensional_annotation/annotator.py
# (Refactored to decouple logic from presentation)

from datetime import datetime


def generate_tridimensional_annotation(
    patient_id: str,
    axis1_genetics: dict,
    axis2_molecular_profile: dict,
    axis3_severity_map: dict,
) -> str:
    """
    Generates a full, structured tridimensional diagnostic annotation
    by formatting pre-calculated results.

    Args:
        patient_id (str): The patient's identifier.
        axis1_genetics (dict): A dict with genetic findings (e.g., {'APOE_e4': 1}).
        axis2_molecular_profile (dict): The dict of posterior probabilities from the Bayesian engine.
        axis3_severity_map (dict): The dict of results from the Axis 3 severity mapper.

    Returns:
        str: The final, formatted diagnostic string.
    """
    print(f"--- Formatting Tridimensional Annotation for Subject ID: {patient_id} ---")

    # --- AXIS 1: ETIOLOGY ---
    # Formats the pre-calculated genetic data.
    axis1_findings = []
    if axis1_genetics.get("APOE_e4", 0) > 0:
        axis1_findings.append(
            f"Sporadic (APOE_e4 Positive, {axis1_genetics['APOE_e4']} allele(s))"
        )
    else:
        axis1_findings.append("Sporadic (APOE_e4 Negative)")
    axis1_text = ", ".join(axis1_findings)

    # --- AXIS 2: MOLECULAR MARKERS ---
    # Formats the pre-calculated Bayesian probabilities.
    if axis2_molecular_profile:
        # Find the diagnosis with the highest probability
        top_molecular_dx = max(axis2_molecular_profile, key=axis2_molecular_profile.get)
        top_prob = axis2_molecular_profile[top_molecular_dx]
        # This simulates finding a secondary biomarker, can be expanded later
        secondary_marker = "NfL (moderate neurodegenerative activity)"
        axis2_text = f"Primary: {top_molecular_dx} profile ({top_prob:.1%}); Secondary: {secondary_marker}"
    else:
        axis2_text = "Molecular profile could not be determined."

    # --- AXIS 3: NEUROANATOMOCLINICAL CORRELATIONS ---
    # Formats the pre-calculated severity mapping results.
    top_region = max(
        axis3_severity_map.get("key_contributing_regions", {}),
        key=lambda k: abs(axis3_severity_map["key_contributing_regions"][k]),
        default="N/A",
    )
    # This simulates linking the top region to a clinical symptom
    clinical_correlation = "Episodic Memory Deficit"
    axis3_text = f"{top_region.replace('_volume','')} atrophy: {clinical_correlation}"

    # --- FINAL ANNOTATION ---
    timestamp = datetime.now().strftime("%B %y")  # Format: Month YY
    final_annotation = f"[{timestamp}]: {axis1_text} / {axis2_text} / {axis3_text}"

    return final_annotation
