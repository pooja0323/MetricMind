# MetricMind AI Agent

import requests


API_URL = "http://127.0.0.1:8000/semantic-query"


# ============================================================
# Helper: Call Semantic Layer API
# ============================================================

def call_semantic_api(params):

    try:

        response = requests.get(
            API_URL,
            params=params,
            timeout=10
        )

        if response.status_code != 200:

            return {
                "error": "Semantic API request failed.",
                "status_code": response.status_code
            }

        return response.json()

    except requests.exceptions.RequestException as e:

        return {
            "error": "Could not connect to MetricMind backend.",
            "details": str(e)
        }


# ============================================================
# Europe Margin Analysis
# ============================================================

def analyze_europe_margin():

    # Get Europe quarterly margin data
    result = call_semantic_api({
        "metric": "margin",
        "dimensions": "year,quarter",
        "region": "Europe"
    })

    if "error" in result:
        return result

    margin_data = result["data"]

    previous = None
    latest = None

    # Find 2026 Q2 and Q3
    for row in margin_data:

        if (
            int(row["year"]) == 2026
            and int(row["quarter"]) == 2
        ):
            previous = row

        if (
            int(row["year"]) == 2026
            and int(row["quarter"]) == 3
        ):
            latest = row

    if previous is None or latest is None:

        return {
            "error": "Required 2026 Q2 and Q3 data not found."
        }

    previous_margin = float(previous["margin"])
    latest_margin = float(latest["margin"])

    margin_change = latest_margin - previous_margin


    # ========================================================
    # Get Cost Driver Data
    # ========================================================

    metrics = {}

    for metric_name in [
        "revenue",
        "material_cost",
        "shipping_cost",
        "other_cost"
    ]:

        result = call_semantic_api({
            "metric": metric_name,
            "dimensions": "year,quarter",
            "region": "Europe",
            "start_date": "2026-04-01",
            "end_date": "2026-09-30"
        })

        if "error" in result:
            return result

        metrics[metric_name] = result["data"]


    # ========================================================
    # Extract Q2 and Q3 values
    # ========================================================

    driver_values = {}

    for metric_name, rows in metrics.items():

        q2_value = None
        q3_value = None

        for row in rows:

            if (
                int(row["year"]) == 2026
                and int(row["quarter"]) == 2
            ):
                q2_value = float(row[metric_name])

            if (
                int(row["year"]) == 2026
                and int(row["quarter"]) == 3
            ):
                q3_value = float(row[metric_name])

        if q2_value is None or q3_value is None:

            return {
                "error": f"Missing Q2/Q3 data for {metric_name}."
            }

        driver_values[metric_name] = {
            "q2": q2_value,
            "q3": q3_value,
            "change": q3_value - q2_value
        }


    # ========================================================
    # Calculate Total Cost
    # ========================================================

    q2_total_cost = (
        driver_values["material_cost"]["q2"]
        + driver_values["shipping_cost"]["q2"]
        + driver_values["other_cost"]["q2"]
    )

    q3_total_cost = (
        driver_values["material_cost"]["q3"]
        + driver_values["shipping_cost"]["q3"]
        + driver_values["other_cost"]["q3"]
    )


    # ========================================================
    # Calculate Profit
    # ========================================================

    q2_profit = (
        driver_values["revenue"]["q2"]
        - q2_total_cost
    )

    q3_profit = (
        driver_values["revenue"]["q3"]
        - q3_total_cost
    )


    # ========================================================
    # Find Largest Cost Increase
    # ========================================================

    cost_changes = {
        "material_cost":
            driver_values["material_cost"]["change"],

        "shipping_cost":
            driver_values["shipping_cost"]["change"],

        "other_cost":
            driver_values["other_cost"]["change"]
    }

    largest_cost_driver = max(
        cost_changes,
        key=cost_changes.get
    )


    driver_names = {

        "material_cost":
            "Material Cost",

        "shipping_cost":
            "Shipping Cost",

        "other_cost":
            "Other Cost"
    }

    largest_driver_name = driver_names[
        largest_cost_driver
    ]


    # ========================================================
    # Final Analysis
    # ========================================================

    analysis = (

        f"European margin changed from "
        f"{previous_margin:.2f}% in 2026 Q2 "
        f"to {latest_margin:.2f}% in 2026 Q3. "

        f"Revenue changed by "
        f"{driver_values['revenue']['change']:.2f}, "

        f"while total cost changed by "
        f"{q3_total_cost - q2_total_cost:.2f}. "

        f"The largest cost increase came from "
        f"{largest_driver_name}, "
        f"which changed by "
        f"{cost_changes[largest_cost_driver]:.2f}. "

        f"Profit changed from "
        f"{q2_profit:.2f} in Q2 "
        f"to {q3_profit:.2f} in Q3."
    )


    return {

        "question":
            "Why did our European margins drop last quarter?",

        "region":
            "Europe",

        "previous_quarter": {

            "year": 2026,

            "quarter": 2,

            "margin":
                round(previous_margin, 2)
        },

        "latest_quarter": {

            "year": 2026,

            "quarter": 3,

            "margin":
                round(latest_margin, 2)
        },

        "margin_change_percentage_points":
            round(margin_change, 2),

        "cost_drivers": {

            "revenue": {

                "q2":
                    round(
                        driver_values["revenue"]["q2"],
                        2
                    ),

                "q3":
                    round(
                        driver_values["revenue"]["q3"],
                        2
                    ),

                "change":
                    round(
                        driver_values["revenue"]["change"],
                        2
                    )
            },

            "material_cost": {

                "q2":
                    round(
                        driver_values["material_cost"]["q2"],
                        2
                    ),

                "q3":
                    round(
                        driver_values["material_cost"]["q3"],
                        2
                    ),

                "change":
                    round(
                        driver_values["material_cost"]["change"],
                        2
                    )
            },

            "shipping_cost": {

                "q2":
                    round(
                        driver_values["shipping_cost"]["q2"],
                        2
                    ),

                "q3":
                    round(
                        driver_values["shipping_cost"]["q3"],
                        2
                    ),

                "change":
                    round(
                        driver_values["shipping_cost"]["change"],
                        2
                    )
            },

            "other_cost": {

                "q2":
                    round(
                        driver_values["other_cost"]["q2"],
                        2
                    ),

                "q3":
                    round(
                        driver_values["other_cost"]["q3"],
                        2
                    ),

                "change":
                    round(
                        driver_values["other_cost"]["change"],
                        2
                    )
            }
        },

        "largest_cost_driver":
            largest_driver_name,

        "profit": {

            "q2":
                round(q2_profit, 2),

            "q3":
                round(q3_profit, 2),

            "change":
                round(
                    q3_profit - q2_profit,
                    2
                )
        },

        "analysis":
            analysis
    }


# ============================================================
# Detect Metric
# ============================================================

def detect_metric(question):

    question = question.lower()

    if "margin" in question:
        return "margin"

    if "revenue" in question:
        return "revenue"

    if "profit" in question:
        return "profit"

    if "total cost" in question:
        return "total_cost"

    if "material cost" in question:
        return "material_cost"

    if "shipping cost" in question:
        return "shipping_cost"

    if "other cost" in question:
        return "other_cost"

    return None


# ============================================================
# Detect Dimension
# ============================================================

def detect_dimension(question):

    question = question.lower()

    # Product
    if (
        "product" in question
        or "products" in question
    ):
        return "product"

    # Category
    if (
        "category" in question
        or "categories" in question
    ):
        return "category"

    # Country
    if (
        "country" in question
        or "countries" in question
    ):
        return "country"

    # Region
    if (
        "region" in question
        or "regions" in question
    ):
        return "region"

    # Customer segment
    if (
        "segment" in question
        or "customer segment" in question
    ):
        return "segment"

        # Year
    if "year" in question:
        return "year"

    # Month
    if "month" in question:
        return "month"

    # Quarter
    if (
        "quarter" in question
        or "quarters" in question
    ):
        return "quarter"

    # Default
    return "region"

# ============================================================
# Detect Comparison
# ============================================================

def detect_comparison(question):

    question = question.lower()

    if (
        "highest" in question
        or "maximum" in question
        or "max" in question
        or "best" in question
    ):
        return "highest"

    if (
        "lowest" in question
        or "minimum" in question
        or "min" in question
        or "worst" in question
    ):
        return "lowest"

    return None


# ============================================================
# Process User Question
# ============================================================

def process_question(question):

    question_lower = question.lower().strip()


    # ========================================================
    # Special Europe Margin Question
    # ========================================================

    if (
        "europe" in question_lower
        and "margin" in question_lower
        and (
            "why" in question_lower
            or "drop" in question_lower
            or "decrease" in question_lower
            or "decline" in question_lower
        )
    ):

        return analyze_europe_margin()


    # ========================================================
    # Detect Metric
    # ========================================================

    metric = detect_metric(question_lower)

    if metric is None:

        return {
            "question": question,

            "error":
                "Could not identify the requested metric. "
                "Try revenue, profit, margin, or cost."
        }


    # ========================================================
    # Detect Dimension
    # ========================================================

    dimension = detect_dimension(question_lower)


    # ========================================================
    # Detect Comparison
    # ========================================================

    comparison = detect_comparison(question_lower)


    # ========================================================
    # Detect Europe Filter
    # ========================================================

    region = None

    if "europe" in question_lower:

        region = "Europe"


    # ========================================================
    # Call Semantic Layer
    # ========================================================

    params = {

        "metric":
            metric,

        "dimensions":
            dimension
    }

    if region:

        params["region"] = region


    result = call_semantic_api(params)


    if "error" in result:

        return result


    data = result.get("data", [])


    if not data:

        return {

            "question": question,

            "metric": metric,

            "dimension": dimension,

            "data": [],

            "message":
                "No data found."
        }


    # ========================================================
    # Comparison Question
    # ========================================================

    if comparison:

        selected = None

        if comparison == "highest":

            selected = max(
                data,
                key=lambda row:
                    float(row[metric])
            )

        elif comparison == "lowest":

            selected = min(
                data,
                key=lambda row:
                    float(row[metric])
            )


        dimension_value = selected[
            dimension
        ]

        metric_value = float(
            selected[metric]
        )


        if metric == "margin":

            formatted_value = (
                f"{metric_value:.2f}%"
            )

        else:

            formatted_value = (
                f"{metric_value:.2f}"
            )


        return {

            "question":
                question,

            "metric":
                metric,

            "dimension":
                dimension,

            "comparison":
                comparison,

            "answer": (

                f"{dimension_value} has the "
                f"{comparison} {metric} "
                f"at {formatted_value}."
            ),

            "selected":
                selected,

            "data":
                data
        }


    # ========================================================
    # Normal Query
    # ========================================================

    return {

        "question":
            question,

        "metric":
            metric,

        "dimension":
            dimension,

        "data":
            data
    }


# ============================================================
# Test Agent
# ============================================================

if __name__ == "__main__":

    test_questions = [

        "Show me revenue by region.",

        "Show me profit by category.",

        "Which region has the highest revenue?",

        "Which category has the lowest margin?",

        "Show me margin by product.",

        "Show me revenue by country.",

        "Show me profit by year."

    ]


    print("\n====================================")
    print("MetricMind AI Agent")
    print("====================================")


    for question in test_questions:

        print("\n------------------------------------")

        print("User Question:")

        print(question)


        result = process_question(
            question
        )


        print("\nAgent Result:")

        print(result)