# MLOps Weekly Assignment – Week 3
## Integrating Feast Feature Store into the IRIS Machine Learning Pipeline

**Student:** YOUR NAME

**Roll Number:** YOUR IITM BS ROLL NUMBER

**Course:** MLOps

**Platform Used:** Google Cloud Platform (Workbench VM)

**Branch:** week_3

---

# Objective

The objective of this assignment is to integrate the Feast Feature Store into an existing IRIS machine learning pipeline.

Unlike the previous assignment where DVC was used to version datasets and models, Feast is introduced to solve the training-serving consistency problem by ensuring that both training and inference use exactly the same engineered features.

The pipeline retrieves historical features from the offline store during training and retrieves real-time features from the online store during inference.

---

# Problem Statement

In production ML systems, feature engineering is often implemented separately for training and inference.

This causes Training-Serving Skew.

Examples include:

- Different preprocessing logic
- Missing feature transformations
- Different feature versions
- Data inconsistencies

Feast solves this issue by acting as a centralized feature repository.

---

# Technology Stack

- Python
- Feast 0.64
- SQLite
- Pandas
- Scikit-learn
- NumPy
- PyArrow
- Google Cloud Platform
- Git
- GitHub

---

# Project Architecture

Raw IRIS Dataset
        │
        ▼
Feature Definitions
(Entity + FileSource + FeatureView)
        │
        ▼
Feast Registry
        │
        ▼
Offline Store (Parquet)
        │
        ├──────────────► Model Training
        │
        ▼
Materialization
        │
        ▼
SQLite Online Store
        │
        ▼
Inference
        │
        ▼
Prediction

---

# Assignment Tasks

## Task 1

Initialized a Feast Feature Repository.

Configured

- feature_store.yaml
- SQLite Online Store
- Local Registry

---

## Task 2

Defined

Entity

```
iris
```

Join Key

```
iris_id
```

Created FileSource

```
iris_data_adapted_for_feast.parquet
```

Created Feature View

Features

- sepal_length
- sepal_width
- petal_length
- petal_width

---

## Task 3

Applied the feature definitions.

```
feast apply
```

Materialized features into SQLite

```
feast materialize
```

Verified

- Registry created
- Online Store created
- Feature View registered

---

## Task 4

Historical feature retrieval.

Training data is fetched using

```
store.get_historical_features()
```

instead of directly reading feature columns from CSV.

The retrieved features were used to train a Random Forest classifier.

Training Accuracy

```
1.0
```

Model saved as

```
iris_model.pkl
```

---

## Task 5

Online inference.

Features were retrieved using

```
store.get_online_features()
```

The returned features were passed to the trained model.

Prediction

```
versicolor
```

The prediction exactly matched the original dataset label.

---

# Repository Structure

```
iris_feature_repo/

feature_store.yaml

feature_definitions.py

train.py

inference.py

data/

iris_data_adapted_for_feast.csv

iris_data_adapted_for_feast.parquet
```

---

# Important Feast Components

## Entity

Represents the primary key.

```
iris_id
```

---

## File Source

Reads historical feature data from Parquet.

---

## Feature View

Defines

- feature schema
- source
- entity
- TTL

---

## Offline Store

Used for

- Training
- Historical feature retrieval

---

## Online Store

SQLite

Used for

- Low latency inference

---

# Workflow

1. Create Feature Repository

↓

2. Define Entity

↓

3. Define Data Source

↓

4. Create Feature View

↓

5. Apply Definitions

↓

6. Materialize Features

↓

7. Train Model

↓

8. Fetch Online Features

↓

9. Predict

---

# Results

✔ Feast Repository Created

✔ Feature Definitions Registered

✔ SQLite Online Store Created

✔ Historical Features Retrieved

✔ Model Trained Successfully

✔ Accuracy = 100%

✔ Online Feature Retrieval Successful

✔ Real-time Prediction Successful

---

# Challenges Faced

## CSV Compatibility

Initially Feast attempted to interpret the CSV as a Parquet dataset.

Solution

Converted the dataset to Parquet using Pandas.

---

## Timestamp Format

The timestamp columns were stored as strings.

Solution

Converted

event_timestamp

and

created_timestamp

to datetime before writing the Parquet file.

---

## Materialization Error

Received

AttributeError

```
'str' object has no attribute tzinfo
```

Solution

Converted timestamp columns into datetime objects before materialization.

---

# Learning Outcomes

Through this assignment I learned

- Importance of Feature Stores
- Difference between Offline and Online Stores
- Feast Repository Structure
- Feature Materialization
- Historical Feature Retrieval
- Online Feature Retrieval
- Training Serving Consistency
- Production ML Pipeline Design

---

# Conclusion

This assignment demonstrates the integration of Feast into an ML workflow using the IRIS dataset. Feature engineering is centralized inside Feast, ensuring consistent feature computation during both model training and inference. This architecture reduces training-serving skew and reflects best practices used in production machine learning systems.