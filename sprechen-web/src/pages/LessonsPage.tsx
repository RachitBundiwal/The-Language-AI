import { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { CheckCircle2, Clock } from "lucide-react";
import { useLessons } from "@/hooks/useProgress";
import { LevelBadge } from "@/components/ui/LevelBadge";
import { ALL_LEVELS, SCENARIO_EMOJI, SCENARIO_LABEL } from "@/constants/levels";
import type { CEFRLevel, LessonSummary } from "@/types";

type Filter = "all" | CEFRLevel;

export function LessonsPage() {
  const [filter, setFilter] = useState<Filter>("all");
  const { data, isLoading, error } = useLessons(filter);

  const lessons: LessonSummary[] = (() => {
    if (!data) return [];
    if (Array.isArray(data)) return data;
    return Object.values(data).flat();
  })();

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap gap-2">
        <FilterChip
          active={filter === "all"}
          label="Alle"
          onClick={() => setFilter("all")}
        />
        {ALL_LEVELS.map((lvl) => (
          <FilterChip
            key={lvl}
            active={filter === lvl}
            label={lvl}
            onClick={() => setFilter(lvl)}
          />
        ))}
      </div>

      {isLoading && <div className="text-sm text-gray-500">Lädt …</div>}
      {error && (
        <div className="rounded-lg bg-danger-light p-4 text-sm text-danger">
          Fehler beim Laden der Lektionen.
        </div>
      )}
      {!isLoading && lessons.length === 0 && (
        <div className="rounded-lg bg-gray-50 p-8 text-center text-sm text-gray-500">
          Keine Lektionen gefunden.
        </div>
      )}

      <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
        {lessons.map((lesson, idx) => (
          <motion.div
            key={lesson.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.02 }}
          >
            <LessonCard lesson={lesson} />
          </motion.div>
        ))}
      </div>
    </div>
  );
}

function FilterChip({
  active,
  label,
  onClick,
}: {
  active: boolean;
  label: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`rounded-full px-4 py-1.5 text-xs font-bold transition-colors ${
        active
          ? "bg-primary text-white"
          : "border border-gray-300 bg-white text-gray-700 hover:border-primary"
      }`}
    >
      {label}
    </button>
  );
}

function LessonCard({ lesson }: { lesson: LessonSummary }) {
  const emoji = SCENARIO_EMOJI[lesson.scenario] ?? "📘";
  const label = SCENARIO_LABEL[lesson.scenario] ?? lesson.scenario;
  return (
    <Link
      to={`/lessons/${lesson.id}`}
      className="block rounded-xl border-2 border-gray-200 bg-white p-4 transition-all hover:border-primary hover:shadow-md"
    >
      <div className="flex items-start justify-between">
        <div className="text-3xl">{emoji}</div>
        <LevelBadge level={lesson.level} size="sm" />
      </div>
      <h3 className="mt-3 text-base font-bold text-gray-900">{lesson.title}</h3>
      <p className="mt-1 text-xs text-gray-500">{label}</p>
      <div className="mt-3 flex items-center justify-between text-xs text-gray-600">
        <span className="flex items-center gap-1">
          <Clock size={12} />
          {lesson.estimated_minutes} Min
        </span>
        {lesson.completed && (
          <span className="flex items-center gap-1 text-success">
            <CheckCircle2 size={14} />
            {lesson.score !== null ? `${Math.round(lesson.score)}%` : ""}
          </span>
        )}
      </div>
    </Link>
  );
}
