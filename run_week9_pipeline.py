import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap
from scipy.stats import ks_2samp
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from fairlearn.metrics import MetricFrame

# Set seeds for complete reproducibility
np.random.seed(42)

# ==========================================
# TASK 1: Load Data & Introduce Sensitive Attribute (Location)
# ==========================================
print("=== TASK 1: Introducing Sensitive Attribute 'Location' ===")
iris = load_iris()
feature_names = iris.feature_names
X_df = pd.DataFrame(iris.data, columns=feature_names)
y = iris.target

# Assign random location attribute (0 or 1)
X_df['location'] = np.random.choice([0, 1], size=len(X_df))

# Separate training features (EXCLUDING location) from sensitive attribute
X_features = X_df[feature_names]
sensitive_location = X_df['location']

# Train/Test Split (70/30)
X_train, X_test, y_train, y_test, loc_train, loc_test = train_test_split(
    X_features, y, sensitive_location, test_size=0.3, random_state=42
)

# Train Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print(f"Model trained on 4 clean features: {list(feature_names)}")
print(f"Overall Accuracy: {accuracy_score(y_test, y_pred):.4f}\n")

# ==========================================
# TASK 2: Assess Fairness with Fairlearn MetricFrame
# ==========================================
print("=== TASK 2: Fairlearn Fairness Audit by Location Group ===")
metrics = {
    'accuracy': accuracy_score,
    'precision': lambda y_true, y_pred: precision_score(y_true, y_pred, average='weighted', zero_division=0),
    'recall': lambda y_true, y_pred: recall_score(y_true, y_pred, average='weighted', zero_division=0)
}

mf = MetricFrame(
    metrics=metrics,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=loc_test
)

print("Disaggregated Metrics by Location Group:")
print(mf.by_group)
print("\nOverall Performance across entire Test Set:")
print(mf.overall)

# Save Fairlearn summary to text file
with open('evidence/fairlearn_audit.txt', 'w') as f:
    f.write("Fairlearn MetricFrame Audit Summary\n")
    f.write("===================================\n\n")
    f.write(str(mf.by_group))

# ==========================================
# TASK 3: SHAP Explainability Plots
# ==========================================
print("\n=== TASK 3: Generating SHAP Summary Plots ===")
explainer = shap.TreeExplainer(clf)
shap_values = explainer.shap_values(X_features)

# Generate and save SHAP summary plot for Class 2 (Virginica)
plt.figure(figsize=(10, 6))
# Class 2 is Virginica
shap.summary_plot(
    shap_values[:, :, 2] if len(shap_values.shape) == 3 else shap_values[2], 
    X_features, 
    show=False
)
plt.title("SHAP Summary Plot for Virginica Class (Class 2)")
plt.tight_layout()
plt.savefig("Screenshots/shap_summary_virginica.png", dpi=300)
plt.close()
print("Saved SHAP summary plot to Screenshots/shap_summary_virginica.png")

# ==========================================
# TASK 4: Simulate & Detect Data Drift
# ==========================================
print("\n=== TASK 4: Simulating Production Data Drift & KS-Test ===")
X_production = X_features.copy()
# Shift petal length and petal width distributions to simulate production drift
X_production['petal length (cm)'] += 0.8
X_production['petal width (cm)'] += 0.4

drift_results = {}
print("Kolmogorov-Smirnov Test for Data Drift Detection:")
print("-" * 55)
print(f"{'Feature':<25} | {'p-value':<10} | {'Drift Status'}")
print("-" * 55)

for col in feature_names:
    stat, p_val = ks_2samp(X_features[col], X_production[col])
    is_drift = p_val < 0.05
    status = "DRIFT DETECTED" if is_drift else "No Drift"
    drift_results[col] = (p_val, is_drift)
    print(f"{col:<25} | {p_val:<10.4e} | {status}")

print("-" * 55)

# Save Drift report
with open('evidence/drift_detection_report.txt', 'w') as f:
    f.write("Data Drift Analysis Report (KS-Test)\n")
    f.write("=====================================\n\n")
    for col, (p_val, is_drift) in drift_results.items():
        f.write(f"Feature: {col} | p-value: {p_val:.4e} | Drift: {is_drift}\n")

print("\nWeek 9 Pipeline Execution Complete!")
