import os
from datetime import datetime

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


# Load dataset
data = pd.read_csv("data/iris.csv")

# Train-test split
train, test = train_test_split(
    data,
    test_size=0.4,
    stratify=data["species"],
    random_state=42
)

# Save evaluation set for inference
os.makedirs("artifacts", exist_ok=True)
test.to_csv("artifacts/evaluation.csv", index=False)

# Features and labels
X_train = train[
    [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width"
    ]
]

y_train = train["species"]

X_test = test[
    [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width"
    ]
]

y_test = test["species"]

# Train model
model = DecisionTreeClassifier(
    max_depth=3,
    random_state=1
)

model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"Accuracy: {accuracy:.3f}")

# Timestamp folder
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

artifact_dir = f"artifacts/{timestamp}"

os.makedirs(
    artifact_dir,
    exist_ok=True
)

# Save model
joblib.dump(
    model,
    f"{artifact_dir}/model.joblib"
)

print(
    f"Model saved in {artifact_dir}"
)