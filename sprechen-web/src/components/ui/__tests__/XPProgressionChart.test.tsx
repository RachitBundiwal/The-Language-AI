import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { XPProgressionChart } from "../XPProgressionChart";
import type { XPProgression } from "@/types";

// Recharts uses ResizeObserver internally, mock it for jsdom
vi.stubGlobal(
  "ResizeObserver",
  vi.fn(() => ({
    observe: vi.fn(),
    unobserve: vi.fn(),
    disconnect: vi.fn(),
  })),
);

describe("XPProgressionChart", () => {
  it("shows empty-state when data is undefined", () => {
    render(<XPProgressionChart data={undefined} />);
    expect(
      screen.getByText(/Noch keine XP-Verlaufsdaten/),
    ).toBeInTheDocument();
  });

  it("shows empty-state when points array is empty", () => {
    const data: XPProgression = {
      points: [],
      thresholds: { A1: 0, A2: 500, B1: 1500, B2: 3500, C1: 7000, C2: 13000 },
    };
    render(<XPProgressionChart data={data} />);
    expect(
      screen.getByText(/Noch keine XP-Verlaufsdaten/),
    ).toBeInTheDocument();
  });

  it("renders chart container when data is provided", () => {
    const data: XPProgression = {
      points: [
        { date: "2026-04-09T12:00:00", cumulative_xp: 500, level_at_time: "A2" },
      ],
      thresholds: { A1: 0, A2: 500, B1: 1500, B2: 3500, C1: 7000, C2: 13000 },
    };
    const { container } = render(<XPProgressionChart data={data} />);
    // The chart container div should be rendered
    expect(container.querySelector(".h-72")).not.toBeNull();
  });
});
