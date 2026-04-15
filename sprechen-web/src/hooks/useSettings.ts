import { useCallback, useEffect, useState } from "react";

export type Theme = "light" | "dark";
export type Formality = "du" | "Sie";

export interface Settings {
  voice: string;
  speed: number; // -20 .. +20 (percent)
  formality: Formality;
  theme: Theme;
  weeklyGoal: 1 | 2 | 5 | 10;
}

const STORAGE_KEY = "sprechen.settings.v1";

export const DEFAULT_SETTINGS: Settings = {
  voice: "de-DE-KatjaNeural",
  speed: 0,
  formality: "du",
  theme: "light",
  weeklyGoal: 5,
};

function readStorage(): Settings {
  if (typeof window === "undefined") return DEFAULT_SETTINGS;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return DEFAULT_SETTINGS;
    const parsed = JSON.parse(raw) as Partial<Settings>;
    return { ...DEFAULT_SETTINGS, ...parsed };
  } catch {
    return DEFAULT_SETTINGS;
  }
}

function applyTheme(theme: Theme) {
  if (typeof document === "undefined") return;
  const root = document.documentElement;
  if (theme === "dark") root.classList.add("dark");
  else root.classList.remove("dark");
}

// Apply persisted theme immediately at module load so there's no flash.
if (typeof window !== "undefined") {
  applyTheme(readStorage().theme);
}

const listeners = new Set<(s: Settings) => void>();
let current: Settings = readStorage();

function persist(next: Settings) {
  current = next;
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  } catch {
    // storage unavailable — ignore
  }
  applyTheme(next.theme);
  listeners.forEach((fn) => fn(next));
}

export function useSettings(): {
  settings: Settings;
  updateSettings: (patch: Partial<Settings>) => void;
  resetSettings: () => void;
} {
  const [settings, setSettings] = useState<Settings>(current);

  useEffect(() => {
    const fn = (s: Settings) => setSettings(s);
    listeners.add(fn);
    return () => {
      listeners.delete(fn);
    };
  }, []);

  const updateSettings = useCallback((patch: Partial<Settings>) => {
    persist({ ...current, ...patch });
  }, []);

  const resetSettings = useCallback(() => {
    persist({ ...DEFAULT_SETTINGS });
  }, []);

  return { settings, updateSettings, resetSettings };
}
