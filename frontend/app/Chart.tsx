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
  previous: {
    margin: number;
  };
  latest: {
    margin: number;
  };
};

export default function Chart({ previous, latest }: Props) {
  const data = [
    {
      quarter: "Previous",
      margin: Number(previous.margin),
    },
    {
      quarter: "Latest",
      margin: Number(latest.margin),
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
            left: 20,
            bottom: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="quarter"
            tick={{ fill: "#cbd5e1" }}
          />

          <YAxis
            domain={[0, 40]}
            tickFormatter={(value) => `${value}%`}
            tick={{ fill: "#cbd5e1" }}
          />

          <Tooltip
            formatter={(value) => [
              `${Number(value).toFixed(2)}%`,
              "Margin",
            ]}
          />

          <Bar
            dataKey="margin"
            name="Margin"
            fill="#3b82f6"
            radius={[6, 6, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}