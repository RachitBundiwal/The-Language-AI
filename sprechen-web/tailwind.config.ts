import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: "#2563EB", light: "#DBEAFE", dark: "#1D4ED8" },
        success: { DEFAULT: "#16A34A", light: "#DCFCE7" },
        warning: { DEFAULT: "#D97706", light: "#FEF3C7" },
        danger: { DEFAULT: "#DC2626", light: "#FEE2E2" },
        level: {
          a1: "#10B981",
          a2: "#059669",
          b1: "#3B82F6",
          b2: "#2563EB",
          c1: "#8B5CF6",
          c2: "#7C3AED",
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
