import psycopg2

from semantic_layer.query_builder import build_query


# ---------------------------------------
# PostgreSQL configuration
# ---------------------------------------

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "metricmind"
DB_USER = "postgres"

# Replace with your PostgreSQL password.
# Do NOT send your password to me.
DB_PASSWORD = "8767"


# ---------------------------------------
# Build Semantic Layer query
# ---------------------------------------

sql = build_query(
    metric="margin",
    dimensions=["region"]
)


print("====================================")
print("MetricMind Semantic Query")
print("====================================")

print(sql)


# ---------------------------------------
# Connect to PostgreSQL
# ---------------------------------------

print("\nConnecting to PostgreSQL...")

connection = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = connection.cursor()

print("Connected successfully!")


# ---------------------------------------
# Execute query
# ---------------------------------------

print("\nExecuting query...\n")

cursor.execute(sql)

results = cursor.fetchall()


# ---------------------------------------
# Display results
# ---------------------------------------

print("====================================")
print("QUERY RESULTS")
print("====================================")

for row in results:
    print(row)


# ---------------------------------------
# Close connection
# ---------------------------------------

cursor.close()
connection.close()

print("\nDatabase connection closed.")