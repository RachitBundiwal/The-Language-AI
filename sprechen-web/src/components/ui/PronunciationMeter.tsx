import { motion } from "framer-motion";

interface Props {
  label: string;
  score: number;
}

export function PronunciationMeter({ label, score }: Props) {
  const pct = Math.max(0, Math.min(100, score));
  const color =
    pct >= 80 ? "#16A34A" : pct >= 60 ? "#D97706" : "#DC2626";
  return (
    <div className="w-full">
      <div className="mb-1 flex items-center justify-between text-sm">
        <span className="font-medium text-gray-700">{label}</span>
        <span className="font-bold" style={{ color }}>
          {Math.round(pct)}
        </span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-gray-200">
        <motion.div
          className="h-full rounded-full"
          style={{ backgroundColor: color }}
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        />
      </div>
    </div>
  );
}
