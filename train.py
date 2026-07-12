from feast import FeatureStore
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib


def main():
    store = FeatureStore(repo_path=".")

    labels = pd.read_parquet("data/iris_data_adapted_for_feast.parquet")

    entity_df = labels[["iris_id", "event_timestamp"]].copy()
    entity_df["event_timestamp"] = pd.to_datetime(entity_df["event_timestamp"])

    training_df = store.get_historical_features(
        entity_df=entity_df,
        features=[
            "iris_features:sepal_length",
            "iris_features:sepal_width",
            "iris_features:petal_length",
            "iris_features:petal_width",
        ],
    ).to_df()

    training_df = training_df.merge(
        labels[["iris_id", "species"]],
        on="iris_id",
    )

    X = training_df[
        ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    ]
    y = training_df["species"]

    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    pred = model.predict(X)

    print("Accuracy:", accuracy_score(y, pred))

    joblib.dump(model, "iris_model.pkl")


if __name__ == "__main__":
    main()
