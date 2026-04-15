import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { WifiOff } from "lucide-react";

export function OfflineNotice() {
  const [online, setOnline] = useState(
    typeof navigator !== "undefined" ? navigator.onLine : true,
  );

  useEffect(() => {
    const goOnline = () => setOnline(true);
    const goOffline = () => setOnline(false);
    window.addEventListener("online", goOnline);
    window.addEventListener("offline", goOffline);
    return () => {
      window.removeEventListener("online", goOnline);
      window.removeEventListener("offline", goOffline);
    };
  }, []);

  return (
    <AnimatePresence>
      {!online && (
        <motion.div
          initial={{ y: -60, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: -60, opacity: 0 }}
          transition={{ type: "spring", stiffness: 180, damping: 22 }}
          className="sticky top-0 z-40 flex items-center justify-center gap-2 bg-warning px-4 py-2 text-xs font-medium text-white shadow"
        >
          <WifiOff size={14} />
          Keine Internetverbindung — KI-Funktionen nicht verfügbar. Vokabeln und
          Lektionen funktionieren offline.
        </motion.div>
      )}
    </AnimatePresence>
  );
}
