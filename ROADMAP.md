# Neurodiagnoses: Roadmap Estratégico

Este documento es la fuente de la verdad para la visión, el estado y la hoja de ruta del proyecto Neurodiagnoses.

## 1. Visión del Proyecto

Crear un ecosistema de IA de código abierto para potenciar la investigación de las enfermedades neurodegenerativas (NDD). El sistema unifica un **motor de diagnóstico "glass-box"** (basado en un marco tridimensional y una base de conocimiento) con **pipelines de ML "black-box"** (para predicción de riesgo y pronóstico), proporcionando una visión de 360 grados del paciente.

---

## 2. Fases del Desarrollo

### ✅ FASE 1: Fundación y Refactorización (Completada)

* **Bifurcación de Repositorios:** Separación del proyecto en un repositorio público (`neurodiagnoses`) y uno privado (`neurodiagnoses-engine`).
* **Creación de la Web Pública:** Despliegue de un sitio web profesional en Astro (`neurodiagnoses.com`).
* **Incidente de Seguridad:** Revocación y purga de una API key expuesta, con implementación de protocolos de seguridad mejorados.
* **Arquitectura de Submódulos:** Creación del proyecto `scikg` y su integración como un submódulo de Git para la generación de conocimiento.

### ✅ FASE 2: Rescate e Integración de Pipelines de ML (Completada)

* **Auditoría Profunda:** Análisis completo del código base para redescubrir funcionalidades "huérfanas".
* **Rescate del Pipeline de Riesgo:** Reparación, refactorización a un módulo (`RiskPredictionEngine`) y validación del pipeline de riesgo genético (PHS).
* **Rescate del Pipeline de Prognosis:** Reparación y validación del pipeline de pronóstico temporal (actualmente "mothballed" a la espera de datos a gran escala).

    - Se ha enriquecido el motor Bayesiano para utilizar evidencia cuantitativa (Odds Ratios) del estudio DIPPA-FTD para diferenciar NDDs de imitadores psiquiátricos.
* **Integración Funcional:** Integración del `RiskPredictionEngine` en el motor principal, enriqueciendo la "Firma Neurodegenerativa" con una evaluación de riesgo.
* **Expansión del Diagnóstico Diferencial:** Evolución del motor y la KB para diferenciar NDDs de sus "grandes imitadores" (ej. autoinmunes) y generar alertas accionables.

### ➡️ FASE 3: Expansión y Puesta en Producción (Sprint Actual)

* **Misión 1: "Operación Océano" Definitiva:** Ejecutar el `knowledge_orchestrator` robustecido para poblar masivamente la Base de Conocimiento.
* **Misión 2: Integración Final en la UI:** Modificar la `app.py` para mostrar los resultados de **riesgo** y **pronóstico** en el informe final.
* **Misión 3: Desarrollo del NKC (`scikg`):** Implementar el pipeline `Dolphin + Ollama` en el repositorio `scikg`.
* **Misión 4: "Laboratorio Visual":** Desarrollar las visualizaciones interactivas para el análisis de cohortes en la UI.
* **Misión 5: Auto-explicabilidad y Trazabilidad Científica (En Progreso):** Poblar continuamente la `explicability_kb.yaml` y asegurar que cada informe generado por el motor incluya una sección de 'Scientific Rationale' que enlace las conclusiones a la evidencia científica fundamental.
* **Misión 6: Motor Probabilístico Avanzado:** Evolucionar el `BayesianEngine` para aceptar no solo evidencia binari