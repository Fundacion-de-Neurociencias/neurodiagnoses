#!/bin/bash
set -e

# --- Ocultamos el modo 'set -x' para una salida limpia ---
set +x
echo "============================================================"
echo "    INFORME DE ESTADO DE LA BASE DE CONOCIMIENTO NEURODIAGNOSES"
echo "============================================================"
echo "Generado el: $(date)"
echo ""

echo "--- [1. Ficheros de la Base de Conocimiento Activos] ---"
ls -1h data/knowledge_base/*.csv
echo ""

echo "--- [2. Profundidad: Número de Entradas por Eje] ---"
# Iteramos sobre cada fichero de la KB para contar sus entradas
for kb_file in data/knowledge_base/*.csv; do
    if [ -f "$kb_file" ]; then
        # Contamos las líneas y restamos 1 por la cabecera
        entry_count=$(($(wc -l < "$kb_file") - 1))
        echo "  - $(basename "$kb_file"): $entry_count entradas"
    fi
done
echo ""

echo "--- [3. Amplitud: Cobertura Actual por Eje] ---"
# Analizamos cada eje si el fichero existe
AXIS1_FILE="data/knowledge_base/axis1_likelihoods.csv"
AXIS2_FILE="data/knowledge_base/axis2_likelihoods.csv"
AXIS3_FILE="data/knowledge_base/axis3_likelihoods.csv"

if [ -f "$AXIS1_FILE" ]; then
    echo "  - EJE 1 (Genética):"
    UNIQUE_VARIANTS=$(tail -n +2 "$AXIS1_FILE" | cut -d, -f1 | sort -u | wc -l)
    UNIQUE_DISEASES=$(tail -n +2 "$AXIS1_FILE" | cut -d, -f6 | sort -u | tr 'n' ',' | sed 's/,$//')
    echo "    - Variantes genéticas únicas: $UNIQUE_VARIANTS"
    echo "    - Enfermedades cubiertas: $UNIQUE_DISEASES"
fi
if [ -f "$AXIS2_FILE" ]; then
    echo "  - EJE 2 (Molecular):"
    UNIQUE_BIOMARKERS=$(tail -n +2 "$AXIS2_FILE" | cut -d, -f1 | sort -u | wc -l)
    UNIQUE_DISEASES=$(tail -n +2 "$AXIS2_FILE" | cut -d, -f8 | sort -u | tr 'n' ',' | sed 's/,$//')
    echo "    - Biomarcadores únicos: $UNIQUE_BIOMARKERS"
    echo "    - Enfermedades cubiertas: $UNIQUE_DISEASES"
fi
if [ -f "$AXIS3_FILE" ]; then
    echo "  - EJE 3 (Fenotipo):"
    UNIQUE_MARKERS=$(tail -n +2 "$AXIS3_FILE" | cut -d, -f2 | sort -u | wc -l)
    UNIQUE_DISEASES=$(tail -n +2 "$AXIS3_FILE" | cut -d, -f8 | sort -u | tr 'n' ',' | sed 's/,$//')
    echo "    - Marcadores (Clínicos/Imagen) únicos: $UNIQUE_MARKERS"
    echo "    - Enfermedades cubiertas: $UNIQUE_DISEASES"
fi
echo ""

echo "--- [4. Origen: Fuentes de Datos Primarias Utilizadas] ---"
echo "  - Resúmenes Curados (Vía 1):"
ls -1 data/ingested_knowledge/summaries/*.md
echo "  - Datos en Bruto (Vía 2):"
ls -1 data/raw/genomics/*.tsv
ls -1 data/raw/imaging/*.csv
echo ""

echo "============================================================"