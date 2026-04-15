import { describe, it, expect, beforeEach } from "vitest";
import { useToastStore } from "../toastStore";
import type { AchievementInfo } from "@/types";

const fakeAchievement = (id: string): AchievementInfo => ({
  achievement_id: id,
  title: `Title ${id}`,
  emoji: "🎓",
  description: `Desc ${id}`,
  earned: true,
  earned_at: "2026-04-01T10:00:00",
});

describe("toastStore", () => {
  beforeEach(() => {
    // Reset store state
    useToastStore.setState({ queue: [], current: null });
  });

  it("push sets current when queue is empty", () => {
    const store = useToastStore.getState();
    store.push(fakeAchievement("a1"));

    const state = useToastStore.getState();
    expect(state.current).not.toBeNull();
    expect(state.current!.achievement.achievement_id).toBe("a1");
    expect(state.queue).toHaveLength(0);
  });

  it("push queues when current is occupied", () => {
    const store = useToastStore.getState();
    store.push(fakeAchievement("a1"));
    store.push(fakeAchievement("a2"));

    const state = useToastStore.getState();
    expect(state.current!.achievement.achievement_id).toBe("a1");
    expect(state.queue).toHaveLength(1);
    expect(state.queue[0].achievement.achievement_id).toBe("a2");
  });

  it("pushMany preserves order", () => {
    const store = useToastStore.getState();
    store.pushMany([
      fakeAchievement("a1"),
      fakeAchievement("a2"),
      fakeAchievement("a3"),
    ]);

    const state = useToastStore.getState();
    expect(state.current!.achievement.achievement_id).toBe("a1");
    expect(state.queue).toHaveLength(2);
    expect(state.queue[0].achievement.achievement_id).toBe("a2");
    expect(state.queue[1].achievement.achievement_id).toBe("a3");
  });

  it("dismiss shifts next from queue to current", () => {
    const store = useToastStore.getState();
    store.push(fakeAchievement("a1"));
    store.push(fakeAchievement("a2"));
    store.push(fakeAchievement("a3"));

    store.dismiss();

    const state = useToastStore.getState();
    expect(state.current!.achievement.achievement_id).toBe("a2");
    expect(state.queue).toHaveLength(1);
  });

  it("dismiss sets current to null when queue is empty", () => {
    const store = useToastStore.getState();
    store.push(fakeAchievement("a1"));
    store.dismiss();

    const state = useToastStore.getState();
    expect(state.current).toBeNull();
    expect(state.queue).toHaveLength(0);
  });

  it("dismiss drains entire queue sequentially", () => {
    const store = useToastStore.getState();
    store.pushMany([
      fakeAchievement("a1"),
      fakeAchievement("a2"),
    ]);

    store.dismiss(); // a2 becomes current
    store.dismiss(); // queue empty, current null

    const state = useToastStore.getState();
    expect(state.current).toBeNull();
    expect(state.queue).toHaveLength(0);
  });
});
