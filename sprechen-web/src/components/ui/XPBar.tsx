import { motion } from "framer-motion";
import type { CEFRLevel } from "@/types";
import { LEVEL_COLORS } from "@/constants/levels";

interface Props {
  currentXP: number;
  nextLevelXP: number;
  level: CEFRLevel;
  compact?: boolean;
}

export function XPBar({ currentXP, nextLevelXP, level, compact }: Props) {
  const pct = Math.max(0, Math.min(100, (currentXP / nextLevelXP) * 100));
  return (
    <div className="w-full">
      <div className="mb-1 flex items-center justify-between text-xs">
        <span className="font-bold" style={{ color: LEVEL_COLORS[level] }}>
          {level}
        </span>
        {!compact && (
          <span className="text-gray-500">
            {Math.round(currentXP)} / {nextLevelXP} XP
          </span>
        )}
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-gray-200">
        <motion.div
          className="h-full rounded-full"
          style={{ backgroundColor: LEVEL_COLORS[level] }}
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ type: "spring", stiffness: 60, damping: 15 }}
        />
      </div>
    </div>
  );
}
