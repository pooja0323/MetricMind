from semantic_layer.query_builder import build_query


print("====================================")
print("MetricMind Semantic Layer Test")
print("====================================")


# Test 1: Revenue by Region
print("\nTEST 1: Revenue by Region")
print("------------------------------------")

sql = build_query(
    metric="revenue",
    dimensions=["region"]
)

print(sql)


# Test 2: Margin by Region
print("\nTEST 2: Margin by Region")
print("------------------------------------")

sql = build_query(
    metric="margin",
    dimensions=["region"]
)

print(sql)


# Test 3: European Revenue
print("\nTEST 3: European Revenue")
print("------------------------------------")

sql = build_query(
    metric="revenue",
    region="Europe"
)

print(sql)


print("\n====================================")
print("Semantic Layer Test Completed")
print("====================================")