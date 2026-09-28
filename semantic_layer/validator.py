# MetricMind Semantic Layer Validator

from semantic_layer.metrics import METRICS
from semantic_layer.dimensions import DIMENSIONS


def validate_metric(metric_name):
    """
    Check whether the requested metric
    is officially defined in the Semantic Layer.
    """

    metric_name = metric_name.lower().strip()

    if metric_name not in METRICS:
        raise ValueError(
            f"Metric '{metric_name}' is not allowed. "
            f"Available metrics: {list(METRICS.keys())}"
        )

    return True


def validate_dimension(dimension_name):
    dimension_name = dimension_name.lower().strip()

    for group in DIMENSIONS.values():
        if dimension_name in group:
            return True

    # Also allow dimensions used directly by the query builder
    allowed_dimensions = {
        "year",
        "quarter",
        "month",
        "date",
        "country",
        "region",
        "segment",
        "product",
        "category",
    }

    if dimension_name in allowed_dimensions:
        return True

    raise ValueError(
        f"Dimension '{dimension_name}' is not allowed."
    )

def validate_dimensions(dimension_names):
    """
    Validate multiple dimensions.
    """

    for dimension in dimension_names:

        validate_dimension(dimension)

    return True