# tools/simulation_engine/graph_based_simulator.py
import json
import os
import random

import networkx as nx

DATA_DIR = "data"
HPO_GRAPH_PATH = os.path.join(DATA_DIR, "hpo_graph.graphml")
OUTPUT_DATASET_PATH = os.path.join(DATA_DIR, "simulated_patient_dataset.jsonl")


def simulate_patients(num_patients=1000, max_phenotypes=15, walk_probability=0.3):
    """
    Uses the HPO knowledge graph to simulate a dataset of patients.
    """
    # 1. Load the knowledge graph
    if not os.path.exists(HPO_GRAPH_PATH):
        print(f"Error: Knowledge graph not found at {HPO_GRAPH_PATH}")
        print("Please run the hpo_parser.py script first.")
        return
    print(f"Loading knowledge graph from {HPO_GRAPH_PATH}...")
    G = nx.read_graphml(HPO_GRAPH_PATH)

    # 2. Define seed diseases (causal gene -> seed HPO terms)
    # These are the "starting points" for our simulation.
    disease_seeds = {
        "SIM_GENE_A": ["HP:0001250"],  # Seizure
        "SIM_GENE_B": ["HP:0001298", "HP:0000726"],  # Encephalopathy, Dementia
        "SIM_GENE_C": ["HP:0001300", "HP:0002069"],  # Parkinsonism, Bradykinesia
    }

    # 3. Simulate patient profiles
    print(f"Simulating {num_patients} patients...")
    dataset = []
    for i in range(num_patients):
        patient_id = f"SIM_{i+1}"
        causal_gene, seed_phenotypes = random.choice(list(disease_seeds.items()))

        patient_phenotypes = set(seed_phenotypes)

        # Simulate phenotype spread by walking the graph
        current_phenotypes = list(seed_phenotypes)
        while len(patient_phenotypes) < max_phenotypes:
            if not current_phenotypes:
                break
            current_node = random.choice(current_phenotypes)

            # Get neighbors (parents and children in the ontology)
            neighbors = list(G.predecessors(current_node)) + list(
                G.successors(current_node)
            )
            if not neighbors:
                current_phenotypes.remove(current_node)
                continue

            # With a certain probability, add a related phenotype
            if random.random() < walk_probability:
                new_phenotype = random.choice(neighbors)
                patient_phenotypes.add(new_phenotype)
                current_phenotypes.append(new_phenotype)
            else:
                # Stop expanding this path
                current_phenotypes.remove(current_node)

        dataset.append(
            {
                "patient_id": patient_id,
                "causal_gene": causal_gene,
                "phenotypes": list(patient_phenotypes),
            }
        )

    # 4. Save the dataset
    print(f"Saving dataset to {OUTPUT_DATASET_PATH}...")
    with open(OUTPUT_DATASET_PATH, "w") as f:
        for entry in dataset:
            f.write(json.dumps(entry) + "\n")

    print(f"\n✅ Simulation complete. {len(dataset)} patients saved.")


if __name__ == "__main__":
    simulate_patients()
