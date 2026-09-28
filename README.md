# MetricMind

## Agentic Semantic BI Engine

MetricMind is an AI-powered Business Intelligence system that allows users to ask business questions in natural language and receive governed, consistent analytics from PostgreSQL data.

The system combines a conversational interface, an agentic query layer, a governed semantic layer, and a PostgreSQL database.

---

## 1. Problem Statement

Traditional Text-to-SQL systems can generate incorrect SQL because business definitions, joins, and metric calculations may not always be consistent.

For example, different queries may calculate Revenue, Profit, or Margin differently.

MetricMind addresses this problem by introducing a governed Semantic Layer that defines approved business metrics and dimensions before queries are executed.

---

## 2. Objective

The main objectives of MetricMind are:

- Allow users to ask business questions using natural language.
- Convert business questions into governed analytical queries.
- Maintain consistent definitions for Revenue, Profit, Margin, and Costs.
- Prevent unsupported metrics and dimensions from being queried.
- Execute analytical queries against PostgreSQL.
- Present results through a conversational BI interface.
- Support comparison questions such as highest and lowest values.

---

## 3. System Architecture

```text
+----------------------+
|    Next.js Frontend  |
|      Chat Interface  |
+----------+-----------+
           |
           | HTTP Request
           v
+----------------------+
|    FastAPI Backend   |
|     REST API         |
+----------+-----------+
           |
           v
+----------------------+
|   Agentic Query      |
|   Processing Layer   |
+----------+-----------+
           |
           v
+----------------------+
|    Semantic Layer    |
|                      |
| Metrics              |
| Dimensions           |
| Validation           |
| Query Builder        |
+----------+-----------+
           |
           v
+----------------------+
|     PostgreSQL       |
|      Database        |
+----------------------+