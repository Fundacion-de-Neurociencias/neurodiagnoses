import numpy as np

PATHOGENIC_MAP = {
    "PSEN1": "AD", "PSEN2": "AD", "APP": "AD",
    "HTT": "Huntington's",
    "GRN": "FTD", "MAPT": "FTD", "C9orf72": "FTD/ALS"
}
SPECIFIC_RISK_MAP = {
    "APOE_e4": {"disease": "AD", "multiplier": 1.5}
}
NON_SPECIFIC_RISK_MAP = {
    "APOE_e4_shared_signature": {"diseases": ["AD", "PD", "FTD"], "boost": 0.1}
}
DISEASE_CLASSES = ['AD', 'PD', 'FTD', 'DLB', 'CO', "Huntington's", 'FTD/ALS']

def predict_etiology(patient_genetics: dict) -> dict:
    """Predicts disease probabilities based on a rules-engine for genetic variants."""
    probabilities = {disease: 1.0 / len(DISEASE_CLASSES) for disease in DISEASE_CLASSES}
    genetics = patient_genetics.get("genetics", {})
    for variant in genetics.get("pathogenic_variants", []):
        variant_gene = variant.split('_')[0]
        if variant_gene in PATHOGENIC_MAP:
            disease = PATHOGENIC_MAP[variant_gene]
            for d in probabilities:
                probabilities[d] = 0.01
            probabilities[disease] = 1.0 - (0.01 * (len(DISEASE_CLASSES) - 1))
            return probabilities
    for variant in genetics.get("disease_specific_risk", []):
        if variant in SPECIFIC_RISK_MAP:
            risk_info = SPECIFIC_RISK_MAP[variant]
            disease = risk_info["disease"]
            multiplier = risk_info["multiplier"]
            if disease in probabilities:
                probabilities[disease] *= multiplier
    for variant in genetics.get("non_specific_risk", []):
        if variant in NON_SPECIFIC_RISK_MAP:
            risk_info = NON_SPECIFIC_RISK_MAP[variant]
            for disease in risk_info["diseases"]:
                if disease in probabilities:
                    probabilities[disease] += risk_info["boost"]
    total_prob = sum(probabilities.values())
    if total_prob > 0:
        for disease in probabilities:
            probabilities[disease] /= total_prob
    return probabilities
