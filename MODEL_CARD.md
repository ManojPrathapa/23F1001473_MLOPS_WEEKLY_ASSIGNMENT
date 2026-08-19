# Model Card: IRIS Decision Tree Classifier

## Model Details
- **Model Name:** IRIS Flower Species Classifier
- **Model Type:** Decision Tree Classifier (`max_depth=None`, `random_state=42`)
- **Version:** 1.0.0
- **Framework:** Scikit-Learn

## Intended Use
- **Primary Use Case:** Automated classification of Iris flower species into `setosa`, `versicolor`, or `virginica`.
- **Target Audience:** Botanical researchers and automated agricultural classification pipelines.
- **Out-of-Scope Uses:** Non-Iris flora species, heavily degraded or corrupted measurement data.

## Training Data
- **Dataset:** Fisher's Iris Dataset (150 total samples, 4 continuous features).
- **Features Used:**
  1. `sepal length (cm)`
  2. `sepal width (cm)`
  3. `petal length (cm)`
  4. `petal width (cm)`
- **Train/Test Split:** 70% Train (105 samples) / 30% Test (45 samples).

## Fairness Considerations & Disaggregated Metrics
- **Sensitive Attribute:** `location` (Binary group indicator: 0 or 1).
- **Inclusion Strategy:** Excluded from training features to prevent proxy bias; used exclusively for auditing via Fairlearn `MetricFrame`.
- **Fairness Audit Results:**
  - **Location 0:** Accuracy ~1.00, Precision ~1.00, Recall ~1.00
  - **Location 1:** Accuracy ~1.00, Precision ~1.00, Recall ~1.00
  - **Fairness Assessment:** Equal performance across subgroups with near-zero performance gap.

## Explainability (SHAP Insights)
- **Top Predictive Features for `virginica`:** `petal length (cm)` and `petal width (cm)`.
- **Feature Attribution:** High feature values (red dots) for petal measurements strongly push the model toward predicting `virginica` (positive SHAP values).

## Known Limitations & Drift Risks
- **Data Drift Vulnerability:** Sensitive to distribution shifts in petal dimensions. Kolmogorov-Smirnov test flags drift if petal length shifts by >0.5 cm.
- **Concept Drift:** Requires re-auditing if environmental factors change physical flower growth ratios over time.
