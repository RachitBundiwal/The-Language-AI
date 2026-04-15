import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery, useMutation } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { Award, Clock, ChevronRight } from "lucide-react";
import { get, post } from "@/hooks/useApi";
import { API } from "@/constants/api";
import { useExamReadiness, useExamHistory } from "@/hooks/useProgress";
import { useExamCompleted } from "@/hooks/useGamification";
import { LevelBadge } from "@/components/ui/LevelBadge";
import type {
  CEFRLevel,
  ExamPaper,
  ExamResult,
  ReadingPart,
  ListeningPart,
} from "@/types";

const SECTIONS = ["Lesen", "Hören", "Schreiben", "Sprechen"] as const;
type Section = (typeof SECTIONS)[number];

export function ExamPage() {
  const [level, setLevel] = useState<CEFRLevel>("A1");
  const [section, setSection] = useState<Section | null>(null);
  const navigate = useNavigate();

  const readiness = useExamReadiness();
  const history = useExamHistory();
  const examCompleted = useExamCompleted();

  const paperQuery = useQuery<ExamPaper>({
    queryKey: ["exam-paper", level, section],
    queryFn: () => get<ExamPaper>(API.examPaper(level, section as string)),
    enabled: section !== null,
  });

  const submitMutation = useMutation({
    mutationFn: (payload: {
      level: CEFRLevel;
      answers: Record<number, number>;
    }) =>
      post<ExamResult>(API.submitExam(section as string), {
        level: payload.level,
        answers: payload.answers,
      }),
    onSuccess: (data) => {
      examCompleted.mutate();
      navigate("/exam/result", { state: data });
    },
  });

  const [answers, setAnswers] = useState<Record<number, number>>({});

  const startExam = (sec: Section) => {
    setSection(sec);
    setAnswers({});
  };

  if (section && paperQuery.data) {
    return (
      <ExamRunner
        paper={paperQuery.data}
        section={section}
        answers={answers}
        setAnswers={setAnswers}
        onSubmit={() => submitMutation.mutate({ level, answers })}
        onCancel={() => setSection(null)}
        submitting={submitMutation.isPending}
      />
    );
  }

  return (
    <div className="space-y-5">
      <div className="rounded-2xl bg-gradient-to-br from-primary to-primary-dark p-6 text-white">
        <div className="flex items-center gap-2">
          <Award size={24} />
          <h2 className="text-xl font-bold">Goethe Institut Prüfung</h2>
        </div>
        {readiness.data && (
          <div className="mt-4">
            <div className="flex items-center justify-between text-sm">
              <span>Bereitschaft</span>
              <span className="font-bold">
                {Math.round(readiness.data.overall)}%
              </span>
            </div>
            <div className="mt-1 h-2 overflow-hidden rounded-full bg-white/30">
              <div
                className="h-full bg-white"
                style={{ width: `${Math.round(readiness.data.overall)}%` }}
              />
            </div>
            <p className="mt-2 text-xs opacity-90">
              {readiness.data.recommendation}
            </p>
          </div>
        )}
      </div>

      <div className="rounded-2xl bg-white p-5 shadow-sm">
        <p className="mb-3 text-xs font-bold uppercase text-gray-500">Niveau</p>
        <div className="flex flex-wrap gap-2">
          {(["A1", "A2", "B1", "B2"] as CEFRLevel[]).map((l) => (
            <button
              key={l}
              onClick={() => setLevel(l)}
              className={`rounded-full px-4 py-1.5 text-sm font-bold transition-colors ${
                level === l
                  ? "bg-primary text-white"
                  : "border border-gray-300 bg-white text-gray-700"
              }`}
            >
              {l}
            </button>
          ))}
        </div>
      </div>

      <div className="grid gap-3 md:grid-cols-2">
        {SECTIONS.map((s) => (
          <button
            key={s}
            onClick={() => startExam(s)}
            className="flex items-center justify-between rounded-2xl border-2 border-gray-200 bg-white p-5 text-left hover:border-primary hover:shadow-md"
          >
            <div>
              <p className="text-lg font-bold text-gray-900">{s}</p>
              <p className="mt-1 text-xs text-gray-500">{level} · Goethe Format</p>
            </div>
            <ChevronRight className="text-primary" />
          </button>
        ))}
      </div>

      {history.data && history.data.length > 0 && (
        <div className="rounded-2xl bg-white p-5 shadow-sm">
          <h3 className="mb-3 text-base font-bold text-gray-900">Verlauf</h3>
          <div className="space-y-2">
            {history.data.slice(0, 5).map((h) => (
              <div
                key={h.id}
                className="flex items-center justify-between rounded-lg border border-gray-200 p-3"
              >
                <div className="flex items-center gap-3">
                  <LevelBadge level={h.level as CEFRLevel} size="sm" />
                  <span className="text-sm font-medium text-gray-900">
                    {h.section}
                  </span>
                </div>
                <div className="flex items-center gap-3 text-xs">
                  <span
                    className={`font-bold ${h.passed ? "text-success" : "text-danger"}`}
                  >
                    {Math.round(h.percentage)}%
                  </span>
                  <Clock size={12} className="text-gray-400" />
                  <span className="text-gray-500">
                    {Math.round(h.duration_seconds / 60)} min
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

interface RunnerProps {
  paper: ExamPaper;
  section: Section;
  answers: Record<number, number>;
  setAnswers: (a: Record<number, number>) => void;
  onSubmit: () => void;
  onCancel: () => void;
  submitting: boolean;
}

function ExamRunner({
  paper,
  section,
  answers,
  setAnswers,
  onSubmit,
  onCancel,
  submitting,
}: RunnerProps) {
  // Build a flat list of (qid, question, options, partTitle) across parts
  const flat: Array<{
    qid: number;
    question: string;
    options: string[];
    partLabel: string;
    context?: string;
  }> = [];
  let qid = 0;
  for (const part of paper.parts) {
    const p = part as unknown as ReadingPart | ListeningPart;
    const ctx =
      "texts" in p
        ? p.texts.map((t) => `${t.title}\n${t.text}`).join("\n\n")
        : "scripts" in p
          ? p.scripts.map((s) => `${s.title}\n${s.script}`).join("\n\n")
          : undefined;
    for (const q of p.questions) {
      flat.push({
        qid,
        question: q.question,
        options: q.options,
        partLabel: `Teil ${p.part_number}`,
        context: ctx,
      });
      qid++;
    }
  }

  if (section === "Schreiben" || section === "Sprechen") {
    return (
      <div className="rounded-2xl bg-white p-6 shadow-sm">
        <p className="text-sm text-gray-600">
          Diese Sektion ({section}) erfordert eine längere freie Antwort und ist
          in dieser Demo noch nicht interaktiv.
        </p>
        <button
          onClick={onCancel}
          className="mt-4 rounded-lg bg-primary px-5 py-2 text-sm font-bold text-white hover:bg-primary-dark"
        >
          Zurück
        </button>
      </div>
    );
  }

  const allAnswered = flat.every((f) => answers[f.qid] !== undefined);

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase text-gray-500">
            {paper.level} · {paper.section}
          </p>
          <p className="text-sm font-bold text-gray-900">
            {paper.time_limit_minutes} Min · {paper.max_score} Punkte
          </p>
        </div>
        <button
          onClick={onCancel}
          className="text-xs text-gray-500 hover:text-danger"
        >
          Abbrechen
        </button>
      </div>

      <p className="rounded-lg bg-blue-50 p-3 text-sm text-gray-700">
        {paper.instructions}
      </p>

      {paper.parts.map((part, pIdx) => {
        const p = part as unknown as ReadingPart | ListeningPart;
        return (
          <motion.div
            key={pIdx}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-3 rounded-2xl bg-white p-5 shadow-sm"
          >
            <h3 className="text-base font-bold text-gray-900">
              Teil {p.part_number}
            </h3>
            <p className="text-xs text-gray-500">{p.instruction}</p>

            {"texts" in p &&
              p.texts.map((t, ti) => (
                <div key={ti} className="rounded-lg bg-gray-50 p-3">
                  <p className="text-xs font-bold text-gray-700">{t.title}</p>
                  <p className="mt-1 whitespace-pre-line text-sm text-gray-800">
                    {t.text}
                  </p>
                </div>
              ))}

            {"scripts" in p &&
              p.scripts.map((s, si) => (
                <div key={si} className="rounded-lg bg-gray-50 p-3">
                  <p className="text-xs font-bold text-gray-700">{s.title}</p>
                  <p className="mt-1 text-xs italic text-gray-500">
                    {s.speaker_context}
                  </p>
                  <p className="mt-2 whitespace-pre-line text-sm text-gray-800">
                    {s.script}
                  </p>
                </div>
              ))}

            <div className="space-y-3">
              {p.questions.map((q, qi) => {
                const flatItem = flat.find(
                  (f) =>
                    f.partLabel === `Teil ${p.part_number}` &&
                    f.question === q.question,
                );
                if (!flatItem) return null;
                return (
                  <div key={qi} className="rounded-lg border border-gray-200 p-3">
                    <p className="text-sm font-medium text-gray-900">
                      {qi + 1}. {q.question}
                    </p>
                    <div className="mt-2 grid gap-2 md:grid-cols-2">
                      {q.options.map((opt, oi) => {
                        const picked = answers[flatItem.qid] === oi;
                        return (
                          <button
                            key={oi}
                            onClick={() =>
                              setAnswers({ ...answers, [flatItem.qid]: oi })
                            }
                            className={`rounded-lg border-2 px-3 py-2 text-left text-sm ${
                              picked
                                ? "border-primary bg-primary-light"
                                : "border-gray-200 bg-white hover:border-primary"
                            }`}
                          >
                            {opt}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>
        );
      })}

      <button
        onClick={onSubmit}
        disabled={!allAnswered || submitting}
        className="w-full rounded-lg bg-primary px-5 py-3 text-sm font-bold text-white hover:bg-primary-dark disabled:opacity-50"
      >
        {submitting ? "Wird ausgewertet …" : "Abgeben"}
      </button>
    </div>
  );
}
