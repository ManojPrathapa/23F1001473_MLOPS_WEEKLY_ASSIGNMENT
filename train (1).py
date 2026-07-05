from feast import FeatureStore
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# ----------------------------------------
# Connect to Feast
# ----------------------------------------

store = FeatureStore(repo_path=".")

# ----------------------------------------
# Read labels from original dataset
# ----------------------------------------

labels = pd.read_csv("data/iris_data_adapted_for_feast.csv")

entity_df = labels[["iris_id", "event_timestamp"]].copy()

entity_df["event_timestamp"] = pd.to_datetime(entity_df["event_timestamp"])

# ----------------------------------------
# Retrieve historical features from Feast
# ----------------------------------------

training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "iris_features:sepal_length",
        "iris_features:sepal_width",
        "iris_features:petal_length",
        "iris_features:petal_width",
    ],
).to_df()

# ----------------------------------------
# Join labels
# ----------------------------------------

training_df = training_df.merge(
    labels[["iris_id", "species"]],
    on="iris_id",
)

print("\nTraining Data")
print(training_df.head())

# ----------------------------------------
# Train Model
# ----------------------------------------

X = training_df[
    [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
    ]
]

y = training_df["species"]

model = RandomForestClassifier(random_state=42)

model.fit(X, y)

pred = model.predict(X)

acc = accuracy_score(y, pred)

print("\nTraining Accuracy:", acc)

# ----------------------------------------
# Save Model
# ----------------------------------------

joblib.dump(model, "iris_model.pkl")

print("\nModel saved as iris_model.pkl")
