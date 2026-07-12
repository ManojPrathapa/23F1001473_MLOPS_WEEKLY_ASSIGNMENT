# MLOps Weekly Assignment – Week 4

# Integrating Continuous Integration (CI) into the IRIS Machine Learning Pipeline

---

# Objective

The objective of this assignment is to integrate Continuous Integration (CI) into the existing IRIS machine learning pipeline using GitHub Actions.

In the previous assignments, DVC was used for dataset and model versioning, and Feast was integrated to ensure training-serving consistency. This assignment extends the pipeline by introducing automated testing and validation.

Every code push and pull request automatically triggers GitHub Actions, which retrieves the latest versioned datasets and models using DVC, executes validation and model evaluation tests using Pytest, and publishes the test results as a Pull Request comment using CML.

This ensures that every change made to the repository is automatically verified before being merged into the main branch.

---

# Problem Statement

As machine learning projects grow larger, manually testing every change becomes difficult and error-prone.

Without Continuous Integration,

- Bugs may reach production.
- Model quality may degrade unnoticed.
- Invalid datasets may be used for training.
- Team collaboration becomes difficult.
- Deployment pipelines become unreliable.

Continuous Integration solves these issues by automatically validating every code change before it is merged into the main branch.

---

# Technology Stack

- Python 3.11
- GitHub Actions
- Pytest
- DVC
- Google Cloud Storage
- Feast
- Scikit-learn
- Pandas
- NumPy
- Joblib
- Google Cloud Vertex AI
- CML (Continuous Machine Learning)
- Git & GitHub

---

# Project Architecture

```
Developer Push / Pull Request
            │
            ▼
      GitHub Actions
            │
            ▼
 Install Python & Dependencies
            │
            ▼
      DVC Pull (GCS Remote)
            │
            ▼
Retrieve Versioned Data & Model
            │
            ▼
 Execute Pytest Test Suite
            │
            ▼
Generate Test Report
            │
            ▼
Publish Report using CML
            │
            ▼
 Merge only after Successful Validation
```

---

# Assignment Tasks

## Task 1

### Data Validation Tests

Created automated Pytest test cases to validate the input dataset.

The tests verify

- Dataset schema
- Missing values
- Feature data types
- Expected feature columns
- Reasonable value ranges

These tests ensure that invalid data cannot enter the training pipeline.

---

## Task 2

### Model Evaluation Tests

Created automated tests that

- Load the trained Random Forest model
- Run inference on the evaluation dataset
- Calculate model performance
- Verify that accuracy remains above the required threshold

If model quality degrades, the CI pipeline automatically fails.

---

## Task 3

### Configure GitHub Actions

Created a GitHub Actions workflow that automatically

- Checks out the repository
- Installs project dependencies
- Pulls datasets and models using DVC
- Executes the Pytest suite
- Generates a test report

This workflow executes entirely inside GitHub's hosted runner.

---

## Task 4

### Enable CI on Every Push & Pull Request

Configured GitHub Actions to automatically execute on

- Every Push
- Every Pull Request

This guarantees that every code modification is tested before merging.

---

## Task 5

### Integrate CML

Configured CML to automatically generate a test report after every successful test execution.

The report includes

- Test execution summary
- Pass/Fail status
- Model evaluation metrics

The generated report is automatically posted as a Pull Request comment.

---

## Task 6

### Pull Request Workflow

Created a feature branch for Week 4.

Implemented the CI pipeline.

Pushed the changes to GitHub.

Created a Pull Request.

Verified that GitHub Actions executed successfully.

Reviewed the automatically generated CML report.

Merged the Pull Request into the main branch.

---

# Repository Structure

```
.github/
    workflows/
        ci.yml

tests/
    test_data_validation.py
    test_model.py

src/

models/

data/

requirements.txt

README.md

dvc.yaml

feature_store.yaml
```

---

# GitHub Actions Workflow

The CI pipeline performs the following steps automatically.

1. Checkout Repository

2. Setup Python Environment

3. Install Dependencies

4. Pull Versioned Data using DVC

5. Execute Pytest Tests

6. Generate Test Report

7. Publish Pull Request Comment using CML

---

# Testing Workflow

```
Developer Push
      │
      ▼
GitHub Actions Triggered
      │
      ▼
Install Dependencies
      │
      ▼
DVC Pull
      │
      ▼
Run Data Validation Tests
      │
      ▼
Run Model Evaluation Tests
      │
      ▼
Generate Report
      │
      ▼
Publish CML Comment
```

---

# Results

✔ GitHub Actions Successfully Configured

✔ Automatic CI Trigger on Every Push

✔ Automatic CI Trigger on Every Pull Request

✔ DVC Successfully Pulled Versioned Data

✔ Data Validation Tests Passed

✔ Model Evaluation Tests Passed

✔ Test Report Generated

✔ CML Successfully Posted Pull Request Comment

✔ Pull Request Successfully Merged into Main

---

# Challenges Faced

### Dependency Conflicts

Initially multiple package version conflicts occurred between Feast, Pandas and Python.

**Solution**

Pinned compatible dependency versions and migrated the workflow to Python 3.11.

---

### CML Installation Issue

The PyPI version of CML depended on deprecated packages.

**Solution**

Installed CML using the official `iterative/setup-cml` GitHub Action.

---

### DVC Compatibility Error

Encountered a PathSpec compatibility issue while running `dvc pull`.

**Solution**

Updated DVC and installed compatible dependency versions.

---

### GitHub Actions Permissions

Initially CML could not publish Pull Request comments because of insufficient workflow permissions.

**Solution**

Granted `pull-requests: write` and `issues: write` permissions in the workflow and enabled repository workflow write permissions.

---

# Learning Outcomes

Through this assignment I learned

- Continuous Integration fundamentals
- GitHub Actions workflow creation
- Automated ML testing using Pytest
- DVC integration inside CI pipelines
- Pull Request automation using CML
- GitHub workflow permissions
- Dependency management in CI
- Debugging GitHub Actions
- Production-ready MLOps pipeline design

---

# Conclusion

This assignment demonstrates the successful integration of Continuous Integration into the IRIS machine learning pipeline. GitHub Actions automatically validates every code change by retrieving versioned datasets and models through DVC, executing automated tests using Pytest, and publishing results through CML. The completed workflow ensures reliable model quality, improves collaboration, and reflects modern MLOps practices used in production environments.
