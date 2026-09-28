# MetricMind Governed Metrics


METRICS = {

    "revenue": {
        "name": "Revenue",
        "description": "Total sales revenue",
        "formula": "SUM(orders.revenue)",
        "sql_expression": "SUM(o.revenue)"
    },

    "material_cost": {
        "name": "Material Cost",
        "description": "Total material cost",
        "formula": "SUM(expenses.material_cost)",
        "sql_expression": "SUM(e.material_cost)"
    },

    "shipping_cost": {
        "name": "Shipping Cost",
        "description": "Total shipping cost",
        "formula": "SUM(expenses.shipping_cost)",
        "sql_expression": "SUM(e.shipping_cost)"
    },

    "other_cost": {
        "name": "Other Cost",
        "description": "Total other operating costs",
        "formula": "SUM(expenses.other_cost)",
        "sql_expression": "SUM(e.other_cost)"
    },

    "total_cost": {
        "name": "Total Cost",
        "description": "Material + Shipping + Other Cost",
        "formula": "Material Cost + Shipping Cost + Other Cost",
        "sql_expression": (
            "SUM(e.material_cost + "
            "e.shipping_cost + "
            "e.other_cost)"
        )
    },

    "profit": {
        "name": "Profit",
        "description": "Revenue minus Total Cost",
        "formula": "Revenue - Total Cost",
        "sql_expression": (
            "SUM(o.revenue) - "
            "SUM(e.material_cost + "
            "e.shipping_cost + "
            "e.other_cost)"
        )
    },

    "margin": {
        "name": "Margin",
        "description": "Profit as percentage of Revenue",
        "formula": "(Profit / Revenue) × 100",
        "sql_expression": (
            "(SUM(o.revenue) - "
            "SUM(e.material_cost + "
            "e.shipping_cost + "
            "e.other_cost)) "
            "/ NULLIF(SUM(o.revenue), 0) * 100"
        )
    }
}


def get_metric(metric_name):

    metric_name = metric_name.lower()

    if metric_name not in METRICS:
        raise ValueError(
            f"Unknown metric: {metric_name}"
        )

    return METRICS[metric_name]


def list_metrics():

    return list(METRICS.keys())