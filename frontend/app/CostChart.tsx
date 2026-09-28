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

type CostDriver = {
  change: number;
};

type Props = {
  costDrivers: {
    revenue: CostDriver;
    material_cost: CostDriver;
    shipping_cost: CostDriver;
    other_cost: CostDriver;
  };
};

export default function CostChart({ costDrivers }: Props) {
  const data = [
    {
      name: "Revenue",
      change: Number(costDrivers.revenue.change),
    },
    {
      name: "Material Cost",
      change: Number(costDrivers.material_cost.change),
    },
    {
      name: "Shipping Cost",
      change: Number(costDrivers.shipping_cost.change),
    },
    {
      name: "Other Cost",
      change: Number(costDrivers.other_cost.change),
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
            bottom: 50,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="name"
            interval={0}
            angle={-15}
            textAnchor="end"
            height={70}
            tick={{ fill: "#cbd5e1" }}
          />

          <YAxis
            tickFormatter={(value) =>
              value.toLocaleString()
            }
            tick={{ fill: "#cbd5e1" }}
          />

          <Tooltip
            formatter={(value) => [
              Number(value).toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              }),
              "Change",
            ]}
          />

          <Bar
            dataKey="change"
            name="Change"
            fill="#3b82f6"
            radius={[6, 6, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}