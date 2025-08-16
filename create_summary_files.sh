SUMMARIES_DIR="data/ingested_knowledge/summaries"
mkdir -p "$SUMMARIES_DIR"

# Resumen Eje 1 (Genética)
cat <<'EOF' > "${SUMMARIES_DIR}/genetics_APOE_summary.md"
APOE is the most significant genetic risk factor for late-onset Alzheimer's disease (AD). A landmark meta-analysis (Farrer et al., 1997, JAMA) established clear risk profiles. For individuals with one copy of the ε4 allele (genotype ε3/ε4), the odds ratio for AD is approximately 3.2 (95% CI: 2.8–3.8). For homozygous carriers (genotype ε4/ε4), the odds ratio skyrockets to 14.9 (95% CI: 10.8–20.6).
EOF

# Resumen Eje 3 (Fenotipo Clínico)
cat <<'EOF' > "${SUMMARIES_DIR}/criteria_NINCDS_ADRDA_summary.md"
The 1984 NINCDS-ADRDA criteria are a cornerstone for the clinical diagnosis of Alzheimer's disease (AD). A large meta-analysis assessing their diagnostic accuracy against neuropathological confirmation found a pooled sensitivity of 0.81 (95% CI: 0.75–0.86) and a pooled specificity of 0.70 (95% CI: 0.65–0.74) for probable AD.
EOF

echo "PASO 1 COMPLETADO: Fuentes de conocimiento listas."