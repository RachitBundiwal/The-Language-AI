import { AnimatePresence, motion } from "framer-motion";
import { CheckCircle2, AlertCircle, Info, X } from "lucide-react";

export type ToastKind = "success" | "error" | "info";

interface Props {
  open: boolean;
  kind?: ToastKind;
  message: string;
  onClose: () => void;
}

const ICON: Record<ToastKind, typeof CheckCircle2> = {
  success: CheckCircle2,
  error: AlertCircle,
  info: Info,
};

const COLOR: Record<ToastKind, string> = {
  success: "bg-success text-white",
  error: "bg-danger text-white",
  info: "bg-primary text-white",
};

export function Toast({ open, kind = "info", message, onClose }: Props) {
  const Icon = ICON[kind];
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 30 }}
          className={`fixed bottom-6 left-1/2 z-50 flex -translate-x-1/2 items-center gap-3 rounded-lg px-4 py-3 shadow-lg ${COLOR[kind]}`}
        >
          <Icon size={20} />
          <span className="text-sm font-medium">{message}</span>
          <button onClick={onClose} className="ml-2 hover:opacity-80">
            <X size={16} />
          </button>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
