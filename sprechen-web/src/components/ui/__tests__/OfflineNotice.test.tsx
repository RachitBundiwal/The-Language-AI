import { describe, it, expect, beforeEach } from "vitest";
import { render, screen, act } from "@testing-library/react";
import { OfflineNotice } from "../OfflineNotice";

describe("OfflineNotice", () => {
  beforeEach(() => {
    // Reset to online
    Object.defineProperty(navigator, "onLine", {
      writable: true,
      value: true,
    });
  });

  it("does not render when online", () => {
    render(<OfflineNotice />);
    expect(
      screen.queryByText(/Keine Internetverbindung/),
    ).not.toBeInTheDocument();
  });

  it("shows banner when offline event fires", () => {
    render(<OfflineNotice />);

    act(() => {
      Object.defineProperty(navigator, "onLine", {
        writable: true,
        value: false,
      });
      window.dispatchEvent(new Event("offline"));
    });

    expect(
      screen.getByText(/Keine Internetverbindung/),
    ).toBeInTheDocument();
  });

  it("hides banner when online event fires after offline", () => {
    render(<OfflineNotice />);

    act(() => {
      window.dispatchEvent(new Event("offline"));
    });

    act(() => {
      window.dispatchEvent(new Event("online"));
    });

    expect(
      screen.queryByText(/Keine Internetverbindung/),
    ).not.toBeInTheDocument();
  });
});
