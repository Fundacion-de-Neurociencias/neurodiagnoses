# Módulo de Ingesta de Datos

Este documento describe el pipeline de ingesta y preprocesamiento de datos del proyecto Neurodiagnoses.

## 1. Unificación de Datos Multi-ómicos

**Script:** `tools/data_ingestion/unify_multiomics_data.py`

### Propósito

Este script es el punto de entrada del pipeline de datos. Su función principal es consolidar múltiples fuentes de datos de pacientes en una única tabla unificada para facilitar el análisis y el modelado.

### Proceso

1.  **Carga de Datos**: El script lee los siguientes tres archivos CSV:
    *   `clinical_data.csv`: Contiene datos demográficos y puntuaciones de tests cognitivos.
    *   `imaging_metrics.csv`: Contiene métricas clave extraídas de imágenes de resonancia magnética (RM).
    *   `genomics_summary.csv`: Contiene información genética relevante, como el genotipo APOE.

2.  **Lógica de Unificación**: Los tres DataFrames se fusionan en uno solo utilizando la columna `patient_id` como clave. Se realiza una unión externa (`outer join`) para asegurar que se conserven todos los registros de pacientes, incluso si falta información en alguno de los archivos fuente.

3.  **Salida**: El DataFrame unificado se guarda en el siguiente archivo en formato Parquet, que es eficiente para almacenar datos tabulares:
    *   `data/processed/unified_patient_data.parquet`

### Uso

Para ejecutar el script y generar el archivo de datos unificado, corre el siguiente comando desde el directorio raíz del proyecto:

```bash
python tools/data_ingestion/unify_multiomics_data.py
```

---

## 2. Control de Calidad (QC) de Datos

**Script:** `tools/data_ingestion/qc.py`

### Propósito

Este script ejecuta una serie de comprobaciones de calidad sobre los datos unificados para garantizar su integridad antes de que pasen a las fases de modelado. Unos datos de alta calidad son fundamentales para construir modelos predictivos fiables.

### Proceso

El script lee el archivo `unified_patient_data.parquet` y realiza las siguientes validaciones:

1.  **Comprobación de Valores Faltantes**: Identifica y reporta el porcentaje de valores nulos en cada columna. Esto es clave para decidir estrategias de imputación de datos si fuera necesario.
2.  **Comprobación de Tipos de Datos**: Verifica que las columnas numéricas (ej. `age`, `MMSE`) y categóricas tengan los tipos de datos correctos (`int`, `float`, `object`).
3.  **Comprobación de Rangos de Valores**: Realiza comprobaciones de sanidad para asegurar que los valores de ciertas columnas estén dentro de un rango esperado y plausible (ej. `MMSE` entre 0 y 30).

### Uso

Para ejecutar el script de control de calidad, corre el siguiente comando desde el directorio raíz del proyecto:

```bash
python tools/data_ingestion/qc.py
```
