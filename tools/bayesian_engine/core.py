import pandas as pd
from pathlib import Path

def load_knowledge_base(kb_path: Path) -> pd.DataFrame:
    """
    Loads a knowledge base CSV file into a pandas DataFrame.
    """
    if not kb_path.exists():
        raise FileNotFoundError(f"Knowledge base file not found at: {kb_path}")
    
    print(f"INFO: Loading Knowledge Base from {kb_path}...")
    df = pd.read_csv(kb_path)
    print("SUCCESS: Knowledge Base loaded.")
    print("--- KB Schema ---")
    print(df.info())
    print("-----------------")
    return df

def get_likelihoods(kb_df: pd.DataFrame, biomarker: str, disease: str) -> (float, float):
    """
    Finds the likelihoods (sensitivity and specificity) for a given biomarker and disease.
    
    Returns:
        A tuple of (sensitivity, 1 - specificity).
    """
    # Find sensitivity: P(test_positive | has_disease)
    sens_row = kb_df[
        (kb_df['biomarker_name'] == biomarker) & 
        (kb_df['statistic_type'] == 'sensitivity') & 
        (kb_df['primary_disease'] == disease)
    ]
    if sens_row.empty:
        raise ValueError(f"Sensitivity not found for biomarker '{biomarker}' and disease '{disease}'")
    sensitivity = sens_row.iloc[0]['value']

    # Find specificity: P(test_negative | no_disease)
    spec_row = kb_df[
        (kb_df['biomarker_name'] == biomarker) & 
        (kb_df['statistic_type'] == 'specificity') & 
        (kb_df['primary_disease'] == disease)
    ]
    # If specificity is not found for a biomarker, we assume a neutral value for this PoC.
    # A more advanced version would handle this with more nuance.
    specificity = spec_row.iloc[0]['value'] if not spec_row.empty else 0.5
    
    # P(test_positive | no_disease) = 1 - specificity
    false_positive_rate = 1 - specificity

    return sensitivity, false_positive_rate

def calculate_posterior(prior: float, sensitivity: float, false_positive_rate: float) -> float:
    """
    Calculates the posterior probability using Bayes' theorem for a positive test result.
    P(Disease | Positive) = [P(Positive | Disease) * P(Disease)] / P(Positive)
    where P(Positive) = P(Positive | Disease) * P(Disease) + P(Positive | No Disease) * P(No Disease)
    """
    p_positive = (sensitivity * prior) + (false_positive_rate * (1 - prior))
    if p_positive == 0:
        return 0.0
    
    posterior = (sensitivity * prior) / p_positive
    return posterior

def run_inference_poc():
    """
    Runs a Proof-of-Concept for the Bayesian inference engine.
    """
    print("\n--- [BAYESIAN INFERENCE ENGINE - PROOF OF CONCEPT] ---")
    
    # 1. Cargar la base de conocimiento
    kb_path = Path("data/knowledge_base/axis2_likelihoods.csv")
    kb_df = load_knowledge_base(kb_path)

    # 2. Definir la evidencia del paciente y la probabilidad a priori
    patient_evidence = {
        "biomarker": "p-tau181",
        "result": "positive" # Asumimos un resultado positivo para este PoC
    }
    disease_in_question = "Alzheimer's Disease"
    prior_probability = 0.20 # La creencia inicial del clínico es del 20%

    print(f"\n--- Inference Scenario ---")
    print(f"Patient Evidence: {patient_evidence['biomarker']} is {patient_evidence['result']}")
    print(f"Disease in Question: {disease_in_question}")
    print(f"Prior Probability (Initial Belief): {prior_probability:.2f}")
    print("--------------------------")

    # 3. Obtener las verosimilitudes (likelihoods) de la base de conocimiento
    try:
        sensitivity, false_positive_rate = get_likelihoods(kb_df, patient_evidence['biomarker'], disease_in_question)
        print(f"INFO: Found Likelihoods in KB:")
        print(f"  - Sensitivity (P(Positive|AD)): {sensitivity:.2f}")
        print(f"  - False Positive Rate (P(Positive|Not AD)): {false_positive_rate:.2f}")
    except ValueError as e:
        print(f"ERROR: Could not run inference. {e}")
        return

    # 4. Calcular la probabilidad posterior
    posterior_probability = calculate_posterior(prior_probability, sensitivity, false_positive_rate)

    print("\n--- Inference Result ---")
    print(f"Posterior Probability (Updated Belief): {posterior_probability:.2f}")
    print(f"Conclusion: The positive {patient_evidence['biomarker']} result increased the probability of {disease_in_question} from {int(prior_probability*100)}% to {int(posterior_probability*100)}%.")
    print("------------------------")


if __name__ == "__main__":
    run_inference_poc()
