import pandas as pd
import numpy as np
from pathlib import Path

def generate_axis1_kb(output_path: Path, num_entries: int):
    print(f"SIMULATING: Generating {num_entries} genetic entries for Axis 1...")
    # Creamos un APOE4 para asegurarnos de que existe uno real
    data = [{'biomarker_name': 'APOE_e4', 'statistic_type': 'odds_ratio', 'value': 3.2, 'ci_lower': 2.8, 'ci_upper': 3.8, 'primary_disease': "Alzheimer's Disease", 'source_snippet': 'Farrer et al., 1997, JAMA'}]
    
    # Generamos el resto
    snps = [f"rs{np.random.randint(1000, 9999999)}" for _ in range(num_entries - 1)]
    odds_ratios = np.random.lognormal(mean=0.2, sigma=0.4, size=num_entries - 1)
    diseases = np.random.choice(["Alzheimer's Disease", "Parkinson's Disease", "FTD"], size=num_entries - 1)
    
    for i in range(num_entries - 1):
        or_val = odds_ratios[i]
        ci_width = or_val * np.random.uniform(0.1, 0.3)
        data.append({
            'biomarker_name': snps[i], 'statistic_type': 'odds_ratio', 'value': or_val,
            'ci_lower': or_val - ci_width / 2, 'ci_upper': or_val + ci_width / 2,
            'primary_disease': diseases[i], 'source_snippet': f"GWAS Catalog PMID:{np.random.randint(20000000, 30000000)}"
        })

    pd.DataFrame(data).to_csv(output_path, index=False)
    print(f"SUCCESS: Simulated Axis 1 KB created with {len(data)} entries.")

def generate_axis3_kb(output_path: Path):
    print("SIMULATING: Generating imaging entries for Axis 3 with laterality...")
    # Lista más amplia de regiones cerebrales
    regions = ['Hippocampus', 'Entorhinal', 'Precuneus', 'Amygdala', 'TemporalLobe', 'FrontalLobe', 'Cingulate']
    data = []
    for region in regions:
        for hemisphere in ['Left', 'Right']:
            biomarker = f"{hemisphere}_{region}_Volume"
            mean_ad, std_ad = (np.random.uniform(2800, 3500), np.random.uniform(50, 150))
            data.append({'axis': 3, 'biomarker_name': biomarker, 'statistic_type': 'distribution_mean', 'value': mean_ad, 'cohort_description': 'ADNI cohort - AD group'})
            data.append({'axis': 3, 'biomarker_name': biomarker, 'statistic_type': 'distribution_std', 'value': std_ad, 'cohort_description': 'ADNI cohort - AD group'})
            mean_ctrl, std_ctrl = (np.random.uniform(4000, 4800), np.random.uniform(100, 200))
            data.append({'axis': 3, 'biomarker_name': biomarker, 'statistic_type': 'distribution_mean', 'value': mean_ctrl, 'cohort_description': 'ADNI cohort - Control group'})
            data.append({'axis': 3, 'biomarker_name': biomarker, 'statistic_type': 'distribution_std', 'value': std_ctrl, 'cohort_description': 'ADNI cohort - Control group'})

    pd.DataFrame(data).to_csv(output_path, index=False)
    print(f"SUCCESS: Simulated Axis 3 KB created with {len(data)} entries.")

# Borramos los ficheros antiguos y los regeneramos con miles de entradas
axis1_path = Path("data/knowledge_base/axis1_likelihoods.csv")
axis3_path = Path("data/knowledge_base/axis3_likelihoods.csv")
axis1_path.unlink(missing_ok=True)
axis3_path.unlink(missing_ok=True)

generate_axis1_kb(axis1_path, 5000)
generate_axis3_kb(axis3_path)
