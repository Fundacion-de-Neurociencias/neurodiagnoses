# Documentación de Pipelines de Machine Learning (ML)

Este documento describe los componentes del pipeline de ML, comenzando por la preparación de datos para el modelado.

## 1. Ingeniería de Características para Biomarcadores

**Script:** `tools/ml_pipelines/build_biomarker_features.py`

### Propósito

Este script transforma los datos unificados y limpios en un conjunto de datos listo para ser utilizado por algoritmos de Machine Learning. La ingeniería de características es un paso crítico para maximizar el rendimiento del modelo.

### Proceso

El script lee el archivo `unified_patient_data.parquet` y realiza las siguientes operaciones:

1.  **Selección de Características**: Se elige un subconjunto de las columnas más relevantes para la predicción inicial. A medida que el proyecto evolucione, aquí se incorporarán biomarcadores más avanzados (p-tau, GFAP, NfL).
2.  **Manejo de Datos Faltantes**: Los valores nulos en la columna `other_variants` se rellenan con la cadena de texto "None", convirtiéndolo en una categoría explícita.
3.  **Codificación de Variables Categóricas**: Las variables no numéricas se convierten a un formato numérico. Específicamente, la columna `sex` se transforma en una variable binaria (0 o 1) mediante codificación *one-hot*.

### Salida

El DataFrame procesado se guarda en el siguiente archivo, que servirá como entrada directa para el entrenamiento del modelo:

*   `data/processed/featured_patient_data.parquet`

### Uso

Para ejecutar el script y generar el archivo de datos con características, corre el siguiente comando desde el directorio raíz del proyecto:

```bash
python tools/ml_pipelines/build_biomarker_features.py
```

---

## 2. Entrenamiento del Modelo de Screening

**Script:** `models/train_model.py`

### Propósito

Este script entrena un modelo de clasificación que constituye el "Panel de Screening" inicial. Su objetivo es predecir una categoría de riesgo para los pacientes basada en sus datos de biomarcadores.

### Proceso

1.  **Carga de Datos**: El script lee el archivo `featured_patient_data.parquet`.
2.  **Creación de Variable Objetivo (Sintética)**: Dado que no se dispone de una etiqueta de diagnóstico real en los datos de ejemplo, el script crea una variable objetivo sintética llamada `risk_group`. Un paciente se etiqueta como de "Alto Riesgo" (`1`) si su puntuación `MMSE` es inferior a 24 y tiene al menos un alelo `APOE4`. En caso contrario, se considera de "Bajo Riesgo" (`0`). **Nota: Esta es una simplificación para fines de demostración.**
3.  **División de Datos**: El conjunto de datos se divide en subconjuntos de entrenamiento y prueba para poder evaluar el rendimiento del modelo de forma imparcial.
4.  **Entrenamiento del Modelo**: Se entrena un clasificador de Regresión Logística con los datos de entrenamiento.
5.  **Evaluación**: Se evalúa el rendimiento del modelo en el conjunto de prueba y se imprime un informe de clasificación y una matriz de confusión.

### Salida

El modelo entrenado y listo para usar se guarda en el siguiente archivo:

*   `models/screening_panel_v1.joblib`

### Uso

Para ejecutar el script de entrenamiento, corre el siguiente comando desde el directorio raíz:

```bash
python models/train_model.py
```

---

## 3. Estratificación de Pacientes por Endotipos

**Script:** `workflows/unified_modeling/endotyping.py`

### Propósito

Este script implementa el concepto de "Endotipos multi-ómicos" de tu plan. Utiliza un algoritmo de clustering no supervisado para agrupar a los pacientes en subgrupos biológicamente coherentes, basados en sus perfiles de biomarcadores.

### Proceso

1.  **Carga de Datos**: El script lee el archivo `featured_patient_data.parquet`.
2.  **Selección y Escalado de Características**: Se seleccionan las características numéricas relevantes para el clustering. Crucialmente, estas características se escalan (estandarizan) para que las variables con diferentes rangos (ej. `age` vs. `hippocampal_volume_norm`) contribuyan de manera equitativa al cálculo de distancias del algoritmo.
3.  **Clustering**: Se aplica el algoritmo K-Means para agrupar los datos. Para esta demostración, se buscan 2 clusters, que podrían representar endotipos como "neurodegenerativo puro" vs. "mixto/inflamatorio".
4.  **Asignación de Etiquetas**: A cada paciente se le asigna una etiqueta de cluster (`endotype`).

### Salida

Los datos de los pacientes, ahora con su etiqueta de endotipo, se guardan en:

*   `data/processed/endotyped_patient_data.parquet`

### Uso

Para ejecutar el script de clustering, corre el siguiente comando desde el directorio raíz:

```bash
python workflows/unified_modeling/endotyping.py
```

---

## 4. Explicabilidad del Modelo (XAI)

**Script:** `tools/ml_pipelines/explainability.py`

### Propósito

Cumpliendo con el requisito de "IA explicable", este script utiliza la librería SHAP para interpretar las predicciones del modelo de screening. Genera visualizaciones que muestran qué características influyen más en las decisiones del modelo, tanto para casos individuales como para el comportamiento global.

### Proceso

1.  **Carga de Modelo y Datos**: Se carga el modelo `screening_panel_v1.joblib` y los datos con características.
2.  **Cálculo de Valores SHAP**: Se utiliza un `KernelExplainer` de SHAP para calcular los valores de Shapley, que cuantifican la contribución de cada característica a la predicción.
3.  **Generación de Gráficos**: Se generan dos tipos de visualizaciones:
    *   **Gráfico de Fuerza (Local)**: Un gráfico interactivo (`force_plot`) que muestra las fuerzas que empujan la predicción hacia "Alto Riesgo" o "Bajo Riesgo" para un paciente específico. Se guarda como un archivo HTML.
    *   **Gráfico Resumen (Global)**: Un diagrama de barras (`summary_plot`) que muestra la importancia media de cada característica en todas las predicciones del conjunto de datos.

### Salida

Los informes de XAI se guardan en el directorio `reports/xai/`:

*   `force_plot_patient_[ID].html`: Explicación para una predicción individual.
*   `summary_plot_bar.png`: Importancia global de las características.

### Uso

Para generar los informes de explicabilidad, ejecuta:

```bash
python tools/ml_pipelines/explainability.py
```
