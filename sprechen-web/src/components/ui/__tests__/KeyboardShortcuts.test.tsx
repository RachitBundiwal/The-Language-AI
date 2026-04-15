import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, act, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { KeyboardShortcuts } from "../KeyboardShortcuts";

// Mock useNavigate
const mockNavigate = vi.fn();
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

function renderShortcuts() {
  return render(
    <MemoryRouter>
      <KeyboardShortcuts />
    </MemoryRouter>,
  );
}

describe("KeyboardShortcuts", () => {
  beforeEach(() => {
    mockNavigate.mockClear();
  });

  it("navigates on Alt+L", () => {
    renderShortcuts();
    act(() => {
      document.dispatchEvent(
        new KeyboardEvent("keydown", {
          key: "l",
          altKey: true,
          bubbles: true,
        }),
      );
    });
    expect(mockNavigate).toHaveBeenCalledWith("/lessons");
  });

  it("navigates on Alt+H to home", () => {
    renderShortcuts();
    act(() => {
      document.dispatchEvent(
        new KeyboardEvent("keydown", {
          key: "h",
          altKey: true,
          bubbles: true,
        }),
      );
    });
    expect(mockNavigate).toHaveBeenCalledWith("/");
  });

  it("opens modal on ? key", () => {
    renderShortcuts();
    act(() => {
      document.dispatchEvent(
        new KeyboardEvent("keydown", {
          key: "?",
          bubbles: true,
        }),
      );
    });
    expect(screen.getByText("Tastenkürzel")).toBeInTheDocument();
  });

  it("closes modal on Escape", () => {
    renderShortcuts();
    // Open
    act(() => {
      document.dispatchEvent(
        new KeyboardEvent("keydown", { key: "?", bubbles: true }),
      );
    });
    expect(screen.getByText("Tastenkürzel")).toBeInTheDocument();

    // Close
    act(() => {
      document.dispatchEvent(
        new KeyboardEvent("keydown", { key: "Escape", bubbles: true }),
      );
    });
    // Modal should be gone (AnimatePresence may leave it briefly, so check title gone)
    expect(screen.queryByText("Tastenkürzel")).not.toBeInTheDocument();
  });

  it("does NOT navigate when typing in an input", () => {
    const { container } = render(
      <MemoryRouter>
        <input data-testid="test-input" />
        <KeyboardShortcuts />
      </MemoryRouter>,
    );

    const input = screen.getByTestId("test-input");
    input.focus();

    // Dispatch keydown event with the input as target
    act(() => {
      fireEvent.keyDown(input, { key: "l", altKey: true });
    });

    expect(mockNavigate).not.toHaveBeenCalled();
  });
});
