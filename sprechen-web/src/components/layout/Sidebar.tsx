import { NavLink } from "react-router-dom";
import {
  Home,
  BookOpen,
  Mic,
  Layers,
  Award,
  BarChart2,
  Flame,
  Settings,
  Moon,
  Sun,
} from "lucide-react";
import { useProgressStore } from "@/store/progressStore";
import { XPBar } from "@/components/ui/XPBar";
import { XP_PER_LEVEL } from "@/constants/levels";
import { useSettings } from "@/hooks/useSettings";

const NAV = [
  { to: "/", label: "Home", icon: Home },
  { to: "/lessons", label: "Lektionen", icon: BookOpen },
  { to: "/conversation", label: "Sprechen", icon: Mic },
  { to: "/vocabulary", label: "Vokabeln", icon: Layers },
  { to: "/exam", label: "Prüfung", icon: Award },
  { to: "/progress", label: "Fortschritt", icon: BarChart2 },
];

export function Sidebar() {
  const { xp, streak, level } = useProgressStore();
  const { settings, updateSettings } = useSettings();
  const nextLevelXP = XP_PER_LEVEL[level];
  const isDark = settings.theme === "dark";

  const toggleTheme = () =>
    updateSettings({ theme: isDark ? "light" : "dark" });

  return (
    <>
      {/* Desktop sidebar */}
      <aside className="fixed left-0 top-0 z-40 hidden h-full w-60 flex-col border-r border-gray-200 bg-white px-4 py-6 md:flex dark:border-gray-700 dark:bg-gray-900">
        <div className="mb-8 flex items-center justify-between px-2">
          <span className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Sprechen <span>🇩🇪</span>
          </span>
          <button
            onClick={toggleTheme}
            className="rounded-lg p-1.5 text-gray-500 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800"
            aria-label="Theme wechseln"
            title="Theme wechseln"
          >
            {isDark ? <Sun size={16} /> : <Moon size={16} />}
          </button>
        </div>
        <nav className="flex-1 space-y-1">
          {NAV.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === "/"}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-primary text-white"
                    : "text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800"
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
          <NavLink
            to="/settings"
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                isActive
                  ? "bg-primary text-white"
                  : "text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800"
              }`
            }
          >
            <Settings size={18} />
            Einstellungen
          </NavLink>
        </nav>
        <div className="space-y-3 border-t border-gray-200 pt-4 dark:border-gray-700">
          <XPBar currentXP={xp} nextLevelXP={nextLevelXP} level={level} compact />
          <div className="flex items-center gap-2 px-2 text-sm text-gray-600 dark:text-gray-400">
            <Flame size={16} className="text-orange-500" />
            <span className="font-bold">{streak}</span>
            <span className="text-gray-500">Tage</span>
          </div>
        </div>
      </aside>

      {/* Mobile bottom tab bar */}
      <nav className="fixed bottom-0 left-0 right-0 z-40 flex h-14 border-t border-gray-200 bg-white md:hidden dark:border-gray-700 dark:bg-gray-900">
        {NAV.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/"}
            className={({ isActive }) =>
              `flex flex-1 flex-col items-center justify-center text-[10px] font-medium ${
                isActive ? "text-primary" : "text-gray-500"
              }`
            }
          >
            <Icon size={18} />
            <span className="mt-0.5">{label}</span>
          </NavLink>
        ))}
      </nav>
    </>
  );
}
