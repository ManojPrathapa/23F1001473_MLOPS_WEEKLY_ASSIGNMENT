# Week 1 - IRIS Classification Pipeline using Vertex AI

## Objective

Build an end-to-end machine learning pipeline on Google Cloud Platform using Vertex AI Workbench and Google Cloud Storage.

The pipeline performs:

1. Data loading
2. Train-test split
3. Model training
4. Model evaluation
5. Artifact generation
6. Inference using trained model
7. Storage of artifacts in GCS

---

## Files Included

### data/iris.csv

Input dataset used for training and evaluation.

### train.py

Training script that:

* Loads IRIS dataset
* Splits data into train and test sets
* Trains a Decision Tree Classifier
* Evaluates model accuracy
* Stores model artifacts in timestamped folders

### inference.py

Inference script that:

* Loads latest trained model
* Loads evaluation dataset
* Performs prediction
* Computes inference accuracy

### requirements.txt

Python package dependencies required for execution.

### README.md

Project documentation and explanation of repository contents.

---

## GCP Components Used

* Vertex AI Workbench
* Google Cloud Storage (GCS)

---

## Output Artifacts

Output artifacts are stored in Google Cloud Storage.

Example:

20260621_054947/model.joblib

20260621_055126/model.joblib

Each execution creates a separate timestamped artifact folder.

---

## Results

Decision Tree Classifier achieved approximately 98.3% accuracy on the evaluation dataset.

---

## Author

23F1001473
MLOps Week 1 Assignment
