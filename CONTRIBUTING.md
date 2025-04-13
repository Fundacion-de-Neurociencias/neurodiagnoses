
# Contributing Guidelines

Thank you for contributing to this repository! To ensure consistency and best practices across the team, please follow these conventions when working with notebooks and scripts.

## 📒 When to Use Notebooks (Jupyter, Colab)

Use notebooks in the following cases:

- **Exploratory Data Analysis (EDA)**: Initial inspection of datasets, missing values, distributions, correlations.
- **Visualization and Communication**: Interactive plots, tables, summaries for discussion with clinical or non-technical stakeholders.
- **Rapid Prototyping**: Testing models quickly (e.g., `sklearn`, XGBoost) without production-ready code.
- **Visual Documentation**: Show reasoning behind hypotheses and initial decisions.

**Notebook Best Practices:**
- Start each notebook with a clear title, dataset description, and version.
- Clear outputs before committing to the repo.
- Save notebooks under: `/notebooks`

---

## 🧱 When to Use Scripts and Modular Code

Use structured Python scripts when:

- Code is **reusable**, **scheduled**, or part of a **pipeline**.
- You're training, saving, or evaluating models for **production**.
- You need version control, reproducibility, or integration (e.g., via API).
- You're automating repeated tasks (e.g., MRI preprocessing, biomarker extraction).

**Recommended structure:**

```
/src
  ├── data/
  ├── features/
  ├── models/
  ├── pipelines/
  └── utils/
```

Use tools like `MLflow`, `DVC`, or `W&B` to track experiments.

---

## 🔄 Combining Both Approaches

- Notebooks may **call functions** from `/src/` to visualize outputs interactively.
- Use **notebooks to explore and communicate**, and **scripts to formalize and maintain**.

---

## ✅ Quick Summary

| Task                             | Notebook ✅ | Script ✅ |
|----------------------------------|-------------|-----------|
| Exploratory data analysis        | Yes         | No        |
| Initial modeling experiments     | Yes         | No        |
| Data preprocessing & pipelines   | No          | Yes       |
| Final model training & tracking  | No          | Yes       |
| Scheduled/automated workflows    | No          | Yes       |
| Clinical dashboards/reporting    | Yes         | Yes (API) |

---

Thank you for keeping the project clean, maintainable and collaborative!
