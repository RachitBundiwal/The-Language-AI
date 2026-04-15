import { motion } from "framer-motion";

interface Props {
  isRecording: boolean;
  audioLevel: number;
}

const BARS = 5;

export function WaveformDisplay({ isRecording, audioLevel }: Props) {
  return (
    <div className="flex h-12 items-center justify-center gap-1.5">
      {Array.from({ length: BARS }).map((_, i) => {
        const variation = isRecording ? 0.3 + Math.random() * 0.7 : 0;
        const height = isRecording
          ? Math.max(8, audioLevel * 40 * variation + 8)
          : 4;
        return (
          <motion.div
            key={i}
            className="w-1.5 rounded-full bg-primary"
            animate={{ height }}
            transition={{ duration: 0.1, ease: "easeOut" }}
            style={{ minHeight: 4 }}
          />
        );
      })}
    </div>
  );
}
