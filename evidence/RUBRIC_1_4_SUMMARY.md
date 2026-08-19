# Rubric Summary: Week 9 Tasks 1 to 5

- **Task 1 (Location Attribute):** Added binary location attribute (0 or 1). Successfully excluded from model features during training.
- **Task 2 (Fairlearn Audit):** Ran Fairlearn `MetricFrame` disaggregated by location group. Confirmed equal opportunity/accuracy across groups.
- **Task 3 (SHAP Analysis):** Generated TreeExplainer SHAP values and exported summary plot for `virginica` to `Screenshots/shap_summary_virginica.png`.
- **Task 4 (Data Drift):** Simulated production drift (+0.8 cm petal offset) and detected statistical drift using 2-sample Kolmogorov-Smirnov tests.
- **Task 5 (Model Card):** Documented model governance, fairness, explainability, and limitations in `MODEL_CARD.md`.
