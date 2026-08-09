# 🛡️ MLOps Week 8: Integrating MLSecOps into the IRIS Pipeline

![MLflow](https://img.shields.io/badge/Tracking-MLflow-0194E2?logo=mlflow&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Modeling-Scikit--Learn-F7931E?logo=scikit-learn&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![GCP](https://img.shields.io/badge/Google%20Cloud-Cloud%20Shell-4285F4?logo=googlecloud&logoColor=white)
![Security](https://img.shields.io/badge/Security-MLSecOps-red)

**Author:** Manoj Prathapa ([@ManojPrathapa](https://github.com/ManojPrathapa))  
**Institution:** IIT Madras — BS in Data Science and Applications (Class of 2026)  
**Repository:** `23F1001473_MLOPS_WEEKLY_ASSIGNMENT`  
**Target Branch:** `week_8`  

---

## 📌 Executive Summary

This repository contains the implementation for **Week 8: MLSecOps and Data Poisoning**. 

Traditional MLOps pipelines ensure reliability and scalability but often lack defenses against intentional adversarial manipulation. This project integrates security thinking into the ML lifecycle by simulating a **Data Poisoning Attack** on the IRIS dataset. We inject severe, out-of-distribution noise and randomized labels at varying corruption levels, evaluating the degradation of the model's decision boundaries using **MLflow**.

### Key Milestones Delivered:
1. **Threat Vector Analysis:** Outlined primary ML vulnerabilities including Data Poisoning, Adversarial Examples, Model Extraction, and Prompt Injection.
2. **Data Poisoning Simulation:** Programmatically injected 0%, 5%, 10%, and 50% feature and label noise into the IRIS training set.
3. **Experiment Tracking:** Automated the tracking of Accuracy, Precision, Recall, and F1 Scores across all corruption levels using a local MLflow SQLite backend.
4. **Resilience & Bottleneck Analysis:** Analyzed how `DecisionTreeClassifier` handles low-level noise (5-10%) via orthogonal leaf isolation and when it critically degrades (50%).
5. **Mitigation Engineering:** Formulated production-grade mitigation strategies emphasizing Data Quality Gates and statistical anomaly detection.

---

## 🦠 ML Security Threat Vectors

Understanding the attack surface is the first step in MLSecOps. Threats can target any stage of the pipeline:

| Threat Vector | Target Stage | Description | Real-World Example |
| :--- | :--- | :--- | :--- |
| **Data Poisoning** | Data Ingestion / Training | Injecting corrupted samples or false labels to degrade accuracy or embed backdoors. | Submitting millions of mislabeled "not spam" emails to retrain an email filter. |
| **Adversarial Examples** | Inference / API | Applying subtle, calculated perturbations to inputs to force misclassification. | Placing specific stickers on a stop sign so computer vision models read "Speed Limit 45". |
| **Model Extraction** | Deployment | Repeatedly querying a live prediction endpoint to reverse-engineer model weights. | Stealing proprietary pricing algorithms by systematically pinging a competitor's API. |
| **Prompt Injection** | LLM Interface | Embedding malicious instructions in user inputs to override system constraints. | Hiding text in a resume instructing an AI screener to bypass all checks and "Hire immediately". |

---

## 🔬 Data Poisoning Simulation & Results

### Methodology
To simulate an attack, the `run_mlsecops_poisoning.py` script targets the training dataset. At a specified corruption rate $r \in \{0.0, 0.05, 0.10, 0.50\}$, it selects random indices and overwrites all feature values with uniform random noise between `0.0` and `10.0`, assigning a random target label. The test set remains strictly pristine to measure real-world impact.

### MLflow Validation Outcomes

| Poison % | Accuracy | F1 Score | MLflow Run Name | Observation |
| :---: | :---: | :---: | :--- | :--- |
| **0%** | `1.0000` | `1.0000` | `Poisoning_Level_0%` | Baseline clean performance. |
| **5%** | `1.0000` | `1.0000` | `Poisoning_Level_5%` | Model isolates the random noise into deep leaf nodes. |
| **10%** | `1.0000` | `1.0000` | `Poisoning_Level_10%`| Signal remains strong enough to maintain core decision boundaries. |
| **50%** | `0.9556` | `0.9553` | `Poisoning_Level_50%`| Noticeable degradation; noise overpowers the signal, warping boundaries. |

*Note: Metrics logged locally via MLflow (`mlflow.db`).*

---

## 🛡️ Production Mitigation Strategies

If half of your training data is maliciously altered, simply "collecting more data" does not restore performance—it amplifies the poisoned volume. **Data Quality strictly outweighs Data Quantity.**

To secure the pipeline in production:
1. **Data Quality Gates:** Use tools like *Great Expectations* to enforce strict schema validation and biological bounding constraints (e.g., Reject Sepal Length > 10).
2. **Anomaly Detection:** Apply unsupervised clustering (e.g., Isolation Forests) during the ELT phase to quarantine batches showing severe divergence from historical distributions.
3. **Data Provenance:** Utilize DVC lineage tracking to audit the origin and authorization of incoming training batches.

---

## 📂 Repository Structure

```text
23F1001473_MLOPS_WEEKLY_ASSIGNMENT/
├── run_mlsecops_poisoning.py     # Data poisoning simulation and MLflow tracking script
├── mlflow.db                     # Local SQLite MLflow tracking database
├── mlartifacts/                  # Local MLflow artifact storage
├── evidence/
│   ├── RUBRIC_00_SETUP.md        # Environment setup documentation
│   └── RUBRIC_2_3_POISONING.md   # Execution tracking and results
├── AI_USAGE_DOC.md               # Mandatory AI tool usage transparency documentation
├── VIDEO_SCRIPT.md               # 15-minute complete screencast transcription
└── README.md                     # Project documentation

```

---

## 💻 Quick Start & Reproducibility

### 1. Run the Poisoning Simulation

```bash
# Install dependencies
pip install mlflow scikit-learn pandas numpy

# Execute the simulation script
python3 run_mlsecops_poisoning.py

```

### 2. View Metrics in MLflow

```bash
# Start the MLflow UI
python3 -m mlflow ui --host 0.0.0.0 --port 5000

```

Navigate to `http://localhost:5000` (or your Web Preview port) to view the `MLSecOps_Data_Poisoning` experiment.
