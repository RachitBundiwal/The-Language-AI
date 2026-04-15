import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Send, Trash2, Loader2, Mic, Square } from "lucide-react";
import { post, postForm } from "@/hooks/useApi";
import { API } from "@/constants/api";
import { useConversationStore } from "@/store/conversationStore";
import { useAudioRecorder } from "@/hooks/useAudioRecorder";
import { ALL_LEVELS, SCENARIO_LABEL, SCENARIO_EMOJI } from "@/constants/levels";
import type {
  CEFRLevel,
  ConversationResponse,
  TranscriptionResponse,
} from "@/types";

const SCENARIOS = [
  "free",
  "bakery",
  "doctor",
  "restaurant",
  "train_station",
  "job_interview",
  "landlord",
  "supermarket",
];

export function ConversationPage() {
  const {
    messages,
    scenario,
    formality,
    level,
    addMessage,
    clearConversation,
    setScenario,
    setFormality,
    setLevel,
  } = useConversationStore();
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [latest, setLatest] = useState<ConversationResponse | null>(null);
  const recorder = useAudioRecorder();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  const send = async (text: string) => {
    if (!text.trim() || busy) return;
    addMessage({ role: "user", content: text });
    setInput("");
    setBusy(true);
    try {
      const res = await post<ConversationResponse>(API.chat, {
        message: text,
        scenario: scenario || "free",
        formality,
        level,
        history: messages,
      });
      addMessage({ role: "assistant", content: res.reply });
      setLatest(res);
    } catch {
      addMessage({
        role: "assistant",
        content: "Entschuldigung, da ist etwas schiefgegangen.",
      });
    } finally {
      setBusy(false);
    }
  };

  const handleVoiceStop = async () => {
    try {
      const blob = await recorder.stopRecording();
      const fd = new FormData();
      fd.append("audio", blob, "rec.webm");
      const tx = await postForm<TranscriptionResponse>(API.transcribe, fd);
      if (tx.transcript.trim()) await send(tx.transcript);
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
    }
  };

  return (
    <div className="grid gap-5 lg:grid-cols-[1fr_300px]">
      <div className="flex h-[calc(100vh-180px)] flex-col rounded-2xl bg-white shadow-sm">
        <div className="flex items-center justify-between border-b border-gray-200 p-3">
          <div className="flex items-center gap-2 text-sm">
            <span className="text-xl">
              {SCENARIO_EMOJI[scenario] ?? "💬"}
            </span>
            <span className="font-bold text-gray-900">
              {SCENARIO_LABEL[scenario] ?? "Freies Gespräch"}
            </span>
          </div>
          <button
            onClick={() => {
              clearConversation();
              setLatest(null);
            }}
            className="flex items-center gap-1 text-xs text-gray-500 hover:text-danger"
          >
            <Trash2 size={14} />
            Löschen
          </button>
        </div>

        <div ref={scrollRef} className="flex-1 space-y-3 overflow-y-auto p-4">
          {messages.length === 0 && (
            <div className="flex h-full items-center justify-center text-sm text-gray-400">
              Beginne ein Gespräch …
            </div>
          )}
          {messages.map((m, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm ${
                  m.role === "user"
                    ? "rounded-tr-sm bg-primary text-white"
                    : "rounded-tl-sm bg-gray-100 text-gray-900"
                }`}
              >
                {m.content}
              </div>
            </motion.div>
          ))}
          {busy && (
            <div className="flex justify-start">
              <div className="rounded-2xl bg-gray-100 px-4 py-2 text-sm text-gray-500">
                <Loader2 size={14} className="inline animate-spin" /> ...
              </div>
            </div>
          )}
        </div>

        <div className="flex items-center gap-2 border-t border-gray-200 p-3">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send(input)}
            placeholder="Schreibe auf Deutsch …"
            className="flex-1 rounded-lg border-2 border-gray-200 px-3 py-2 text-sm focus:border-primary focus:outline-none"
          />
          {!recorder.isRecording ? (
            <button
              onClick={() => recorder.startRecording()}
              disabled={busy}
              className="rounded-lg bg-gray-100 p-2 text-gray-700 hover:bg-gray-200 disabled:opacity-50"
              title="Sprechen"
            >
              <Mic size={18} />
            </button>
          ) : (
            <button
              onClick={handleVoiceStop}
              className="rounded-lg bg-danger p-2 text-white"
            >
              <Square size={18} />
            </button>
          )}
          <button
            onClick={() => send(input)}
            disabled={busy || !input.trim()}
            className="rounded-lg bg-primary p-2 text-white hover:bg-primary-dark disabled:opacity-50"
          >
            <Send size={18} />
          </button>
        </div>
      </div>

      <aside className="space-y-4">
        <div className="rounded-2xl bg-white p-4 shadow-sm">
          <p className="mb-2 text-xs font-bold uppercase text-gray-500">
            Szenario
          </p>
          <select
            value={scenario || "free"}
            onChange={(e) => setScenario(e.target.value)}
            className="w-full rounded-lg border-2 border-gray-200 px-2 py-2 text-sm focus:border-primary focus:outline-none"
          >
            {SCENARIOS.map((s) => (
              <option key={s} value={s}>
                {SCENARIO_LABEL[s] ?? s}
              </option>
            ))}
          </select>

          <p className="mb-2 mt-3 text-xs font-bold uppercase text-gray-500">
            Niveau
          </p>
          <select
            value={level}
            onChange={(e) => setLevel(e.target.value as CEFRLevel)}
            className="w-full rounded-lg border-2 border-gray-200 px-2 py-2 text-sm focus:border-primary focus:outline-none"
          >
            {ALL_LEVELS.map((l) => (
              <option key={l} value={l}>
                {l}
              </option>
            ))}
          </select>

          <p className="mb-2 mt-3 text-xs font-bold uppercase text-gray-500">
            Anrede
          </p>
          <div className="flex gap-2">
            {(["du", "Sie"] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFormality(f)}
                className={`flex-1 rounded-lg border-2 px-3 py-1.5 text-xs font-bold ${
                  formality === f
                    ? "border-primary bg-primary text-white"
                    : "border-gray-200 bg-white text-gray-700"
                }`}
              >
                {f}
              </button>
            ))}
          </div>
        </div>

        {latest && latest.corrections.length > 0 && (
          <div className="rounded-2xl bg-white p-4 shadow-sm">
            <p className="mb-2 text-xs font-bold uppercase text-gray-500">
              Korrekturen
            </p>
            <div className="space-y-2">
              {latest.corrections.map((c, i) => (
                <div key={i} className="rounded-lg bg-yellow-50 p-2 text-xs">
                  <p className="text-danger line-through">{c.original}</p>
                  <p className="font-bold text-success">{c.corrected}</p>
                  <p className="mt-1 italic text-gray-600">{c.explanation}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {latest && latest.new_vocabulary.length > 0 && (
          <div className="rounded-2xl bg-white p-4 shadow-sm">
            <p className="mb-2 text-xs font-bold uppercase text-gray-500">
              Neue Wörter
            </p>
            <div className="space-y-2">
              {latest.new_vocabulary.map((v, i) => (
                <div key={i} className="rounded-lg bg-blue-50 p-2 text-xs">
                  <p className="font-bold text-gray-900">{v.word}</p>
                  <p className="text-gray-600">{v.translation}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </aside>
    </div>
  );
}
