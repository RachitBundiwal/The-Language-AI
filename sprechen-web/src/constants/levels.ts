import type { CEFRLevel } from "@/types";

export const ALL_LEVELS: CEFRLevel[] = ["A1", "A2", "B1", "B2", "C1", "C2"];

export const LEVEL_COLORS: Record<CEFRLevel, string> = {
  A1: "#10B981",
  A2: "#059669",
  B1: "#3B82F6",
  B2: "#2563EB",
  C1: "#8B5CF6",
  C2: "#7C3AED",
};

export const LEVEL_BG_CLASS: Record<CEFRLevel, string> = {
  A1: "bg-level-a1",
  A2: "bg-level-a2",
  B1: "bg-level-b1",
  B2: "bg-level-b2",
  C1: "bg-level-c1",
  C2: "bg-level-c2",
};

export const SCENARIO_EMOJI: Record<string, string> = {
  bakery: "🥖",
  doctor: "🏥",
  restaurant: "🍽",
  train_station: "🚂",
  job_interview: "💼",
  landlord: "🏠",
  supermarket: "🛒",
  free: "💬",
};

export const SCENARIO_LABEL: Record<string, string> = {
  bakery: "Bakery",
  doctor: "Doctor's Office",
  restaurant: "Restaurant",
  train_station: "Train Station",
  job_interview: "Job Interview",
  landlord: "Apartment",
  supermarket: "Supermarket",
  free: "Free Conversation",
};

export const XP_PER_LEVEL: Record<CEFRLevel, number> = {
  A1: 500,
  A2: 1000,
  B1: 2000,
  B2: 3500,
  C1: 5500,
  C2: 8000,
};
