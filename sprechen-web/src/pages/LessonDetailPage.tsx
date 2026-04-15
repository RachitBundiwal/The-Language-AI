import { useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { ArrowLeft, BookOpen, MessageSquare, Sparkles, ListChecks } from "lucide-react";
import { get } from "@/hooks/useApi";
import { API } from "@/constants/api";
import { useCompleteLesson } from "@/hooks/useGamification";
import { LevelBadge } from "@/components/ui/LevelBadge";
import { DialoguePlayer } from "@/components/lessons/DialoguePlayer";
import { ExerciseRenderer } from "@/components/lessons/ExerciseRenderer";
import { Toast, type ToastKind } from "@/components/ui/Toast";
import type { LessonDetail } from "@/types";

type Tab = "overview" | "dialogue" | "grammar" | "exercises";

const TABS: { id: Tab; label: string; icon: typeof BookOpen }[] = [
  { id: "overview", label: "Übersicht", icon: BookOpen },
  { id: "dialogue", label: "Dialog", icon: MessageSquare },
  { id: "grammar", label: "Grammatik", icon: Sparkles },
  { id: "exercises", label: "Übungen", icon: ListChecks },
];

export function LessonDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const lessonId = Number(id);
  const [tab, setTab] = useState<Tab>("overview");
  const [exerciseIdx, setExerciseIdx] = useState(0);
  const [scores, setScores] = useState<number[]>([]);
  const [toast, setToast] = useState<{ open: boolean; msg: string; kind: ToastKind }>({
    open: false,
    msg: "",
    kind: "info",
  });

  const { data, isLoading, error } = useQuery<LessonDetail>({
    queryKey: ["lesson", lessonId],
    queryFn: () => get<LessonDetail>(API.lessonDetail(lessonId)),
    enabled: Number.isFinite(lessonId),
  });

  const completeMutation = useCompleteLesson();

  const handleComplete = (avgScore: number) => {
    completeMutation.mutate(
      { lessonId, score: avgScore },
      {
        onSuccess: () => {
          setToast({
            open: true,
            msg: "Lektion abgeschlossen! +XP",
            kind: "success",
          });
          setTimeout(() => navigate("/lessons"), 1500);
        },
        onError: () =>
          setToast({
            open: true,
            msg: "Fehler beim Speichern.",
            kind: "error",
          }),
      },
    );
  };

  if (isLoading) return <div className="text-sm text-gray-500">Lädt …</div>;
  if (error || !data) {
    return (
      <div className="rounded-lg bg-danger-light p-4 text-sm text-danger">
        Lektion konnte nicht geladen werden.
      </div>
    );
  }

  const handleAnswer = (result: { correct: boolean; score: number }) => {
    const nextScores = [...scores, result.score];
    setScores(nextScores);
    setTimeout(() => {
      if (exerciseIdx + 1 < data.exercises.length) {
        setExerciseIdx(exerciseIdx + 1);
      } else {
        const avg = nextScores.reduce((a, b) => a + b, 0) / nextScores.length;
        handleComplete(Math.round(avg));
      }
    }, 1200);
  };

  return (
    <div className="space-y-5">
      <Link
        to="/lessons"
        className="inline-flex items-center gap-1 text-sm text-gray-600 hover:text-primary"
      >
        <ArrowLeft size={16} />
        Zurück
      </Link>

      <div className="rounded-2xl bg-white p-5 shadow-sm">
        <div className="flex items-start justify-between gap-3">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{data.title}</h1>
            <p className="mt-1 text-sm text-gray-500">
              {data.scenario} · {data.estimated_minutes} Min
            </p>
          </div>
          <LevelBadge level={data.level} />
        </div>
      </div>

      <div className="flex gap-1 overflow-x-auto rounded-xl bg-white p-1 shadow-sm">
        {TABS.map(({ id: tabId, label, icon: Icon }) => (
          <button
            key={tabId}
            onClick={() => setTab(tabId)}
            className={`flex flex-1 items-center justify-center gap-1.5 whitespace-nowrap rounded-lg px-3 py-2 text-xs font-bold transition-colors ${
              tab === tabId
                ? "bg-primary text-white"
                : "text-gray-600 hover:bg-gray-100"
            }`}
          >
            <Icon size={14} />
            {label}
          </button>
        ))}
      </div>

      <motion.div
        key={tab}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-2xl bg-white p-5 shadow-sm"
      >
        {tab === "overview" && (
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-bold uppercase text-gray-500">
                Lernziele
              </h3>
              <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-gray-700">
                {data.learning_objectives.map((obj, i) => (
                  <li key={i}>{obj}</li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-bold uppercase text-gray-500">
                Kulturhinweis
              </h3>
              <p className="mt-2 rounded-lg bg-yellow-50 p-3 text-sm text-gray-700">
                {data.cultural_note}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-bold uppercase text-gray-500">
                Vokabular ({data.vocabulary_list.length})
              </h3>
              <div className="mt-2 grid gap-2 md:grid-cols-2">
                {data.vocabulary_list.map((v, i) => (
                  <div
                    key={i}
                    className="rounded-lg border border-gray-200 p-3"
                  >
                    <p className="font-bold text-gray-900">{v.word}</p>
                    <p className="text-xs text-gray-500">{v.translation}</p>
                    {v.example_sentence && (
                      <p className="mt-1 text-xs italic text-gray-600">
                        {v.example_sentence}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {tab === "dialogue" && (
          <DialoguePlayer dialogue={data.dialogue} lessonId={data.id} />
        )}

        {tab === "grammar" && (
          <div className="space-y-4">
            <h3 className="text-lg font-bold text-gray-900">
              {data.grammar_focus.rule_name}
            </h3>
            <p className="text-sm text-gray-700">
              {data.grammar_focus.explanation}
            </p>
            <div className="rounded-lg bg-blue-50 p-3 font-mono text-sm text-blue-900">
              {data.grammar_focus.formula}
            </div>
            <div>
              <h4 className="text-xs font-bold uppercase text-gray-500">
                Beispiele
              </h4>
              <div className="mt-2 space-y-2">
                {data.grammar_focus.examples.map((ex, i) => (
                  <div key={i} className="rounded-lg border border-gray-200 p-3">
                    <p className="font-bold text-gray-900">{ex.german}</p>
                    <p className="text-xs text-gray-500">{ex.english}</p>
                    {ex.breakdown && (
                      <p className="mt-1 text-xs italic text-gray-600">
                        {ex.breakdown}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
            {data.grammar_focus.common_mistakes.length > 0 && (
              <div>
                <h4 className="text-xs font-bold uppercase text-gray-500">
                  Häufige Fehler
                </h4>
                <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-gray-700">
                  {data.grammar_focus.common_mistakes.map((m, i) => (
                    <li key={i}>{m}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {tab === "exercises" && data.exercises.length > 0 && (
          <div>
            <div className="mb-4 flex items-center justify-between text-xs text-gray-500">
              <span>
                Übung {exerciseIdx + 1} / {data.exercises.length}
              </span>
              <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-gray-200 ml-3">
                <div
                  className="h-full bg-primary transition-all"
                  style={{
                    width: `${((exerciseIdx + 1) / data.exercises.length) * 100}%`,
                  }}
                />
              </div>
            </div>
            <ExerciseRenderer
              key={exerciseIdx}
              exercise={data.exercises[exerciseIdx]}
              lessonId={data.id}
              onAnswer={handleAnswer}
            />
          </div>
        )}
        {tab === "exercises" && data.exercises.length === 0 && (
          <p className="text-sm text-gray-500">Keine Übungen vorhanden.</p>
        )}
      </motion.div>

      <Toast
        open={toast.open}
        kind={toast.kind}
        message={toast.msg}
        onClose={() => setToast({ ...toast, open: false })}
      />
    </div>
  );
}
