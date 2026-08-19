# ⚖️ MLOps Week 9: Explainability, Fairness, and Drift in the IRIS Pipeline

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Fairlearn](https://img.shields.io/badge/Fairness-Fairlearn-8A2BE2)
![SHAP](https://img.shields.io/badge/Explainability-SHAP-00C853)
![Scipy](https://img.shields.io/badge/Stats-SciPy-0054A6?logo=scipy&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Modeling-Scikit--Learn-F7931E?logo=scikit-learn&logoColor=white)

**Author:** Manoj Prathapa  
**Institution:** IIT Madras — BS in Data Science and Applications  
**Repository:** `23F1001473_MLOPS_WEEKLY_ASSIGNMENT`  
**Target Branch:** `week_9`  

---

## 📌 Executive Summary

This repository contains the complete implementation for **Week 9: Explainability, Fairness, and Drift**. 

While previous weeks focused on automation, scaling, and security, a secure model can still be fundamentally untrustworthy if it is biased, opaque, or degrades silently in production. This week establishes the foundation of **Responsible AI** by auditing the IRIS pipeline for demographic fairness, explaining black-box decisions using Game Theory (SHAP), and statistically monitoring feature distributions for production drift.

### Key Milestones Delivered:
1. **Fairness Auditing:** Introduced a sensitive `location` attribute and used `Fairlearn` MetricFrames to prove equitable performance across sub-populations.
2. **Model Explainability:** Generated `SHAP` (SHapley Additive exPlanations) values and summary plots to demystify feature attributions for the `virginica` class.
3. **Data Drift Detection:** Simulated production feature shifts and deployed 2-sample Kolmogorov-Smirnov (KS) statistical tests to successfully trigger drift alerts.
4. **ML Governance:** Authored a formal, production-ready Model Card detailing intended use, limitations, and accountability metrics.

---

## 🔬 Implementation Details

### 1. Fairness Assessment (Fairlearn)
- **Sensitive Attribute:** A `location` feature (0 or 1) was assigned randomly to the dataset.
- **Rule:** Excluded from training to prevent proxy bias; used strictly for post-hoc auditing.
- **Outcome:** The `MetricFrame` revealed identical Accuracy, Precision, and Recall (1.0) across both Location 0 and Location 1, confirming a **0% performance gap**.

### 2. SHAP Explainability (Virginica Class)
- **Explainer Used:** `shap.TreeExplainer`
- **Insights:** The SHAP summary plot (`Screenshots/shap_summary_virginica.png`) proves that high values (red dots) of `petal length` and `petal width` are the dominant forces pushing the model toward predicting the `virginica` class.

### 3. Data Drift Detection (SciPy KS-Test)
- **Simulation:** Added $+0.8$ cm to `petal length` and $+0.4$ cm to `petal width`.
- **Detection Method:** Two-sample Kolmogorov-Smirnov test comparing the original training distribution against the simulated production distribution.
- **Outcome:** Successfully detected statistically significant drift ($p < 0.05$) exclusively in the altered petal features.

---

## 📂 Repository Structure

```text
23F1001473_MLOPS_WEEKLY_ASSIGNMENT/
├── run_week9_pipeline.py         # Unified script for Fairness, SHAP, and Drift
├── MODEL_CARD.md                 # ML Governance Model Card
├── Screenshots/
│   └── shap_summary_virginica.png # SHAP explainability plot
├── evidence/
│   ├── RUBRIC_00_SETUP.md        # Environment setup logs
│   ├── fairlearn_audit.txt       # Disaggregated metric outputs
│   └── drift_detection_report.txt# KS-test p-value results
├── AI_USAGE_DOC.md               # Transparency documentation
├── VIDEO_SCRIPT.md               # Video screencast transcription
└── README.md                     # Project documentation
