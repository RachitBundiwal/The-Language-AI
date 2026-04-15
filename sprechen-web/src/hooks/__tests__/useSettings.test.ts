import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useSettings, DEFAULT_SETTINGS } from "../useSettings";

const STORAGE_KEY = "sprechen.settings.v1";

describe("useSettings", () => {
  beforeEach(() => {
    window.localStorage.clear();
    document.documentElement.classList.remove("dark");
  });

  afterEach(() => {
    window.localStorage.clear();
    document.documentElement.classList.remove("dark");
  });

  it("returns default settings when localStorage is empty", () => {
    const { result } = renderHook(() => useSettings());
    expect(result.current.settings).toEqual(DEFAULT_SETTINGS);
  });

  it("persists settings to localStorage on update", () => {
    const { result } = renderHook(() => useSettings());

    act(() => {
      result.current.updateSettings({ speed: 10 });
    });

    const stored = JSON.parse(
      window.localStorage.getItem(STORAGE_KEY) || "{}"
    );
    expect(stored.speed).toBe(10);
    expect(result.current.settings.speed).toBe(10);
  });

  it("applies dark theme class on documentElement", () => {
    const { result } = renderHook(() => useSettings());

    act(() => {
      result.current.updateSettings({ theme: "dark" });
    });

    expect(document.documentElement.classList.contains("dark")).toBe(true);

    act(() => {
      result.current.updateSettings({ theme: "light" });
    });

    expect(document.documentElement.classList.contains("dark")).toBe(false);
  });

  it("resetSettings restores defaults", () => {
    const { result } = renderHook(() => useSettings());

    act(() => {
      result.current.updateSettings({ speed: 15, formality: "Sie" });
    });

    act(() => {
      result.current.resetSettings();
    });

    expect(result.current.settings).toEqual(DEFAULT_SETTINGS);
  });

  it("reads persisted settings from localStorage", () => {
    const custom = { ...DEFAULT_SETTINGS, weeklyGoal: 10, voice: "de-DE-ConradNeural" };
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(custom));

    const { result } = renderHook(() => useSettings());
    expect(result.current.settings.weeklyGoal).toBe(10);
    expect(result.current.settings.voice).toBe("de-DE-ConradNeural");
  });

  it("subscribers receive updates across hooks", () => {
    const { result: hook1 } = renderHook(() => useSettings());
    const { result: hook2 } = renderHook(() => useSettings());

    act(() => {
      hook1.current.updateSettings({ formality: "Sie" });
    });

    expect(hook2.current.settings.formality).toBe("Sie");
  });
});
