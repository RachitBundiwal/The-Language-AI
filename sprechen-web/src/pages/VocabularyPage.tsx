import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { RotateCw, Check, X } from "lucide-react";
import { post, queryClient } from "@/hooks/useApi";
import { API } from "@/constants/api";
import { useVocabDue } from "@/hooks/useProgress";
import type { VocabularyCard } from "@/types";

type Quality = 0 | 1 | 2 | 3 | 4 | 5;

export function VocabularyPage() {
  const { data, isLoading, error } = useVocabDue();
  const [idx, setIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);

  const review = useMutation({
    mutationFn: (payload: { card_id: number; quality: Quality }) =>
      post(API.vocabReview, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["vocab-due"] });
      queryClient.invalidateQueries({ queryKey: ["stats"] });
    },
  });

  if (isLoading) return <div className="text-sm text-gray-500">Lädt …</div>;
  if (error) {
    return (
      <div className="rounded-lg bg-danger-light p-4 text-sm text-danger">
        Fehler beim Laden.
      </div>
    );
  }

  const cards: VocabularyCard[] = data ?? [];
  if (cards.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center rounded-2xl bg-white p-12 text-center shadow-sm">
        <Check size={48} className="text-success" />
        <h2 className="mt-4 text-xl font-bold text-gray-900">
          Alle Karten erledigt!
        </h2>
        <p className="mt-1 text-sm text-gray-500">
          Komm später wieder, um weitere Vokabeln zu wiederholen.
        </p>
      </div>
    );
  }

  if (idx >= cards.length) {
    return (
      <div className="flex flex-col items-center justify-center rounded-2xl bg-white p-12 text-center shadow-sm">
        <Check size={48} className="text-success" />
        <h2 className="mt-4 text-xl font-bold text-gray-900">Geschafft!</h2>
        <p className="mt-1 text-sm text-gray-500">
          {cards.length} Karten überprüft.
        </p>
        <button
          onClick={() => {
            setIdx(0);
            setFlipped(false);
          }}
          className="mt-4 rounded-lg bg-primary px-5 py-2 text-sm font-bold text-white hover:bg-primary-dark"
        >
          Nochmal
        </button>
      </div>
    );
  }

  const card = cards[idx];

  const grade = (quality: Quality) => {
    review.mutate({ card_id: card.id, quality });
    setFlipped(false);
    setIdx(idx + 1);
  };

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between text-sm text-gray-600">
        <span>
          Karte {idx + 1} / {cards.length}
        </span>
        <span>{Math.round(((idx + 1) / cards.length) * 100)}%</span>
      </div>
      <div className="h-1.5 overflow-hidden rounded-full bg-gray-200">
        <div
          className="h-full bg-primary transition-all"
          style={{ width: `${((idx + 1) / cards.length) * 100}%` }}
        />
      </div>

      <div className="relative h-64">
        <AnimatePresence mode="wait">
          <motion.button
            key={`${card.id}-${flipped}`}
            initial={{ rotateY: 90, opacity: 0 }}
            animate={{ rotateY: 0, opacity: 1 }}
            exit={{ rotateY: -90, opacity: 0 }}
            transition={{ duration: 0.25 }}
            onClick={() => setFlipped(!flipped)}
            className="absolute inset-0 flex flex-col items-center justify-center rounded-2xl bg-white p-8 shadow-md"
          >
            {!flipped ? (
              <>
                <p className="text-4xl font-bold text-gray-900">
                  {card.german_word}
                </p>
                {card.phonetic && (
                  <p className="mt-2 text-sm italic text-gray-500">
                    [{card.phonetic}]
                  </p>
                )}
                <p className="mt-6 flex items-center gap-1 text-xs text-gray-400">
                  <RotateCw size={12} />
                  Tipp zum Umdrehen
                </p>
              </>
            ) : (
              <>
                <p className="text-3xl font-bold text-primary">
                  {card.english_translation}
                </p>
                {card.example_sentence && (
                  <p className="mt-4 text-center text-sm italic text-gray-600">
                    {card.example_sentence}
                  </p>
                )}
              </>
            )}
          </motion.button>
        </AnimatePresence>
      </div>

      {flipped && (
        <div className="grid grid-cols-3 gap-2">
          <button
            onClick={() => grade(1)}
            className="flex flex-col items-center gap-1 rounded-lg border-2 border-danger bg-danger-light px-3 py-3 text-xs font-bold text-danger hover:bg-red-100"
          >
            <X size={18} />
            Falsch
          </button>
          <button
            onClick={() => grade(3)}
            className="flex flex-col items-center gap-1 rounded-lg border-2 border-orange-400 bg-orange-50 px-3 py-3 text-xs font-bold text-orange-600 hover:bg-orange-100"
          >
            <RotateCw size={18} />
            Schwer
          </button>
          <button
            onClick={() => grade(5)}
            className="flex flex-col items-center gap-1 rounded-lg border-2 border-success bg-success-light px-3 py-3 text-xs font-bold text-success hover:bg-green-100"
          >
            <Check size={18} />
            Leicht
          </button>
        </div>
      )}
    </div>
  );
}
