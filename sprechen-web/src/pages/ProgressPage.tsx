import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import { motion } from "framer-motion";
import { Sparkles, Flame, BookOpen, Mic } from "lucide-react";
import { useStats, usePronunciationHistory } from "@/hooks/useProgress";
import {
  useAchievements,
  useFullAnalytics,
  useStudyHeatmap,
  useXPProgression,
} from "@/hooks/useGamification";
import { LevelBadge } from "@/components/ui/LevelBadge";
import { XPBar } from "@/components/ui/XPBar";
import { StudyHeatmap } from "@/components/ui/StudyHeatmap";
import { AchievementGrid } from "@/components/ui/AchievementGrid";
import { XPProgressionChart } from "@/components/ui/XPProgressionChart";
import { XP_PER_LEVEL } from "@/constants/levels";

export function ProgressPage() {
  const stats = useStats();
  const pron = usePronunciationHistory();
  const heatmap = useStudyHeatmap();
  const xp = useXPProgression();
  const achievements = useAchievements();
  const full = useFullAnalytics();

  if (stats.isLoading) {
    return <div className="text-sm text-gray-500">Lädt …</div>;
  }
  if (!stats.data) {
    return (
      <div className="rounded-lg bg-danger-light p-4 text-sm text-danger">
        Fehler beim Laden.
      </div>
    );
  }

  const pronChart = (pron.data ?? [])
    .slice()
    .reverse()
    .map((p, i) => ({
      idx: i + 1,
      score: Math.round(p.overall_score),
    }));

  const weeklyChart = (full.data?.weekly_stats.per_day ?? []).map((d) => ({
    day: new Date(d.date).toLocaleDateString("de-DE", { weekday: "short" }),
    lessons: d.lessons,
  }));

  const nextLevelXP = XP_PER_LEVEL[stats.data.level];
  const weekly = full.data?.weekly_stats;
  const readiness = full.data?.exam_readiness;

  return (
    <div className="space-y-5">
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-2xl bg-white p-6 shadow-sm"
      >
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs uppercase text-gray-500">Aktuelles Niveau</p>
            <div className="mt-1 flex items-center gap-3">
              <h2 className="text-3xl font-bold text-gray-900">
                {stats.data.level}
              </h2>
              <LevelBadge level={stats.data.level} />
            </div>
          </div>
        </div>
        <div className="mt-4">
          <XPBar
            currentXP={stats.data.xp}
            nextLevelXP={nextLevelXP}
            level={stats.data.level}
          />
        </div>
      </motion.div>

      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <Stat
          icon={<Sparkles className="text-primary" />}
          label="XP"
          value={Math.round(stats.data.xp).toLocaleString()}
        />
        <Stat
          icon={<Flame className="text-orange-500" />}
          label="Streak"
          value={`${stats.data.streak} Tage`}
        />
        <Stat
          icon={<BookOpen className="text-success" />}
          label="Lektionen"
          value={String(stats.data.lessons_completed)}
        />
        <Stat
          icon={<Mic className="text-primary-dark" />}
          label="Aussprache Ø"
          value={`${Math.round(stats.data.pronunciation_avg)}%`}
        />
      </div>

      {weekly && (
        <Section title="Diese Woche">
          <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
            <MiniStat label="Lektionen" value={String(weekly.lessons_this_week)} />
            <MiniStat label="Minuten" value={String(weekly.minutes_studied)} />
            <MiniStat label="Vokabeln" value={String(weekly.vocab_learned)} />
            <MiniStat label="XP" value={String(weekly.xp_earned)} />
          </div>
          <div className="mt-4 h-48">
            {weeklyChart.length === 0 ? (
              <p className="py-8 text-center text-sm text-gray-400">
                Noch keine Aktivität diese Woche.
              </p>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={weeklyChart}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis dataKey="day" stroke="#9CA3AF" fontSize={11} />
                  <YAxis allowDecimals={false} stroke="#9CA3AF" fontSize={11} />
                  <Tooltip
                    contentStyle={{
                      borderRadius: 8,
                      border: "1px solid #E5E7EB",
                      fontSize: 12,
                    }}
                  />
                  <Bar dataKey="lessons" fill="#2563EB" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </Section>
      )}

      <Section title="Studienverlauf (365 Tage)">
        {heatmap.isLoading ? (
          <p className="py-4 text-sm text-gray-400">Lädt …</p>
        ) : (
          <StudyHeatmap cells={heatmap.data ?? []} />
        )}
      </Section>

      <Section title="XP-Entwicklung">
        <XPProgressionChart data={xp.data} />
      </Section>

      <Section title="Aussprache-Verlauf">
        {pronChart.length === 0 ? (
          <p className="py-8 text-center text-sm text-gray-400">
            Noch keine Aufnahmen.
          </p>
        ) : (
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={pronChart}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis dataKey="idx" stroke="#9CA3AF" fontSize={12} />
                <YAxis domain={[0, 100]} stroke="#9CA3AF" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    borderRadius: 8,
                    border: "1px solid #E5E7EB",
                    fontSize: 12,
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#2563EB"
                  strokeWidth={2}
                  dot={{ r: 3 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </Section>

      {readiness && (
        <Section title="Prüfungsbereitschaft">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Gesamt</span>
            <span className="text-lg font-bold text-primary">
              {Math.round(readiness.overall)}%
            </span>
          </div>
          <div className="mt-2 h-2 overflow-hidden rounded-full bg-gray-200">
            <div
              className="h-full bg-primary"
              style={{ width: `${Math.round(readiness.overall)}%` }}
            />
          </div>
          <p className="mt-3 text-xs text-gray-600">
            {readiness.recommendation}
          </p>
        </Section>
      )}

      <Section title="Erfolge">
        <AchievementGrid achievements={achievements.data ?? []} />
      </Section>
    </div>
  );
}

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm">
      <h3 className="mb-3 text-base font-bold text-gray-900">{title}</h3>
      {children}
    </div>
  );
}

function Stat({
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
      <div>{icon}</div>
      <p className="mt-2 text-lg font-bold text-gray-900">{value}</p>
      <p className="text-xs text-gray-500">{label}</p>
    </div>
  );
}

function MiniStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg bg-gray-50 p-3 text-center">
      <p className="text-lg font-bold text-gray-900">{value}</p>
      <p className="text-[10px] uppercase text-gray-500">{label}</p>
    </div>
  );
}
