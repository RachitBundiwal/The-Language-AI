import { create } from "zustand";
import type { CEFRLevel, ConversationMessage } from "@/types";

interface ConversationState {
  messages: ConversationMessage[];
  scenario: string;
  formality: "du" | "Sie";
  level: CEFRLevel;
  addMessage: (msg: ConversationMessage) => void;
  clearConversation: () => void;
  setScenario: (s: string) => void;
  setFormality: (f: "du" | "Sie") => void;
  setLevel: (l: CEFRLevel) => void;
}

export const useConversationStore = create<ConversationState>((set) => ({
  messages: [],
  scenario: "",
  formality: "du",
  level: "B1",
  addMessage: (msg) =>
    set((state) => ({ messages: [...state.messages, msg] })),
  clearConversation: () => set({ messages: [], scenario: "" }),
  setScenario: (s) => set({ scenario: s }),
  setFormality: (f) => set({ formality: f }),
  setLevel: (l) => set({ level: l }),
}));
