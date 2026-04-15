import type { CEFRLevel } from "@/types";
import { LEVEL_BG_CLASS } from "@/constants/levels";

interface Props {
  level: CEFRLevel;
  size?: "sm" | "md" | "lg";
}

const SIZE_CLS: Record<NonNullable<Props["size"]>, string> = {
  sm: "px-2 py-0.5 text-xs",
  md: "px-2.5 py-1 text-sm",
  lg: "px-3 py-1.5 text-base",
};

export function LevelBadge({ level, size = "md" }: Props) {
  return (
    <span
      className={`inline-flex items-center rounded-full font-bold text-white ${LEVEL_BG_CLASS[level]} ${SIZE_CLS[size]}`}
    >
      {level}
    </span>
  );
}
