import random
from datetime import date, timedelta

import psycopg2
from faker import Faker


# ---------------------------------------
# Configuration
# ---------------------------------------

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "metricmind"
DB_USER = "postgres"

# IMPORTANT:
# Replace this with the PostgreSQL password
# you created during PostgreSQL installation.
DB_PASSWORD = "8767"


fake = Faker()
random.seed(42)


# ---------------------------------------
# Corporate data
# ---------------------------------------

countries = {
    "Europe": [
        "Germany",
        "France",
        "Italy",
        "Spain",
        "Netherlands",
    ],
    "Asia": [
        "India",
        "Japan",
        "Singapore",
        "Thailand",
    ],
    "North America": [
        "USA",
        "Canada",
        "Mexico",
    ],
}

segments = [
    "Enterprise",
    "SMB",
    "Consumer",
]

categories = [
    "Electronics",
    "Software",
    "Hardware",
    "Services",
]


# ---------------------------------------
# Generate customers
# ---------------------------------------

customers = []

for customer_id in range(1, 101):

    region = random.choice(list(countries.keys()))
    country = random.choice(countries[region])

    customers.append(
        (
            customer_id,
            fake.company(),
            country,
            region,
            random.choice(segments),
        )
    )


# ---------------------------------------
# Generate products
# ---------------------------------------

products = []

for product_id in range(1, 21):

    category = random.choice(categories)

    unit_cost = round(
        random.uniform(50, 800),
        2
    )

    unit_price = round(
        unit_cost * random.uniform(1.2, 2.5),
        2
    )

    products.append(
        (
            product_id,
            f"Product {product_id}",
            category,
            unit_cost,
            unit_price,
        )
    )


# ---------------------------------------
# Generate orders and expenses
# ---------------------------------------

orders = []
expenses = []

start_date = date(2025, 1, 1)

for order_id in range(1, 2001):

    customer = random.choice(customers)
    product = random.choice(products)

    customer_id = customer[0]
    product_id = product[0]
    unit_cost = product[3]
    unit_price = product[4]

    order_date = (
        start_date
        + timedelta(days=random.randint(0, 730))
    )

    quantity = random.randint(1, 20)

    revenue = round(
        quantity * unit_price,
        2
    )

    material_cost = round(
        quantity
        * unit_cost
        * random.uniform(0.95, 1.10),
        2,
    )

    shipping_cost = round(
        revenue * random.uniform(0.03, 0.12),
        2,
    )

    other_cost = round(
        revenue * random.uniform(0.01, 0.05),
        2,
    )

    orders.append(
        (
            order_id,
            customer_id,
            product_id,
            order_date,
            quantity,
            revenue,
        )
    )

    expenses.append(
        (
            order_id,
            order_id,
            material_cost,
            shipping_cost,
            other_cost,
        )
    )


# ---------------------------------------
# Connect to PostgreSQL
# ---------------------------------------

print("Connecting to PostgreSQL...")

try:

    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    cursor = connection.cursor()

    print("Connected successfully!")


    # -----------------------------------
    # Insert customers
    # -----------------------------------

    print("Inserting customers...")

    cursor.executemany(
        """
        INSERT INTO customers
        (
            customer_id,
            customer_name,
            country,
            region,
            customer_segment
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        customers,
    )


    # -----------------------------------
    # Insert products
    # -----------------------------------

    print("Inserting products...")

    cursor.executemany(
        """
        INSERT INTO products
        (
            product_id,
            product_name,
            category,
            unit_cost,
            unit_price
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        products,
    )


    # -----------------------------------
    # Insert orders
    # -----------------------------------

    print("Inserting orders...")

    cursor.executemany(
        """
        INSERT INTO orders
        (
            order_id,
            customer_id,
            product_id,
            order_date,
            quantity,
            revenue
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        orders,
    )


    # -----------------------------------
    # Insert expenses
    # -----------------------------------

    print("Inserting expenses...")

    cursor.executemany(
        """
        INSERT INTO expenses
        (
            expense_id,
            order_id,
            material_cost,
            shipping_cost,
            other_cost
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        expenses,
    )


    # -----------------------------------
    # Commit
    # -----------------------------------

    connection.commit()

    print()
    print("===================================")
    print("MetricMind data loaded successfully!")
    print("===================================")
    print(f"Customers : {len(customers)}")
    print(f"Products  : {len(products)}")
    print(f"Orders    : {len(orders)}")
    print(f"Expenses  : {len(expenses)}")


except Exception as error:

    print()
    print("ERROR:")
    print(error)

    if "connection" in locals():
        connection.rollback()


finally:

    if "cursor" in locals():
        cursor.close()

    if "connection" in locals():
        connection.close()

    print("Database connection closed.")