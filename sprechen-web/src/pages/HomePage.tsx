import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  BookOpen,
  Mic,
  Layers,
  Award,
  ArrowRight,
  Flame,
  Sparkles,
  Clock,
} from "lucide-react";
import { useStats } from "@/hooks/useProgress";
import { LevelBadge } from "@/components/ui/LevelBadge";
import { XPBar } from "@/components/ui/XPBar";
import { XP_PER_LEVEL } from "@/constants/levels";

export function HomePage() {
  const { data, isLoading, error } = useStats();

  if (isLoading) {
    return <div className="text-sm text-gray-500">Lädt …</div>;
  }
  if (error || !data) {
    return (
      <div className="rounded-lg bg-danger-light p-4 text-sm text-danger">
        Fehler beim Laden der Statistiken.
      </div>
    );
  }

  const nextLevelXP = XP_PER_LEVEL[data.level];

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-2xl bg-gradient-to-br from-primary to-primary-dark p-6 text-white"
      >
        <p className="text-sm opacity-90">Willkommen zurück!</p>
        <div className="mt-1 flex items-center gap-3">
          <h2 className="text-3xl font-bold">Bereit zum Lernen?</h2>
          <LevelBadge level={data.level} />
        </div>
        <div className="mt-4">
          <XPBar
            currentXP={data.xp}
            nextLevelXP={nextLevelXP}
            level={data.level}
          />
        </div>
      </motion.div>

      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <StatCard
          icon={<Flame className="text-orange-500" size={20} />}
          label="Streak"
          value={`${data.streak} Tage`}
        />
        <StatCard
          icon={<Sparkles className="text-primary" size={20} />}
          label="XP"
          value={Math.round(data.xp).toLocaleString()}
        />
        <StatCard
          icon={<BookOpen className="text-success" size={20} />}
          label="Lektionen"
          value={String(data.lessons_completed)}
        />
        <StatCard
          icon={<Clock className="text-gray-700" size={20} />}
          label="Minuten"
          value={String(Math.round(data.total_minutes))}
        />
      </div>

      {data.next_lesson && (
        <Link
          to={`/lessons/${data.next_lesson.id}`}
          className="block rounded-2xl border-2 border-primary bg-primary-light p-5 transition-shadow hover:shadow-md"
        >
          <p className="text-xs font-bold uppercase text-primary-dark">
            Nächste Lektion
          </p>
          <div className="mt-1 flex items-center justify-between">
            <div>
              <h3 className="text-lg font-bold text-gray-900">
                {data.next_lesson.title}
              </h3>
              <p className="mt-1 text-xs text-gray-600">
                {data.next_lesson.estimated_minutes} Min ·{" "}
                {data.next_lesson.level}
              </p>
            </div>
            <ArrowRight className="text-primary" />
          </div>
        </Link>
      )}

      <div>
        <h3 className="mb-3 text-base font-bold text-gray-900">
          Schnellzugriff
        </h3>
        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          <QuickLink
            to="/lessons"
            icon={<BookOpen size={22} />}
            label="Lektionen"
          />
          <QuickLink
            to="/conversation"
            icon={<Mic size={22} />}
            label="Sprechen"
          />
          <QuickLink
            to="/vocabulary"
            icon={<Layers size={22} />}
            label={`Vokabeln (${data.vocab_due_count})`}
          />
          <QuickLink to="/exam" icon={<Award size={22} />} label="Prüfung" />
        </div>
      </div>
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-3">
      <div className="flex items-center gap-2">{icon}</div>
      <p className="mt-2 text-lg font-bold text-gray-900">{value}</p>
      <p className="text-xs text-gray-500">{label}</p>
    </div>
  );
}

function QuickLink({
  to,
  icon,
  label,
}: {
  to: string;
  icon: React.ReactNode;
  label: string;
}) {
  return (
    <Link
      to={to}
      className="flex flex-col items-center gap-2 rounded-xl border-2 border-gray-200 bg-white p-4 text-center transition-colors hover:border-primary hover:bg-primary-light"
    >
      <div className="text-primary">{icon}</div>
      <span className="text-xs font-medium text-gray-700">{label}</span>
    </Link>
  );
}
