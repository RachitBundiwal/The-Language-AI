import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { AchievementGrid } from "../AchievementGrid";
import type { AchievementInfo } from "@/types";

const earned: AchievementInfo = {
  achievement_id: "first_lesson",
  title: "Erster Schritt",
  emoji: "🎓",
  description: "Erste Lektion abgeschlossen",
  earned: true,
  earned_at: "2026-04-01T10:00:00",
};

const locked: AchievementInfo = {
  achievement_id: "lessons_10",
  title: "Auf Kurs",
  emoji: "📖",
  description: "10 Lektionen abgeschlossen",
  earned: false,
  earned_at: null,
};

describe("AchievementGrid", () => {
  it("shows empty-state message when no achievements", () => {
    render(<AchievementGrid achievements={[]} />);
    expect(
      screen.getByText(/Noch keine Erfolge verfügbar/),
    ).toBeInTheDocument();
  });

  it("renders earned achievement with title", () => {
    render(<AchievementGrid achievements={[earned]} />);
    expect(screen.getByText("Erster Schritt")).toBeInTheDocument();
    expect(screen.getByText("🎓")).toBeInTheDocument();
  });

  it("renders locked achievement with description", () => {
    render(<AchievementGrid achievements={[locked]} />);
    expect(screen.getByText("Auf Kurs")).toBeInTheDocument();
    expect(screen.getByText("10 Lektionen abgeschlossen")).toBeInTheDocument();
  });

  it("earned badges have yellow border styling", () => {
    const { container } = render(<AchievementGrid achievements={[earned]} />);
    const badge = container.querySelector(".border-yellow-300");
    expect(badge).not.toBeNull();
  });

  it("locked badges have grayscale styling", () => {
    const { container } = render(<AchievementGrid achievements={[locked]} />);
    const badge = container.querySelector(".grayscale");
    expect(badge).not.toBeNull();
  });

  it("renders both earned and locked in the same grid", () => {
    render(<AchievementGrid achievements={[earned, locked]} />);
    expect(screen.getByText("Erster Schritt")).toBeInTheDocument();
    expect(screen.getByText("Auf Kurs")).toBeInTheDocument();
  });
});
