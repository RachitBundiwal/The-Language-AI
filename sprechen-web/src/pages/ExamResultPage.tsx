import { useLocation, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Award, ArrowLeft, Check, X } from "lucide-react";
import { ScoreRing } from "@/components/ui/ScoreRing";
import type { ExamResult } from "@/types";

export function ExamResultPage() {
  const { state } = useLocation() as { state: ExamResult | null };

  if (!state) {
    return (
      <div className="rounded-lg bg-gray-50 p-6 text-center text-sm text-gray-500">
        Kein Ergebnis vorhanden.{" "}
        <Link to="/exam" className="text-primary underline">
          Zur Prüfung
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-5">
      <Link
        to="/exam"
        className="inline-flex items-center gap-1 text-sm text-gray-600 hover:text-primary"
      >
        <ArrowLeft size={16} />
        Zurück zur Prüfungsübersicht
      </Link>

      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="flex flex-col items-center gap-4 rounded-2xl bg-white p-8 shadow-sm"
      >
        <Award size={36} className="text-primary" />
        <h1 className="text-2xl font-bold text-gray-900">
          {state.level} · {state.section}
        </h1>
        <ScoreRing score={Math.round(state.percentage)} />
        <div
          className={`flex items-center gap-2 rounded-full px-4 py-1.5 text-sm font-bold ${
            state.passed
              ? "bg-success-light text-success"
              : "bg-danger-light text-danger"
          }`}
        >
          {state.passed ? <Check size={16} /> : <X size={16} />}
          {state.grade}
        </div>
        <p className="text-sm text-gray-600">
          {Math.round(state.score)} / {state.max_score} Punkte
        </p>
      </motion.div>

      {state.feedback && (
        <div className="rounded-2xl bg-blue-50 p-5">
          <p className="text-xs font-bold uppercase text-primary-dark">
            Feedback
          </p>
          <p className="mt-2 text-sm text-gray-800">{state.feedback}</p>
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        {state.strengths.length > 0 && (
          <div className="rounded-2xl bg-white p-5 shadow-sm">
            <p className="text-xs font-bold uppercase text-success">Stärken</p>
            <ul className="mt-2 space-y-1 text-sm text-gray-700">
              {state.strengths.map((s, i) => (
                <li key={i} className="flex items-start gap-2">
                  <Check size={14} className="mt-0.5 text-success" />
                  {s}
                </li>
              ))}
            </ul>
          </div>
        )}
        {state.improvements.length > 0 && (
          <div className="rounded-2xl bg-white p-5 shadow-sm">
            <p className="text-xs font-bold uppercase text-orange-600">
              Verbesserungen
            </p>
            <ul className="mt-2 space-y-1 text-sm text-gray-700">
              {state.improvements.map((s, i) => (
                <li key={i} className="flex items-start gap-2">
                  <X size={14} className="mt-0.5 text-orange-500" />
                  {s}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
