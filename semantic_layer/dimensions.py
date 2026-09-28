# MetricMind Governed Dimensions


DIMENSIONS = {

    "time": {
        "year": {
            "name": "Year",
            "sql_expression": "EXTRACT(YEAR FROM o.order_date)"
        },

        "quarter": {
            "name": "Quarter",
            "sql_expression": (
                "EXTRACT(QUARTER FROM o.order_date)"
            )
        },

        "month": {
            "name": "Month",
            "sql_expression": (
                "EXTRACT(MONTH FROM o.order_date)"
            )
        },

        "date": {
            "name": "Date",
            "sql_expression": "o.order_date"
        }
    },


    "geography": {

        "country": {
            "name": "Country",
            "sql_expression": "c.country"
        },

        "region": {
            "name": "Region",
            "sql_expression": "c.region"
        }
    },


    "customer": {

        "segment": {
            "name": "Customer Segment",
            "sql_expression": "c.customer_segment"
        }
    },


    "product": {

        "name": "Product",
        "sql_expression": "p.product_name"
    },


    "category": {

        "name": "Category",
        "sql_expression": "p.category"
    }
}


def get_dimension(dimension_group, dimension_name):

    if dimension_group not in DIMENSIONS:
        raise ValueError(
            f"Unknown dimension group: {dimension_group}"
        )

    group = DIMENSIONS[dimension_group]

    if dimension_name not in group:
        raise ValueError(
            f"Unknown dimension: {dimension_name}"
        )

    return group[dimension_name]


def list_dimension_groups():

    return list(DIMENSIONS.keys())