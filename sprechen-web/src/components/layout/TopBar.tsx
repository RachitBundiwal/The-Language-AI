import { useLocation } from "react-router-dom";
import { Flame, Sparkles } from "lucide-react";
import { useProgressStore } from "@/store/progressStore";

const TITLES: Record<string, string> = {
  "/": "Startseite",
  "/lessons": "Lektionen",
  "/conversation": "Gespräch",
  "/vocabulary": "Vokabeln",
  "/exam": "Prüfung",
  "/exam/result": "Prüfungsergebnis",
  "/progress": "Fortschritt",
  "/voice": "Sprachübung",
  "/settings": "Einstellungen",
};

export function TopBar() {
  const location = useLocation();
  const { xp, streak } = useProgressStore();

  const path = location.pathname;
  let title = TITLES[path];
  if (!title) {
    if (path.startsWith("/lessons/")) title = "Lektion";
    else title = "Sprechen";
  }

  return (
    <header className="sticky top-0 z-30 flex h-14 items-center justify-between border-b border-gray-200 bg-white px-4 md:px-8 dark:border-gray-700 dark:bg-gray-900">
      <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">
        {title}
      </h1>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1.5 text-sm">
          <Flame size={16} className="text-orange-500" />
          <span className="font-bold text-gray-900 dark:text-gray-100">
            {streak}
          </span>
        </div>
        <div className="flex items-center gap-1.5 text-sm">
          <Sparkles size={16} className="text-primary" />
          <span className="font-bold text-gray-900 dark:text-gray-100">
            {xp.toLocaleString()}
          </span>
          <span className="text-gray-500">XP</span>
        </div>
      </div>
    </header>
  );
}
