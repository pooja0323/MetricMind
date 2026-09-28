"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

type Props = {
  profit: {
    q2: number;
    q3: number;
    change: number;
  };
};

export default function ProfitChart({ profit }: Props) {
  const data = [
    {
      quarter: "Q2",
      profit: Number(profit.q2),
    },
    {
      quarter: "Q3",
      profit: Number(profit.q3),
    },
  ];

  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{
            top: 20,
            right: 30,
            left: 30,
            bottom: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="quarter"
            tick={{ fill: "#cbd5e1" }}
          />

          <YAxis
            tickFormatter={(value) =>
              `₹${Number(value).toLocaleString()}`
            }
            tick={{ fill: "#cbd5e1" }}
          />

          <Tooltip
            formatter={(value) => [
              `₹${Number(value).toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })}`,
              "Profit",
            ]}
          />

          <Bar
            dataKey="profit"
            name="Profit"
            fill="#3b82f6"
            radius={[6, 6, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}