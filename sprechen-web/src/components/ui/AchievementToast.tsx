import { useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { useToastStore } from "@/store/toastStore";

const AUTO_DISMISS_MS = 3000;

export function AchievementToast() {
  const current = useToastStore((s) => s.current);
  const dismiss = useToastStore((s) => s.dismiss);

  useEffect(() => {
    if (!current) return;
    const t = setTimeout(dismiss, AUTO_DISMISS_MS);
    return () => clearTimeout(t);
  }, [current, dismiss]);

  return (
    <div className="pointer-events-none fixed inset-x-0 top-0 z-[100] flex justify-center">
      <AnimatePresence>
        {current && (
          <motion.div
            key={current.id}
            initial={{ y: -120, opacity: 0 }}
            animate={{ y: 16, opacity: 1 }}
            exit={{ y: -120, opacity: 0 }}
            transition={{ type: "spring", stiffness: 220, damping: 22 }}
            className="pointer-events-auto flex items-center gap-4 rounded-2xl border border-yellow-300 bg-gradient-to-br from-yellow-50 to-white px-5 py-4 shadow-xl"
          >
            <div className="text-4xl">{current.achievement.emoji}</div>
            <div>
              <p className="text-[10px] font-bold uppercase tracking-wide text-yellow-600">
                Erfolg freigeschaltet
              </p>
              <p className="text-base font-bold text-gray-900">
                {current.achievement.title}
              </p>
              <p className="text-xs text-gray-600">
                {current.achievement.description}
              </p>
            </div>
            <button
              onClick={dismiss}
              className="ml-2 text-xs text-gray-400 hover:text-gray-600"
              aria-label="Schließen"
            >
              ✕
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
