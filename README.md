# Week 2 - Data Version Control (DVC) with Google Cloud Storage

## Overview

This project demonstrates how Data Version Control (DVC) can be integrated with a Machine Learning workflow to efficiently manage datasets using cloud storage. Instead of storing large datasets inside Git, DVC tracks the data while Google Cloud Storage (GCS) stores the actual files.

The project uses the Iris dataset and configures a Google Cloud Storage bucket as the remote storage backend for DVC.

---

## Objective

The objective of this assignment is to:

- Install and configure DVC
- Initialize DVC in the project
- Track the Iris dataset using DVC
- Configure Google Cloud Storage as a remote
- Push dataset versions to GCS
- Verify successful synchronization between the local repository and cloud storage

---

## Project Structure

```
.
├── .dvc/
├── data/
│   ├── iris.csv
│   ├── iris.csv.dvc
│   └── .gitignore
├── train.py
├── inference.py
├── requirements.txt
└── README.md
```

---

## Technologies Used

- Python 3.12
- Git
- DVC 3.67
- Google Cloud Platform
- Google Cloud Storage
- Google Cloud VM (Notebook Instance)

---

## Steps Performed

1. Created a Google Cloud VM / Notebook environment.
2. Installed DVC and verified installation.
3. Initialized DVC inside the repository.
4. Configured a Google Cloud Storage bucket as the DVC remote.
5. Added the Iris dataset using DVC.
6. Pushed the tracked dataset to the configured GCS bucket.
7. Verified synchronization using DVC status commands.

---

## Verification

The following commands were used for verification:

```bash
dvc version
dvc status
dvc remote list
dvc push
gsutil ls gs://23f1001473-iris-week1/week2/dvc-storage/
```

---

## Output

- Dataset tracked by DVC
- Metadata stored in Git
- Actual dataset stored in Google Cloud Storage
- Successful verification of cloud synchronization

---

## Learning Outcomes

Through this assignment I learned:

- How DVC differs from Git.
- Why large datasets should not be stored directly in Git.
- How to configure cloud storage as a DVC remote.
- How DVC tracks datasets using metadata files.
- How to version datasets independently from source code.
