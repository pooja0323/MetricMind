# MetricMind Semantic Query Builder

from semantic_layer.metrics import METRICS
from semantic_layer.validator import (
    validate_metric,
    validate_dimensions,
)


DIMENSION_SQL = {
    "year": "EXTRACT(YEAR FROM o.order_date)",
    "quarter": "EXTRACT(QUARTER FROM o.order_date)",
    "month": "EXTRACT(MONTH FROM o.order_date)",
    "date": "o.order_date",
    "country": "c.country",
    "region": "c.region",
    "segment": "c.customer_segment",
    "product": "p.product_name",
    "category": "p.category",
}


def build_query(
    metric,
    dimensions=None,
    region=None,
    country=None,
    category=None,
    start_date=None,
    end_date=None,
):

    if dimensions is None:
        dimensions = []

    validate_metric(metric)
    validate_dimensions(dimensions)

    metric_sql = METRICS[metric]["sql_expression"]

    select_parts = []

    for dimension in dimensions:

        dimension_sql = DIMENSION_SQL.get(dimension)

        if dimension_sql is None:
            raise ValueError(
                f"Unsupported dimension: {dimension}"
            )

        select_parts.append(
            f"{dimension_sql} AS {dimension}"
        )

    select_parts.append(
        f"{metric_sql} AS {metric}"
    )

    select_clause = ",\n        ".join(select_parts)

    sql = f"""
SELECT
        {select_clause}

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

JOIN products p
    ON o.product_id = p.product_id

JOIN expenses e
    ON o.order_id = e.order_id
"""

    conditions = []

    if region:
        conditions.append(
            f"c.region = '{region}'"
        )

    if country:
        conditions.append(
            f"c.country = '{country}'"
        )

    if category:
        conditions.append(
            f"p.category = '{category}'"
        )

    if start_date:
        conditions.append(
            f"o.order_date >= '{start_date}'"
        )

    if end_date:
        conditions.append(
            f"o.order_date <= '{end_date}'"
        )

    if conditions:

        sql += "\nWHERE\n        "

        sql += "\n        AND ".join(conditions)

    if dimensions:

        group_by_parts = []

        for dimension in dimensions:

            group_by_parts.append(
                DIMENSION_SQL[dimension]
            )

        sql += "\n\nGROUP BY\n        "

        sql += ",\n        ".join(
            group_by_parts
        )

    if dimensions:

        sql += "\n\nORDER BY\n        "

        sql += ", ".join(
            DIMENSION_SQL[d]
            for d in dimensions
        )

    return sql.strip()