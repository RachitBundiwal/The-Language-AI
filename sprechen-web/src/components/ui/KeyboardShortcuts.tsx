import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";

const SHORTCUTS: Array<{ keys: string; label: string; path?: string }> = [
  { keys: "Alt + H", label: "Startseite", path: "/" },
  { keys: "Alt + L", label: "Lektionen", path: "/lessons" },
  { keys: "Alt + S", label: "Sprechen", path: "/conversation" },
  { keys: "Alt + V", label: "Vokabeln", path: "/vocabulary" },
  { keys: "Alt + P", label: "Prüfung", path: "/exam" },
  { keys: "Alt + F", label: "Fortschritt", path: "/progress" },
  { keys: "?", label: "Diese Übersicht" },
];

const ROUTES: Record<string, string> = {
  h: "/",
  l: "/lessons",
  s: "/conversation",
  v: "/vocabulary",
  p: "/exam",
  f: "/progress",
};

function isTypingTarget(el: EventTarget | null): boolean {
  if (!(el instanceof HTMLElement)) return false;
  const tag = el.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return true;
  if (el.isContentEditable) return true;
  return false;
}

export function KeyboardShortcuts() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (isTypingTarget(e.target)) return;

      if (e.key === "?" || (e.shiftKey && e.key === "/")) {
        e.preventDefault();
        setOpen((v) => !v);
        return;
      }
      if (e.key === "Escape" && open) {
        e.preventDefault();
        setOpen(false);
        return;
      }
      if (!e.altKey) return;
      const key = e.key.toLowerCase();
      const route = ROUTES[key];
      if (route) {
        e.preventDefault();
        navigate(route);
      }
    };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [navigate, open]);

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[90] flex items-center justify-center bg-black/40 p-4"
          onClick={() => setOpen(false)}
        >
          <motion.div
            initial={{ scale: 0.95, y: 10 }}
            animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.95, y: 10 }}
            onClick={(e) => e.stopPropagation()}
            className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl dark:bg-gray-800"
          >
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100">
                Tastenkürzel
              </h2>
              <button
                onClick={() => setOpen(false)}
                className="rounded-lg p-1 text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700"
                aria-label="Schließen"
              >
                <X size={18} />
              </button>
            </div>
            <ul className="space-y-2">
              {SHORTCUTS.map((s) => (
                <li
                  key={s.keys}
                  className="flex items-center justify-between rounded-lg bg-gray-50 px-3 py-2 text-sm dark:bg-gray-700"
                >
                  <span className="text-gray-700 dark:text-gray-200">
                    {s.label}
                  </span>
                  <kbd className="rounded border border-gray-300 bg-white px-2 py-0.5 font-mono text-xs text-gray-700 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200">
                    {s.keys}
                  </kbd>
                </li>
              ))}
            </ul>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
