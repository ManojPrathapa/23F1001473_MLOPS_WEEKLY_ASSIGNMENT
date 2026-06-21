import os
import joblib
import pandas as pd

from sklearn.metrics import accuracy_score

# Find latest model folder
artifact_folders = sorted(
    [
        f
        for f in os.listdir("artifacts")
        if os.path.isdir(
            os.path.join(
                "artifacts",
                f
            )
        )
        and f[0].isdigit()
    ]
)

latest_folder = artifact_folders[-1]

model_path = (
    f"artifacts/"
    f"{latest_folder}/"
    f"model.joblib"
)

# Load model
model = joblib.load(model_path)

# Load evaluation set
test = pd.read_csv(
    "artifacts/evaluation.csv"
)

X_test = test[
    [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width"
    ]
]

y_test = test["species"]

# Predict
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"Using model: {latest_folder}"
)

print(
    f"Inference Accuracy: {accuracy:.3f}"
)