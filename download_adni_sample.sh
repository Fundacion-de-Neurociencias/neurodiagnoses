#!/bin/bash
set -e
set -x

# --- FASE 1: Definir la configuración ---
# Datos de ejemplo de un dataset de neurociencia.
OUTPUT_DIR="data/raw/imaging"
SAMPLE_FILE="${OUTPUT_DIR}/neuroscience_sample.csv"
LINE_COUNT=6 # 1 cabecera + 5 filas de datos

# --- FASE 2: Preparar el entorno y crear la muestra ---
echo "INFO: Creating directory for raw imaging data..."
mkdir -p "$OUTPUT_DIR"

echo "INFO: Creating a sample neuroscience data file..."
cat <<EOF > "$SAMPLE_FILE"
SubjectID,Age,Gender,MemoryScore,AttentionScore,HippocampusVolume_mm3,Diagnosis
001,25,M,85,92,4500,Control
002,30,F,78,88,4350,Control
003,68,M,55,62,3200,AD
004,72,F,50,58,3150,AD
005,45,F,70,75,4000,MCI
EOF

# --- FASE 3: VERIFICAR que la creación no ha resultado en un fichero vacío ---
if [ ! -s "$SAMPLE_FILE" ]; then
    echo "ERROR: The file creation resulted in an empty file."
    exit 1
fi
echo "SUCCESS: Neuroscience data sample created and verified."

# --- FASE 4: Analizar la estructura del fichero ---
echo "INFO: Analyzing the structure of the sample file..."

echo -e "\n--- [ Columnas Disponibles (Variables del Dataset) ] ---"
# Mostramos la primera línea (la cabecera) y reemplazamos las comas por saltos de línea
head -n 1 "$SAMPLE_FILE" | tr ',' '\n'
echo "------------------------------------------------------------"

echo -e "\n--- [ Vistazo a los Primeros 5 Sujetos ] ---"
# Mostramos las primeras 5 líneas y las formateamos como una tabla
head -n 5 "$SAMPLE_FILE" | column -s, -t
echo "--------------------------------------------------"
