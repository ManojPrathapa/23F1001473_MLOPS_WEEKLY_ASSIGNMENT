# 📈 High-Frequency Stock Movement Predictor: End-to-End MLOps Pipeline

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![MLOps](https://img.shields.io/badge/MLOps-DVC%20%7C%20MLflow%20%7C%20Feast-orange)]()
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF.svg?logo=github)]()
[![Cloud](https://img.shields.io/badge/GCP-Cloud%20Storage-4285F4.svg?logo=googlecloud)]()

## 📖 Project Overview
This repository contains a production-grade **Machine Learning Operations (MLOps)** pipeline designed to predict short-term (5-minute) stock price movements using high-frequency trading data. 

While training a machine learning model is relatively straightforward, **operationalizing it is a complex engineering challenge.** This project demonstrates a complete, automated lifecycle: from versioning raw financial data and centralizing feature engineering, to tracking hyperparameter sweeps, registering models, and automating CI/CD evaluations.

---

## 🎯 The Problem Statement
In algorithmic trading, milliseconds matter. Predicting whether a stock's price will increase or decrease in the next 5 minutes requires processing rapid streams of volume and price data. 

However, the core engineering challenge is **reproducibility and safety**. Financial data suffers from rapid *concept drift*. If a model degrades, data scientists must be able to roll back to the exact dataset and feature definitions used months ago. Furthermore, no model should ever be deployed to production without rigorous, automated sanity checks and benchmark evaluations. 

This project solves these challenges by implementing a strict MLOps architecture that removes manual intervention from the model evaluation and deployment lifecycle.

---

## 🌍 Real-World Applications
| Domain | Application |
| :--- | :--- |
| **Algorithmic Trading** | Executing automated, high-frequency buy/sell orders based on 5-minute forecast confidence intervals. |
| **Market Making** | Dynamically adjusting bid-ask spreads in response to anticipated short-term volume surges or drops. |
| **Quantitative Research** | Allowing quants to rapidly test new alpha-generating features against version-controlled historical market snapshots. |
| **Risk Management** | Triggering automated portfolio hedging when consecutive downward 5-minute movements are predicted. |

---

## 🏗️ System Architecture & Data Flow

*(GitHub automatically renders this diagram)*

```mermaid
graph TD
    subgraph 1. Data Layer
        A[Raw Market Data CSV] -->|DVC Tracked| B(GCP Cloud Storage)
        B -->|DVC Pull| C{Feast Feature Store}
        C -->|Materialize| D[SQLite Offline Store]
    end

    subgraph 2. Experimentation Layer
        D -->|Engineered Features| E[Hyperparameter Sweep]
        E -->|Metrics & Params| F[(MLflow Tracking DB)]
        E -->|Best F1 Score| G[(MLflow Model Registry)]
    end

    subgraph 3. CI/CD & Automation Layer
        H[GitHub Push to Main] --> I[GitHub Actions Runner]
        I -->|1. Auth| J[GCP Service Account]
        J -->|2. Pull Data| B
        I -->|3. Train & Log| E
        I -->|4. Evaluate| K[eval_ci.py]
        G -.->|Load v1 Model| K
        K -->|5. Generate Metrics| L[CML Report + Plot]
        L -->|Post Comment| M[GitHub Pull Request / Commit]
    end
🛠️ The MLOps Tech StackData Versioning: Data Version Control (DVC) backed by Google Cloud Storage (GCS).Feature Store: Feast for defining, managing, and serving time-series features consistently.Experiment Tracking & Registry: MLflow (SQLite backend) for parameter logging and artifact management.Model Training: Scikit-Learn (Random Forest Classifier).CI/CD Pipeline: GitHub Actions orchestrated with Continuous Machine Learning (CML) by Iterative.ai.📂 Detailed File StructureFile / DirectoryPurpose & Explanationdata/Contains the raw stock CSV files. Instead of tracking gigabytes of data in Git, this folder is tracked via DVC (data.dvc), mapping files to our remote GCP bucket.feature_repo/features.pyThe Feast configuration. Defines the stock_name entity and Feature Views (e.g., rolling_avg_10, volume_sum_10). Ensures that features used in training are mathematically identical to those used in production serving.train.pyA local script used by data scientists to iterate on the model. It reads the DVC-pinned data, engineers features, and fits a baseline Random Forest model.tune_and_register.pyThe MLflow engine. It conducts a grid search over hyperparameters (like max_depth), logs all experiments to the MLflow tracking server, identifies the highest-performing model, and automatically registers it as stock_movement_predictor.eval_ci.pyThe automated Evaluation Gatekeeper. It fetches the latest model directly from the MLflow Registry, runs strict data sanity tests (ensuring no nulls/negative volumes), evaluates against a holdout test set, and generates a visual bar chart (metrics_plot.png) and Markdown report..github/workflows/ci.ymlThe GitHub Actions Orchestrator. This YAML file defines the CI pipeline. It provisions an Ubuntu runner, authenticates with Google Cloud, pulls DVC data, natively executes the MLflow sweep, triggers the evaluation script, and uses CML to post the results back to GitHub.requirements.txtExplicitly pinned Python dependencies ensuring environment reproducibility across local machines and cloud runners.🚀 How It All Runs Together (End-to-End Execution)The Developer Push: A Data Scientist pushes new feature engineering logic or a new model architecture to the main branch.Environment Provisioning: GitHub Actions detects the push and spins up a clean, isolated Ubuntu container. It sets up Python 3.12 and installs dependencies from requirements.txt.Cloud Authentication & Data Pull: The runner securely authenticates to Google Cloud using a hidden Service Account Key. It then uses dvc pull to download the exact version of the financial datasets associated with the current Git commit.Native Training & Registry: The pipeline executes tune_and_register.py. It runs a hyperparameter sweep, finds the best configuration, and registers the model in a fresh, runner-local MLflow database.Sanity Testing & Evaluation: eval_ci.py takes over. It pulls the newly registered model from MLflow. Before predicting, it runs strict feature assertions (e.g., ensuring rolling averages are strictly positive). It then scores the model on a test set, outputting Accuracy, Precision, Recall, and F1-Score.Automated Reporting: Finally, the CML (Continuous Machine Learning) CLI takes the generated metrics and evaluation plots, formats them into a professional Markdown report, and posts them directly as a comment on the Git commit.Business Impact: The team never has to guess how a model performs. Every single code change results in an auditable, transparent performance report attached directly to the code history.
