import { create } from "zustand";
import type { CEFRLevel, DashboardStats } from "@/types";

interface ProgressState {
  xp: number;
  streak: number;
  level: CEFRLevel;
  vocabDueCount: number;
  updateFromStats: (stats: DashboardStats) => void;
  addXP: (n: number) => void;
}

export const useProgressStore = create<ProgressState>((set) => ({
  xp: 0,
  streak: 0,
  level: "A1",
  vocabDueCount: 0,
  updateFromStats: (stats) =>
    set({
      xp: stats.xp,
      streak: stats.streak,
      level: stats.level,
      vocabDueCount: stats.vocab_due_count,
    }),
  addXP: (n) => set((state) => ({ xp: state.xp + n })),
}));
