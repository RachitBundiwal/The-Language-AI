import { useState } from "react";
import { motion } from "framer-motion";
import { Volume2, ChevronDown, ChevronUp, Loader2 } from "lucide-react";
import { post } from "@/hooks/useApi";
import { API, BASE_URL } from "@/constants/api";
import type { DialogueTurn } from "@/types";

interface Props {
  dialogue: DialogueTurn[];
  lessonId: number;
}

interface TtsResponse {
  audio_url: string;
}

export function DialoguePlayer({ dialogue, lessonId }: Props) {
  const [expanded, setExpanded] = useState<Record<number, boolean>>({});
  const [loadingIdx, setLoadingIdx] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const toggle = (idx: number) =>
    setExpanded((prev) => ({ ...prev, [idx]: !prev[idx] }));

  const playAudio = async (idx: number, text: string) => {
    if (loadingIdx !== null) return;
    setError(null);
    setLoadingIdx(idx);
    try {
      const res = await post<TtsResponse>(API.tts, {
        text,
        language: "de",
        voice: "de-DE-KatjaNeural",
      });
      const url = res.audio_url.startsWith("http")
        ? res.audio_url
        : `${BASE_URL}${res.audio_url}`;
      const audio = new Audio(url);
      await audio.play();
    } catch (e) {
      setError("Audio konnte nicht geladen werden.");
      // eslint-disable-next-line no-console
      console.error("[TTS]", e);
    } finally {
      setLoadingIdx(null);
    }
  };

  if (dialogue.length === 0) {
    return (
      <div className="rounded-lg bg-gray-50 p-6 text-center text-sm text-gray-500">
        Kein Dialog für diese Lektion.
      </div>
    );
  }

  return (
    <div className="space-y-3" data-lesson-id={lessonId}>
      {error && (
        <div className="rounded-lg bg-danger-light px-3 py-2 text-xs text-danger">
          {error}
        </div>
      )}
      {dialogue.map((turn, idx) => {
        const isNative = turn.role === "native";
        const isOpen = !!expanded[idx];
        return (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.04 }}
            className={`flex ${isNative ? "justify-start" : "justify-end"}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl px-4 py-3 ${
                isNative
                  ? "rounded-tl-sm bg-blue-50 text-gray-900"
                  : "rounded-tr-sm bg-gray-100 text-gray-900"
              }`}
            >
              <div className="mb-1 text-[10px] font-bold uppercase tracking-wide text-gray-500">
                {isNative ? "Muttersprachler" : "Lernender"}
              </div>
              <div className="flex items-start gap-2">
                <p className="flex-1 text-sm font-bold leading-snug">
                  {turn.german}
                </p>
                <button
                  onClick={() => playAudio(idx, turn.german)}
                  disabled={loadingIdx !== null}
                  className="shrink-0 rounded-full bg-white/70 p-1.5 text-primary hover:bg-white disabled:opacity-50"
                  title="Anhören"
                  aria-label="Anhören"
                >
                  {loadingIdx === idx ? (
                    <Loader2 size={14} className="animate-spin" />
                  ) : (
                    <Volume2 size={14} />
                  )}
                </button>
              </div>
              <button
                onClick={() => toggle(idx)}
                className="mt-1 flex items-center gap-1 text-[11px] text-gray-500 hover:text-gray-700"
              >
                {isOpen ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
                {isOpen ? "Übersetzung ausblenden" : "Übersetzung anzeigen"}
              </button>
              {isOpen && (
                <p className="mt-1 text-xs italic text-gray-600">
                  {turn.english}
                </p>
              )}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
