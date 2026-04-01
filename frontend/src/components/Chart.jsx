import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

export default function Chart({ rul }) {
  if (!rul) return null;

  const data = Array.from({ length: 10 }, (_, i) => ({
    cycle: i,
    value: rul + (10 - i) * 2,
  }));

  return (
    <LineChart width={500} height={300} data={data}>
      <XAxis dataKey="cycle" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="value" />
    </LineChart>
  );
}