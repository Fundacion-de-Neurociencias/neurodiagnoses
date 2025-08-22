import sys
from pathlib import Path
import pandas as pd
import subprocess
import os

sys.path.append(str(Path(__file__).parent.parent.absolute()))

PROGNOSIS_DIR = Path("neurodiagnoses-engine/tools/ml_pipelines/prognosis")
SCRIPT_1_TEMPORAL = PROGNOSIS_DIR / "1_calculate_temporal_features.py"
SCRIPT_2_TRAIN = PROGNOSIS_DIR / "2_train_prognosis_model.py"
SCRIPT_3_EVAL = PROGNOSIS_DIR / "3_evaluate_prognosis_model.py"
SCRIPT_4_PREDICT = PROGNOSIS_DIR / "4_predict_prognosis_risk.py"
INPUT_COHORT = Path("neurodiagnoses-engine/data/simulated/simulated_longitudinal_data.csv")
OUTCOMES_DATA = Path("neurodiagnoses-engine/data/simulated/longitudinal_outcomes.csv")

def run_pipeline_step(script_path: Path, *args):
    """Función helper para ejecutar un script de Python como un subproceso."""
    command = [sys.executable, str(script_path)] + list(args)
    print(f"n--- EJECUTANDO: {' '.join(command)} ---")
    env = os.environ.copy()
    result = subprocess.run(command, capture_output=True, text=True, env=env)
    
    print("--- STDOUT ---")
    print(result.stdout)
    print("--- STDERR ---")
    print(result.stderr)
    
    if result.returncode != 0 or "ERROR:" in result.stdout or "ERROR:" in result.stderr:
        print(f"!!!!!!!!!! ERROR: El script {script_path.name} ha fallado. !!!!!!!!!!!")
        raise subprocess.CalledProcessError(result.returncode, command)
    else:
        print(f"--- SUCCESS: El script {script_path.name} se ha ejecutado correctamente. --- ")

def test_prognosis_pipeline():
    print("--- [INICIO] Test de diagnóstico del pipeline de Prognosis ---")
    
    temp_dir = Path("tests/prognosis_temp_output")
    temp_dir.mkdir(exist_ok=True)
    
    temp_features_out = temp_dir / "temp_features.parquet"
    temp_merged_data = temp_dir / "temp_merged_data.parquet"
    model_out = temp_dir / "temp_model.joblib"
    eval_out = temp_dir / "temp_eval.json"
    predict_out = temp_dir / "temp_predictions.csv"

    # --- [CORRECCIÓN]: Usamos los nombres de argumentos correctos para cada script ---
    run_pipeline_step(SCRIPT_1_TEMPORAL, f"--data_path={INPUT_COHORT}", f"--output_path={temp_features_out}")

    # Load outcomes and merge with features
    features_df = pd.read_parquet(temp_features_out)
    outcomes_df = pd.read_csv(OUTCOMES_DATA)

    # Rename columns for consistency with the model trainer
    outcomes_df = outcomes_df.rename(columns={
        'follow_up_years': 'survival_duration_years',
        'cognitive_status_at_follow_up': 'survival_event_occurred'
    })

    # Merge features and outcomes
    merged_df = pd.merge(features_df, outcomes_df, left_on='SubjectID', right_on='subject_id', how='inner')
    merged_df = merged_df.drop(columns=['subject_id']) # Drop redundant subject_id column

    # Save the merged data as parquet for the next step
    merged_df.to_parquet(temp_merged_data)

    run_pipeline_step(SCRIPT_2_TRAIN, f"--data_path={temp_merged_data}", f"--model_out={model_out}")
    run_pipeline_step(SCRIPT_3_EVAL, f"--model_path={model_out}", f"--data_path={temp_merged_data}", f"--output_dir={temp_dir}")
    run_pipeline_step(SCRIPT_4_PREDICT, f"--model_path={model_out}", f"--data_path={temp_merged_data}", f"--output_path={predict_out}")

    print("n--- [FIN] Test de diagnóstico finalizado. Revisa los logs para el plan de reparación. ---")

if __name__ == "__main__":
    test_prognosis_pipeline()
