from feast import FeatureStore
import pandas as pd
import joblib


def main():
    # Load model
    model = joblib.load("iris_model.pkl")

    # Connect to Feast
    store = FeatureStore(repo_path=".")

    # Retrieve online features
    features = store.get_online_features(
        features=[
            "iris_features:sepal_length",
            "iris_features:sepal_width",
            "iris_features:petal_length",
            "iris_features:petal_width",
        ],
        entity_rows=[
            {"iris_id": 1001},
        ],
    ).to_dict()

    print("\nFeatures Retrieved")
    print(features)

    # Prepare input
    X = pd.DataFrame({
        "sepal_length": features["sepal_length"],
        "sepal_width": features["sepal_width"],
        "petal_length": features["petal_length"],
        "petal_width": features["petal_width"],
    })

    prediction = model.predict(X)

    print("\nPrediction")
    print(prediction[0])


if __name__ == "__main__":
    main()
