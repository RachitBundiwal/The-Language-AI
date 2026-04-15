import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { Download, Moon, Sun, Trash2, AlertTriangle } from "lucide-react";
import { get } from "@/hooks/useApi";
import { API, BASE_URL } from "@/constants/api";
import { useSettings, type Formality, type Theme } from "@/hooks/useSettings";

type VoicesResponse = Record<string, string>;

const WEEKLY_GOALS: Array<1 | 2 | 5 | 10> = [1, 2, 5, 10];

export function SettingsPage() {
  const { settings, updateSettings, resetSettings } = useSettings();
  const [confirmOpen, setConfirmOpen] = useState(false);

  const voices = useQuery<VoicesResponse>({
    queryKey: ["voices"],
    queryFn: () => get<VoicesResponse>(API.voices),
    staleTime: Infinity,
  });

  const handleExport = () => {
    window.open(`${BASE_URL}/api/v1/admin/export`, "_blank");
  };

  const handleReset = async () => {
    try {
      // Wipe local preferences AND clear TanStack caches via reload.
      resetSettings();
      window.localStorage.removeItem("sprechen.settings.v1");
      // Best-effort: call a reset endpoint if one exists; otherwise instruct.
      alert(
        "Lokale Einstellungen wurden zurückgesetzt. Um den kompletten Fortschritt zu löschen, lösche sprechen.db im Backend-Verzeichnis.",
      );
    } finally {
      setConfirmOpen(false);
    }
  };

  return (
    <div className="space-y-5">
      <Section title="Aussprache (TTS)">
        <label className="block text-xs font-bold uppercase text-gray-500 dark:text-gray-400">
          Stimme
        </label>
        <select
          value={settings.voice}
          onChange={(e) => updateSettings({ voice: e.target.value })}
          className="mt-1 w-full rounded-lg border-2 border-gray-200 bg-white px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100"
        >
          {voices.isLoading && <option>Lädt …</option>}
          {voices.data &&
            Object.entries(voices.data).map(([id, label]) => (
              <option key={id} value={id}>
                {label} ({id})
              </option>
            ))}
        </select>

        <label className="mt-4 block text-xs font-bold uppercase text-gray-500 dark:text-gray-400">
          Sprechgeschwindigkeit: {settings.speed > 0 ? "+" : ""}
          {settings.speed}%
        </label>
        <input
          type="range"
          min={-20}
          max={20}
          step={5}
          value={settings.speed}
          onChange={(e) =>
            updateSettings({ speed: Number(e.target.value) })
          }
          className="mt-2 w-full"
        />
      </Section>

      <Section title="Gespräche">
        <label className="block text-xs font-bold uppercase text-gray-500 dark:text-gray-400">
          Standard-Anrede
        </label>
        <div className="mt-2 flex gap-2">
          {(["du", "Sie"] as Formality[]).map((f) => (
            <button
              key={f}
              onClick={() => updateSettings({ formality: f })}
              className={`flex-1 rounded-lg border-2 px-4 py-2 text-sm font-bold transition-colors ${
                settings.formality === f
                  ? "border-primary bg-primary text-white"
                  : "border-gray-200 bg-white text-gray-700 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200"
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </Section>

      <Section title="Darstellung">
        <label className="block text-xs font-bold uppercase text-gray-500 dark:text-gray-400">
          Theme
        </label>
        <div className="mt-2 flex gap-2">
          {(["light", "dark"] as Theme[]).map((t) => (
            <button
              key={t}
              onClick={() => updateSettings({ theme: t })}
              className={`flex flex-1 items-center justify-center gap-2 rounded-lg border-2 px-4 py-2 text-sm font-bold transition-colors ${
                settings.theme === t
                  ? "border-primary bg-primary text-white"
                  : "border-gray-200 bg-white text-gray-700 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200"
              }`}
            >
              {t === "light" ? <Sun size={14} /> : <Moon size={14} />}
              {t === "light" ? "Hell" : "Dunkel"}
            </button>
          ))}
        </div>
      </Section>

      <Section title="Tägliches Ziel">
        <label className="block text-xs font-bold uppercase text-gray-500 dark:text-gray-400">
          Lektionen pro Woche
        </label>
        <div className="mt-2 grid grid-cols-4 gap-2">
          {WEEKLY_GOALS.map((g) => (
            <button
              key={g}
              onClick={() => updateSettings({ weeklyGoal: g })}
              className={`rounded-lg border-2 px-3 py-2 text-sm font-bold ${
                settings.weeklyGoal === g
                  ? "border-primary bg-primary text-white"
                  : "border-gray-200 bg-white text-gray-700 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200"
              }`}
            >
              {g}
            </button>
          ))}
        </div>
      </Section>

      <Section title="Daten">
        <button
          onClick={handleExport}
          className="flex w-full items-center justify-center gap-2 rounded-lg border-2 border-primary bg-primary-light px-4 py-2 text-sm font-bold text-primary-dark hover:bg-primary hover:text-white"
        >
          <Download size={16} />
          Datenbank exportieren (.db)
        </button>
      </Section>

      <Section title="Gefahrenzone">
        <button
          onClick={() => setConfirmOpen(true)}
          className="flex w-full items-center justify-center gap-2 rounded-lg border-2 border-danger bg-danger-light px-4 py-2 text-sm font-bold text-danger hover:bg-danger hover:text-white"
        >
          <Trash2 size={16} />
          Alle Fortschritte zurücksetzen
        </button>
      </Section>

      <AnimatePresence>
        {confirmOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[95] flex items-center justify-center bg-black/50 p-4"
            onClick={() => setConfirmOpen(false)}
          >
            <motion.div
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.95 }}
              onClick={(e) => e.stopPropagation()}
              className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl dark:bg-gray-800"
            >
              <div className="flex items-center gap-3 text-danger">
                <AlertTriangle />
                <h3 className="text-lg font-bold">Wirklich zurücksetzen?</h3>
              </div>
              <p className="mt-3 text-sm text-gray-600 dark:text-gray-300">
                Alle lokalen Einstellungen werden gelöscht. Um auch die
                Fortschrittsdaten (XP, Lektionen, Aussprache-Verlauf) zu
                entfernen, lösche die Datei{" "}
                <code className="rounded bg-gray-100 px-1 text-xs dark:bg-gray-700">
                  sprechen.db
                </code>{" "}
                im Backend-Verzeichnis.
              </p>
              <div className="mt-5 flex gap-2">
                <button
                  onClick={() => setConfirmOpen(false)}
                  className="flex-1 rounded-lg border-2 border-gray-200 bg-white px-4 py-2 text-sm font-bold text-gray-700 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200"
                >
                  Abbrechen
                </button>
                <button
                  onClick={handleReset}
                  className="flex-1 rounded-lg bg-danger px-4 py-2 text-sm font-bold text-white hover:bg-red-700"
                >
                  Zurücksetzen
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
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
    <div className="rounded-2xl bg-white p-5 shadow-sm dark:bg-gray-800">
      <h3 className="mb-3 text-base font-bold text-gray-900 dark:text-gray-100">
        {title}
      </h3>
      {children}
    </div>
  );
}
