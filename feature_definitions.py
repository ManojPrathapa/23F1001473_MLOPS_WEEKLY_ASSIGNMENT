from datetime import timedelta

from feast import Entity
from feast import FeatureView
from feast import Field
from feast import FileSource

from feast.types import Float32, Int64


# -----------------------------
# Entity
# -----------------------------

iris = Entity(
    name="iris",
    join_keys=["iris_id"],
)

# -----------------------------
# Data Source
# -----------------------------

iris_source = FileSource(
    path="data/iris_data_adapted_for_feast.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# -----------------------------
# Feature View
# -----------------------------

iris_features = FeatureView(
    name="iris_features",

    entities=[iris],

    ttl=timedelta(days=365),

    schema=[
        Field(name="sepal_length", dtype=Float32),
        Field(name="sepal_width", dtype=Float32),
        Field(name="petal_length", dtype=Float32),
        Field(name="petal_width", dtype=Float32),
    ],

    source=iris_source,

    online=True,
)
