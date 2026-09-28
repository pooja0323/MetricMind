"use client";

import { useState } from "react";
import Chart from "./Chart";
import CostChart from "./CostChart";
import ProfitChart from "./ProfitChart";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const sampleQuestions = [
    "Show me revenue by region.",
    "Which region has the highest revenue?",
    "Which category has the lowest margin?",
    "Show me profit by year.",
  ];

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/agent-query?question=${encodeURIComponent(
          question
        )}`
      );

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        error: "Could not connect to MetricMind backend.",
      });
    }

    setLoading(false);
  };

  const formatNumber = (value: any) => {
    const number = Number(value);

    if (!Number.isFinite(number)) {
      return "N/A";
    }

    return number.toLocaleString("en-IN", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  };

  return (
    <main className="min-h-screen bg-slate-950 text-white">

      {/* HEADER */}
      <header className="border-b border-slate-800 bg-slate-950/95">
        <div className="max-w-6xl mx-auto px-6 md:px-8 py-5 flex items-center justify-between">

          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              MetricMind
            </h1>

            <p className="text-sm text-slate-400 mt-1">
              Agentic Semantic BI Engine
            </p>
          </div>

          <div className="flex items-center gap-2 text-sm text-slate-400">
            <span className="w-2 h-2 rounded-full bg-green-500"></span>
            System Online
          </div>

        </div>
      </header>

      {/* MAIN */}
      <section className="max-w-6xl mx-auto px-6 md:px-8 py-12">

        {/* HERO */}
        <div className="mb-10">

          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-blue-900 bg-blue-950/40 text-blue-400 text-sm mb-5">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
            Governed Business Intelligence
          </div>

          <h2 className="text-4xl md:text-5xl font-bold tracking-tight">
            Ask your business data
          </h2>

          <p className="text-slate-400 mt-4 text-base md:text-lg max-w-2xl">
            Explore revenue, profit, margin and business performance using
            governed business metrics and an agentic semantic layer.
          </p>

        </div>

        {/* QUESTION CARD */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl">

          <label className="block text-sm font-medium text-slate-300 mb-3">
            Ask a business question
          </label>

          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && e.ctrlKey) {
                askQuestion();
              }
            }}
            placeholder="Example: Which region has the highest revenue?"
            className="w-full h-32 bg-slate-950 border border-slate-700 rounded-xl p-4 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none text-slate-200 placeholder:text-slate-600"
          />

          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mt-4">

            <p className="text-xs text-slate-500">
              Press Ctrl + Enter to run your query
            </p>

            <button
              onClick={askQuestion}
              disabled={loading || !question.trim()}
              className="px-7 py-3 bg-blue-600 hover:bg-blue-500 rounded-xl font-semibold shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Analyzing..." : "Ask MetricMind"}
            </button>

          </div>

          {/* SAMPLE QUESTIONS */}
          <div className="mt-6">

            <p className="text-xs uppercase tracking-wider text-slate-500 mb-3">
              Try a sample question
            </p>

            <div className="flex flex-wrap gap-2">

              {sampleQuestions.map((sample) => (
                <button
                  key={sample}
                  onClick={() => setQuestion(sample)}
                  className="px-3 py-2 text-sm rounded-lg border border-slate-700 bg-slate-950 text-slate-300 hover:border-blue-600 hover:text-blue-400 transition"
                >
                  {sample}
                </button>
              ))}

            </div>

          </div>

        </div>

        {/* RESULT */}
        {result && (
          <div className="mt-8">

            {/* ERROR */}
            {result.error ? (
              <div className="bg-red-950/50 border border-red-800 rounded-2xl p-6">

                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full bg-red-900 flex items-center justify-center">
                    !
                  </div>

                  <h3 className="font-semibold text-red-400">
                    Query Error
                  </h3>
                </div>

                <p className="mt-3 text-slate-300">
                  {result.error}
                </p>

              </div>
            ) : (
              <>

                {/* ANSWER */}
                {result.answer && (
                  <div className="bg-blue-950/40 border border-blue-800 rounded-2xl p-6 shadow-lg">

                    <div className="flex items-center gap-3 mb-3">
                      <div className="w-9 h-9 rounded-full bg-blue-900 flex items-center justify-center text-blue-300">
                        ✓
                      </div>

                      <h3 className="text-lg font-semibold text-blue-400">
                        Answer
                      </h3>
                    </div>

                    <p className="text-slate-200 text-lg leading-relaxed">
                      {result.answer}
                    </p>

                  </div>
                )}

                {/* QUERY RESULTS */}
                {result.data && (
                  <div className="mt-6 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-lg">

                    <div className="flex items-center justify-between mb-5">

                      <div>
                        <h3 className="text-xl font-semibold">
                          {result.metric
                            ? `${result.metric.charAt(0).toUpperCase()}${result.metric.slice(
                                1
                              )} by ${
                                result.dimension
                                  ? result.dimension.charAt(0).toUpperCase() +
                                    result.dimension.slice(1)
                                  : "Dimension"
                              }`
                            : "Query Results"}
                        </h3>

                        <p className="text-sm text-slate-500 mt-1">
                          Governed semantic query result
                        </p>
                      </div>

                      <div className="px-3 py-1 rounded-full bg-slate-950 border border-slate-700 text-xs text-slate-400">
                        {result.data.length} results
                      </div>

                    </div>

                    <div className="space-y-3">

                      {result.data.map((row: any, index: number) => {

                        const dimensionKey = Object.keys(row).find(
                          (key) => key !== result.metric
                        );

                        const dimensionValue = dimensionKey
                          ? row[dimensionKey]
                          : "Unknown";

                        const metricValue = Number(row[result.metric]);

                        return (
                          <div
                            key={index}
                            className="flex items-center justify-between bg-slate-950 border border-slate-800 rounded-xl px-5 py-4 hover:border-slate-700 transition"
                          >

                            <span className="text-slate-300">
                              {dimensionValue}
                            </span>

                            <span className="font-semibold text-white">
                              {formatNumber(metricValue)}
                              {result.metric === "margin" ? "%" : ""}
                            </span>

                          </div>
                        );
                      })}

                    </div>

                  </div>
                )}

                {/* QUARTERLY MARGIN KPI CARDS */}
                {result.previous_quarter && result.latest_quarter && (
                  <div className="grid md:grid-cols-3 gap-5 mt-6">

                    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
                      <p className="text-sm text-slate-400">
                        Previous Quarter Margin
                      </p>

                      <p className="text-3xl font-bold mt-2">
                        {result.previous_quarter.margin}%
                      </p>
                    </div>

                    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
                      <p className="text-sm text-slate-400">
                        Latest Quarter Margin
                      </p>

                      <p className="text-3xl font-bold mt-2">
                        {result.latest_quarter.margin}%
                      </p>
                    </div>

                    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
                      <p className="text-sm text-slate-400">
                        Margin Change
                      </p>

                      <p className="text-3xl font-bold mt-2">
                        {result.margin_change_percentage_points} pp
                      </p>
                    </div>

                  </div>
                )}

                {/* MARGIN CHART */}
                {result.previous_quarter && result.latest_quarter && (
                  <div className="mt-6 bg-slate-900 border border-slate-800 rounded-2xl p-6">

                    <h3 className="text-xl font-semibold mb-5">
                      Margin Comparison
                    </h3>

                    <Chart
                      previous={result.previous_quarter}
                      latest={result.latest_quarter}
                    />

                  </div>
                )}

                {/* COST DRIVERS */}
                {result.cost_drivers && (
                  <div className="mt-6 bg-slate-900 border border-slate-800 rounded-2xl p-6">

                    <div className="mb-5">
                      <h3 className="text-xl font-semibold">
                        Cost Drivers
                      </h3>

                      <p className="text-sm text-slate-500 mt-1">
                        Comparison of major business cost components
                      </p>
                    </div>

                    <CostChart
                      costDrivers={result.cost_drivers}
                    />

                    <div className="grid md:grid-cols-4 gap-4 mt-6">

                      {Object.entries(result.cost_drivers).map(
                        ([name, values]: any) => (
                          <div
                            key={name}
                            className="bg-slate-950 border border-slate-800 rounded-xl p-4"
                          >

                            <p className="text-slate-400 text-sm capitalize">
                              {name.replace("_", " ")}
                            </p>

                            <p
                              className={`text-xl font-semibold mt-2 ${
                                values.change >= 0
                                  ? "text-red-400"
                                  : "text-green-400"
                              }`}
                            >
                              {values.change >= 0 ? "+" : ""}
                              {values.change.toFixed(2)}
                            </p>

                          </div>
                        )
                      )}

                    </div>

                    <div className="mt-5 pt-5 border-t border-slate-800">

                      <p className="text-sm text-slate-400">
                        Largest cost driver
                      </p>

                      <p className="font-semibold text-white mt-1">
                        {result.largest_cost_driver}
                      </p>

                    </div>

                  </div>
                )}

                {/* PROFIT */}
                {result.profit && (
                  <div className="mt-6 bg-slate-900 border border-slate-800 rounded-2xl p-6">

                    <div className="mb-5">
                      <h3 className="text-xl font-semibold">
                        Profit Comparison
                      </h3>

                      <p className="text-sm text-slate-500 mt-1">
                        Profit performance across the selected periods
                      </p>
                    </div>

                    <ProfitChart profit={result.profit} />

                    <div className="grid md:grid-cols-3 gap-5 mt-6">

                      <div className="bg-slate-950 border border-slate-800 rounded-xl p-4">
                        <p className="text-slate-400 text-sm">
                          Q2
                        </p>

                        <p className="text-xl font-semibold mt-2">
                          ₹{formatNumber(result.profit.q2)}
                        </p>
                      </div>

                      <div className="bg-slate-950 border border-slate-800 rounded-xl p-4">
                        <p className="text-slate-400 text-sm">
                          Q3
                        </p>

                        <p className="text-xl font-semibold mt-2">
                          ₹{formatNumber(result.profit.q3)}
                        </p>
                      </div>

                      <div className="bg-slate-950 border border-slate-800 rounded-xl p-4">
                        <p className="text-slate-400 text-sm">
                          Change
                        </p>

                        <p className="text-xl font-semibold mt-2">
                          ₹{formatNumber(result.profit.change)}
                        </p>
                      </div>

                    </div>

                  </div>
                )}

              </>
            )}

          </div>
        )}

      </section>

      {/* FOOTER */}
      <footer className="border-t border-slate-800 mt-10">

        <div className="max-w-6xl mx-auto px-6 md:px-8 py-6 flex flex-col md:flex-row justify-between gap-3 text-sm text-slate-500">

          <p>
            MetricMind — Agentic Semantic BI Engine
          </p>

          <p>
            Governed metrics • PostgreSQL • FastAPI • Next.js
          </p>

        </div>

      </footer>

    </main>
  );
}