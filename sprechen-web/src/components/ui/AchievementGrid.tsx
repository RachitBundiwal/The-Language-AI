import { Lock } from "lucide-react";
import type { AchievementInfo } from "@/types";

interface Props {
  achievements: AchievementInfo[];
}

export function AchievementGrid({ achievements }: Props) {
  if (achievements.length === 0) {
    return (
      <p className="py-6 text-center text-sm text-gray-400">
        Noch keine Erfolge verfügbar.
      </p>
    );
  }
  return (
    <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
      {achievements.map((a) => (
        <Badge key={a.achievement_id} achievement={a} />
      ))}
    </div>
  );
}

function Badge({ achievement: a }: { achievement: AchievementInfo }) {
  const tooltip = a.earned
    ? `Freigeschaltet: ${a.earned_at ? new Date(a.earned_at).toLocaleDateString("de-DE") : ""}`
    : "Noch nicht freigeschaltet";
  return (
    <div
      title={`${a.description} — ${tooltip}`}
      className={`relative flex flex-col items-center gap-1 rounded-xl border-2 p-4 text-center transition-all ${
        a.earned
          ? "border-yellow-300 bg-gradient-to-br from-yellow-50 to-white shadow-sm"
          : "border-gray-200 bg-gray-50 grayscale"
      }`}
    >
      <div className="text-3xl">{a.emoji}</div>
      <p
        className={`text-xs font-bold ${a.earned ? "text-gray-900" : "text-gray-400"}`}
      >
        {a.title}
      </p>
      <p className="text-[10px] leading-tight text-gray-500">{a.description}</p>
      {!a.earned && (
        <div className="absolute right-2 top-2 rounded-full bg-white/80 p-1 text-gray-400">
          <Lock size={10} />
        </div>
      )}
    </div>
  );
}
