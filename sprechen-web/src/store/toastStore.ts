import { create } from "zustand";
import type { AchievementInfo } from "@/types";

interface QueuedToast {
  id: number;
  achievement: AchievementInfo;
}

interface ToastState {
  queue: QueuedToast[];
  current: QueuedToast | null;
  push: (achievement: AchievementInfo) => void;
  pushMany: (achievements: AchievementInfo[]) => void;
  dismiss: () => void;
}

let nextId = 1;

export const useToastStore = create<ToastState>((set, get) => ({
  queue: [],
  current: null,
  push: (achievement) => {
    const item: QueuedToast = { id: nextId++, achievement };
    const { current } = get();
    if (current === null) {
      set({ current: item });
    } else {
      set((s) => ({ queue: [...s.queue, item] }));
    }
  },
  pushMany: (achievements) => {
    achievements.forEach((a) => get().push(a));
  },
  dismiss: () => {
    const { queue } = get();
    if (queue.length === 0) {
      set({ current: null });
    } else {
      const [next, ...rest] = queue;
      set({ current: next, queue: rest });
    }
  },
}));
