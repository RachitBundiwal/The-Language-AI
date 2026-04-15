import { useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Mic, Square, ArrowLeft, Volume2, Loader2 } from "lucide-react";
import { useAudioRecorder } from "@/hooks/useAudioRecorder";
import { postForm, post } from "@/hooks/useApi";
import { API, BASE_URL } from "@/constants/api";
import { useSavePronunciation } from "@/hooks/useGamification";
import { WaveformDisplay } from "@/components/ui/WaveformDisplay";
import { ScoreRing } from "@/components/ui/ScoreRing";
import { PronunciationMeter } from "@/components/ui/PronunciationMeter";
import type { VoiceExerciseResult } from "@/types";

export function VoiceExercisePage() {
  const [params] = useSearchParams();
  const referenceText = params.get("text") ?? "Guten Tag, wie geht es Ihnen?";
  const lessonId = params.get("lesson");

  const recorder = useAudioRecorder();
  const savePron = useSavePronunciation();
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<VoiceExerciseResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [ttsLoading, setTtsLoading] = useState(false);

  const handleStop = async () => {
    setError(null);
    try {
      const blob = await recorder.stopRecording();
      setBusy(true);
      const fd = new FormData();
      fd.append("audio", blob, "rec.webm");
      fd.append("reference_text", referenceText);
      if (lessonId) fd.append("lesson_id", lessonId);
      const res = await postForm<VoiceExerciseResult>(API.fullExercise, fd);
      setResult(res);
      savePron.mutate({
        reference_text: referenceText,
        pronunciation: res.pronunciation,
        lesson_id: lessonId ? Number(lessonId) : undefined,
      });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Fehler bei der Auswertung.");
    } finally {
      setBusy(false);
    }
  };

  const playReference = async () => {
    setTtsLoading(true);
    try {
      const res = await post<{ audio_url: string }>(API.tts, {
        text: referenceText,
        language: "de",
      });
      const url = res.audio_url.startsWith("http")
        ? res.audio_url
        : `${BASE_URL}${res.audio_url}`;
      await new Audio(url).play();
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
    } finally {
      setTtsLoading(false);
    }
  };

  const reset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="space-y-5">
      <Link
        to={lessonId ? `/lessons/${lessonId}` : "/lessons"}
        className="inline-flex items-center gap-1 text-sm text-gray-600 hover:text-primary"
      >
        <ArrowLeft size={16} />
        Zurück
      </Link>

      <div className="rounded-2xl bg-white p-6 shadow-sm">
        <p className="text-xs font-bold uppercase text-gray-500">Sprich nach</p>
        <p className="mt-2 text-2xl font-bold text-gray-900">{referenceText}</p>
        <button
          onClick={playReference}
          disabled={ttsLoading}
          className="mt-4 inline-flex items-center gap-2 rounded-lg border-2 border-primary px-4 py-2 text-sm font-bold text-primary hover:bg-primary-light disabled:opacity-50"
        >
          {ttsLoading ? (
            <Loader2 size={16} className="animate-spin" />
          ) : (
            <Volume2 size={16} />
          )}
          Vorhören
        </button>
      </div>

      {!result && (
        <div className="flex flex-col items-center gap-4 rounded-2xl bg-white p-8 shadow-sm">
          <WaveformDisplay audioLevel={recorder.audioLevel} active={recorder.isRecording} />
          {recorder.error && (
            <p className="text-sm text-danger">{recorder.error}</p>
          )}
          {error && <p className="text-sm text-danger">{error}</p>}
          {!recorder.isRecording ? (
            <motion.button
              whileTap={{ scale: 0.95 }}
              onClick={() => recorder.startRecording()}
              disabled={busy}
              className="flex h-20 w-20 items-center justify-center rounded-full bg-primary text-white shadow-lg hover:bg-primary-dark disabled:opacity-50"
            >
              {busy ? <Loader2 className="animate-spin" /> : <Mic size={32} />}
            </motion.button>
          ) : (
            <motion.button
              whileTap={{ scale: 0.95 }}
              onClick={handleStop}
              className="flex h-20 w-20 items-center justify-center rounded-full bg-danger text-white shadow-lg"
            >
              <Square size={28} />
            </motion.button>
          )}
          <p className="text-xs text-gray-500">
            {busy
              ? "Wird ausgewertet …"
              : recorder.isRecording
                ? "Aufnahme läuft … Tipp zum Beenden"
                : "Tipp zum Aufnehmen"}
          </p>
        </div>
      )}

      {result && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          <div className="flex flex-col items-center gap-3 rounded-2xl bg-white p-6 shadow-sm">
            <ScoreRing score={Math.round(result.pronunciation.overall_score)} />
            <p className="text-xs text-gray-500">Gesamtbewertung</p>
          </div>

          <div className="rounded-2xl bg-white p-5 shadow-sm">
            <p className="text-xs font-bold uppercase text-gray-500">
              Du hast gesagt
            </p>
            <p className="mt-1 text-base text-gray-900">
              {result.transcription.transcript || "(nichts erkannt)"}
            </p>
          </div>

          <div className="space-y-3 rounded-2xl bg-white p-5 shadow-sm">
            <PronunciationMeter
              label="Aussprache"
              score={Math.round(result.pronunciation.pronunciation_score)}
            />
            <PronunciationMeter
              label="Flüssigkeit"
              score={Math.round(result.pronunciation.fluency_score)}
            />
            <PronunciationMeter
              label="Genauigkeit"
              score={Math.round(result.pronunciation.accuracy_score)}
            />
            <PronunciationMeter
              label="Vollständigkeit"
              score={Math.round(result.pronunciation.completeness_score)}
            />
          </div>

          {result.pronunciation.problem_phonemes.length > 0 && (
            <div className="rounded-2xl bg-white p-5 shadow-sm">
              <p className="text-xs font-bold uppercase text-gray-500">
                Schwierige Laute
              </p>
              <div className="mt-2 flex flex-wrap gap-2">
                {result.pronunciation.problem_phonemes.map((p) => (
                  <span
                    key={p}
                    className="rounded-full bg-danger-light px-3 py-1 text-xs font-bold text-danger"
                  >
                    /{p}/
                  </span>
                ))}
              </div>
            </div>
          )}

          {result.pronunciation.ai_feedback && (
            <div className="rounded-2xl bg-blue-50 p-5">
              <p className="text-xs font-bold uppercase text-primary-dark">
                Feedback
              </p>
              <p className="mt-2 text-sm text-gray-800">
                {result.pronunciation.ai_feedback}
              </p>
            </div>
          )}

          <button
            onClick={reset}
            className="w-full rounded-lg bg-primary px-5 py-3 text-sm font-bold text-white hover:bg-primary-dark"
          >
            Nochmal versuchen
          </button>
        </motion.div>
      )}
    </div>
  );
}
