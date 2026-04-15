import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { StudyHeatmap } from "../StudyHeatmap";
import type { HeatmapCell } from "@/types";

describe("StudyHeatmap", () => {
  it("shows empty-state when cells array is empty", () => {
    render(<StudyHeatmap cells={[]} />);
    expect(screen.getByText(/Noch keine Aktivität/)).toBeInTheDocument();
  });

  it("renders grid with cells when data provided", () => {
    const cells: HeatmapCell[] = [
      { date: "2026-04-07", count: 3, level: 2 },
      { date: "2026-04-08", count: 0, level: 0 },
      { date: "2026-04-09", count: 7, level: 3 },
    ];
    const { container } = render(<StudyHeatmap cells={cells} />);

    // Should render the legend
    expect(screen.getByText("Weniger")).toBeInTheDocument();
    expect(screen.getByText("Mehr")).toBeInTheDocument();

    // Should have colored cells
    expect(container.querySelector(".bg-green-400")).not.toBeNull(); // level 2
    expect(container.querySelector(".bg-green-600")).not.toBeNull(); // level 3
  });

  it("renders level 0 cells with bg-gray-100", () => {
    const cells: HeatmapCell[] = [
      { date: "2026-04-09", count: 0, level: 0 },
    ];
    const { container } = render(<StudyHeatmap cells={cells} />);
    expect(container.querySelector(".bg-gray-100")).not.toBeNull();
  });

  it("renders level 4 cells with bg-green-800", () => {
    const cells: HeatmapCell[] = [
      { date: "2026-04-09", count: 15, level: 4 },
    ];
    const { container } = render(<StudyHeatmap cells={cells} />);
    expect(container.querySelector(".bg-green-800")).not.toBeNull();
  });

  it("renders weekday labels", () => {
    const cells: HeatmapCell[] = [
      { date: "2026-04-09", count: 1, level: 1 },
    ];
    render(<StudyHeatmap cells={cells} />);
    expect(screen.getByText("Mo")).toBeInTheDocument();
    expect(screen.getByText("Mi")).toBeInTheDocument();
    expect(screen.getByText("Fr")).toBeInTheDocument();
  });
});
