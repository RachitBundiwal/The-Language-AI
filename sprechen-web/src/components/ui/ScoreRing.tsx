import { motion } from "framer-motion";

interface Props {
  score: number;
  maxScore?: number;
  label: string;
  color?: string;
  size?: number;
}

export function ScoreRing({
  score,
  maxScore = 100,
  label,
  color = "#2563EB",
  size = 120,
}: Props) {
  const pct = Math.max(0, Math.min(1, score / maxScore));
  const stroke = 10;
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - pct);

  return (
    <div className="flex flex-col items-center" style={{ width: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#E5E7EB"
          strokeWidth={stroke}
          fill="none"
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          fill="none"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: "easeOut" }}
        />
      </svg>
      <div
        className="-mt-[calc(50%+12px)] flex flex-col items-center"
        style={{ width: size }}
      >
        <span className="text-2xl font-bold text-gray-900">
          {Math.round(score)}
        </span>
      </div>
      <span className="mt-2 text-sm font-medium text-gray-600">{label}</span>
    </div>
  );
}
