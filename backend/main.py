from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

from semantic_layer.query_builder import build_query
from agent.agent import process_question

app = FastAPI(
    title="MetricMind API",
    description="Agentic Semantic BI Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "metricmind"
DB_USER = "postgres"
DB_PASSWORD = "8767"


# ---------------------------------------
# Health Check
# ---------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "MetricMind API"
    }


# ---------------------------------------
# Semantic Query API
# ---------------------------------------

@app.get("/semantic-query")
def semantic_query(
    metric: str,
    dimensions: str = "region",
    region: str = None,
    country: str = None,
    category: str = None,
    start_date: str = None,
    end_date: str = None
):

    # Convert comma-separated dimensions
    # into a Python list

    dimension_list = [
        item.strip()
        for item in dimensions.split(",")
    ]

    sql = build_query(
        metric=metric,
        dimensions=dimension_list,
        region=region,
        country=country,
        category=category,
        start_date=start_date,
        end_date=end_date
    )

    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cursor = connection.cursor()

    cursor.execute(sql)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    data = []

    for row in results:

        row_data = {}

        for index, dimension in enumerate(dimension_list):
            value = row[index]

            if hasattr(value, "item"):
                value = value.item()

            row_data[dimension] = value

        metric_value = row[len(dimension_list)]

        if hasattr(metric_value, "item"):
            metric_value = metric_value.item()

        row_data[metric] = float(metric_value)

        data.append(row_data)

    return {
        "metric": metric,
        "dimensions": dimension_list,
        "region": region,
        "country": country,
        "category": category,
        "sql": sql,
        "data": data
    }

# ---------------------------------------
# Agent Query API
# ---------------------------------------

@app.get("/agent-query")
def agent_query(question: str):

    result = process_question(question)

    return result