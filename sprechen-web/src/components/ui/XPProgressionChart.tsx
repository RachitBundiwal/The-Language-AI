import {
  Area,
  AreaChart,
  CartesianGrid,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { CEFRLevel, XPProgression } from "@/types";

interface Props {
  data: XPProgression | undefined;
}

export function XPProgressionChart({ data }: Props) {
  if (!data || data.points.length === 0) {
    return (
      <p className="py-8 text-center text-sm text-gray-400">
        Noch keine XP-Verlaufsdaten.
      </p>
    );
  }

  const chartData = data.points.map((p) => ({
    date: new Date(p.date).toLocaleDateString("de-DE", {
      day: "2-digit",
      month: "2-digit",
    }),
    xp: p.cumulative_xp,
    level: p.level_at_time,
  }));

  const maxXP = chartData[chartData.length - 1]?.xp ?? 0;

  const thresholdEntries = (
    Object.entries(data.thresholds) as [CEFRLevel, number][]
  )
    .filter(([, v]) => v > 0 && v <= maxXP * 1.2)
    .sort((a, b) => a[1] - b[1]);

  return (
    <div className="h-72">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData}>
          <defs>
            <linearGradient id="xpGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#2563EB" stopOpacity={0.45} />
              <stop offset="95%" stopColor="#2563EB" stopOpacity={0.02} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis dataKey="date" stroke="#9CA3AF" fontSize={11} />
          <YAxis stroke="#9CA3AF" fontSize={11} />
          <Tooltip
            contentStyle={{
              borderRadius: 8,
              border: "1px solid #E5E7EB",
              fontSize: 12,
            }}
            formatter={(value: number, _name, item) => [
              `${Math.round(value).toLocaleString()} XP`,
              `Niveau ${item?.payload?.level ?? ""}`,
            ]}
          />
          {thresholdEntries.map(([level, value]) => (
            <ReferenceLine
              key={level}
              y={value}
              stroke="#9CA3AF"
              strokeDasharray="4 4"
              label={{
                value: level,
                position: "right",
                fill: "#6B7280",
                fontSize: 10,
              }}
            />
          ))}
          <Area
            type="monotone"
            dataKey="xp"
            stroke="#2563EB"
            strokeWidth={2}
            fill="url(#xpGradient)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
