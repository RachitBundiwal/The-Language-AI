import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Check, X, Mic } from "lucide-react";
import type { Exercise } from "@/types";

interface AnswerResult {
  correct: boolean;
  score: number;
}

interface Props {
  exercise: Exercise;
  lessonId?: number;
  onAnswer: (result: AnswerResult) => void;
}

export function ExerciseRenderer({ exercise, lessonId, onAnswer }: Props) {
  switch (exercise.type) {
    case "fill_in_blank":
      return <FillInBlank ex={exercise} onAnswer={onAnswer} />;
    case "multiple_choice":
      return <MultipleChoice ex={exercise} onAnswer={onAnswer} />;
    case "arrange_words":
      return <ArrangeWords ex={exercise} onAnswer={onAnswer} />;
    case "translate":
      return <Translate ex={exercise} onAnswer={onAnswer} />;
    case "speaking_prompt":
      return <SpeakingPrompt ex={exercise} lessonId={lessonId} onAnswer={onAnswer} />;
    case "listening":
      return <Listening ex={exercise} onAnswer={onAnswer} />;
    default:
      return null;
  }
}

// ---------- fill in blank ----------
function FillInBlank({
  ex,
  onAnswer,
}: {
  ex: Extract<Exercise, { type: "fill_in_blank" }>;
  onAnswer: (r: AnswerResult) => void;
}) {
  const [picked, setPicked] = useState<number | null>(null);
  const handle = (idx: number) => {
    if (picked !== null) return;
    setPicked(idx);
    const correct = idx === ex.correct_index;
    onAnswer({ correct, score: correct ? 100 : 0 });
  };
  return (
    <div>
      <div className="mb-6 rounded-lg bg-yellow-50 p-6 text-center text-xl text-gray-900">
        {ex.sentence_with_blank.split("___").map((part, i, arr) => (
          <span key={i}>
            {part}
            {i < arr.length - 1 && (
              <span className="mx-1 inline-block min-w-[60px] rounded border-b-2 border-yellow-500 bg-yellow-200 px-2 font-bold">
                {picked !== null ? ex.options[picked] : "____"}
              </span>
            )}
          </span>
        ))}
      </div>
      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        {ex.options.map((opt, idx) => {
          const isPicked = picked === idx;
          const isCorrect = idx === ex.correct_index;
          let cls = "border-gray-200 bg-white hover:border-primary";
          if (picked !== null) {
            if (isPicked && isCorrect) cls = "border-success bg-success-light";
            else if (isPicked && !isCorrect) cls = "border-danger bg-danger-light";
            else if (isCorrect) cls = "border-success bg-success-light";
            else cls = "border-gray-200 bg-gray-50 opacity-60";
          }
          return (
            <button
              key={idx}
              onClick={() => handle(idx)}
              disabled={picked !== null}
              className={`rounded-lg border-2 px-4 py-3 text-sm font-medium transition-colors ${cls}`}
            >
              {opt}
            </button>
          );
        })}
      </div>
      {picked !== null && ex.hint && (
        <p className="mt-4 text-sm italic text-gray-600">{ex.hint}</p>
      )}
    </div>
  );
}

// ---------- multiple choice ----------
function MultipleChoice({
  ex,
  onAnswer,
}: {
  ex: Extract<Exercise, { type: "multiple_choice" }>;
  onAnswer: (r: AnswerResult) => void;
}) {
  const [picked, setPicked] = useState<number | null>(null);
  const handle = (idx: number) => {
    if (picked !== null) return;
    setPicked(idx);
    const correct = idx === ex.correct_index;
    onAnswer({ correct, score: correct ? 100 : 0 });
  };
  return (
    <div>
      <h3 className="mb-4 text-lg font-semibold text-gray-900">{ex.question}</h3>
      <div className="space-y-2">
        {ex.options.map((opt, idx) => {
          const isPicked = picked === idx;
          const isCorrect = idx === ex.correct_index;
          let cls = "border-gray-200 bg-white hover:border-primary";
          if (picked !== null) {
            if (isCorrect) cls = "border-success bg-success-light";
            else if (isPicked) cls = "border-danger bg-danger-light";
            else cls = "border-gray-200 bg-gray-50 opacity-60";
          }
          return (
            <button
              key={idx}
              onClick={() => handle(idx)}
              disabled={picked !== null}
              className={`flex w-full items-center justify-between rounded-lg border-2 px-4 py-3 text-left text-sm transition-colors ${cls}`}
            >
              <span>{opt}</span>
              {picked !== null && isCorrect && <Check size={16} className="text-success" />}
              {picked !== null && isPicked && !isCorrect && <X size={16} className="text-danger" />}
            </button>
          );
        })}
      </div>
      {picked !== null && ex.explanation && (
        <p className="mt-4 rounded-lg bg-blue-50 p-3 text-sm text-gray-700">
          {ex.explanation}
        </p>
      )}
    </div>
  );
}

// ---------- arrange words ----------
function ArrangeWords({
  ex,
  onAnswer,
}: {
  ex: Extract<Exercise, { type: "arrange_words" }>;
  onAnswer: (r: AnswerResult) => void;
}) {
  const [order, setOrder] = useState<string[]>(ex.scrambled_words);
  const [checked, setChecked] = useState<boolean | null>(null);

  const move = (from: number, to: number) => {
    if (checked !== null) return;
    const next = [...order];
    const [item] = next.splice(from, 1);
    next.splice(to, 0, item);
    setOrder(next);
  };

  const handleCheck = () => {
    const normalized = order.join(" ").trim().toLowerCase();
    const target = ex.correct_sentence.trim().toLowerCase().replace(/\s+/g, " ");
    const correct = normalized === target;
    setChecked(correct);
    onAnswer({ correct, score: correct ? 100 : 0 });
  };

  return (
    <div>
      <p className="mb-4 text-sm text-gray-600">Ordne die Wörter zu einem Satz:</p>
      <div className="mb-4 flex flex-wrap gap-2">
        {order.map((word, idx) => (
          <button
            key={`${word}-${idx}`}
            onClick={() => move(idx, Math.max(0, idx - 1))}
            className="cursor-grab rounded-lg border-2 border-primary bg-primary-light px-3 py-2 text-sm font-medium text-primary-dark"
            title="Klick um nach links zu verschieben"
          >
            {word}
          </button>
        ))}
      </div>
      {checked === null ? (
        <button
          onClick={handleCheck}
          className="rounded-lg bg-primary px-5 py-2 text-sm font-bold text-white hover:bg-primary-dark"
        >
          Überprüfen
        </button>
      ) : (
        <div
          className={`rounded-lg p-4 ${
            checked ? "bg-success-light text-success" : "bg-danger-light text-danger"
          }`}
        >
          {checked ? (
            <p>Richtig!</p>
          ) : (
            <div>
              <p className="font-bold">Nicht ganz.</p>
              <p className="mt-1 text-sm">Korrekt: {ex.correct_sentence}</p>
            </div>
          )}
          {ex.hint && <p className="mt-2 text-xs text-gray-600">{ex.hint}</p>}
        </div>
      )}
    </div>
  );
}

// ---------- translate ----------
function Translate({
  ex,
  onAnswer,
}: {
  ex: Extract<Exercise, { type: "translate" }>;
  onAnswer: (r: AnswerResult) => void;
}) {
  const [text, setText] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const handle = () => {
    if (!text.trim()) return;
    const ok =
      text.trim().toLowerCase().replace(/[.,!?]/g, "") ===
      ex.model_answer.trim().toLowerCase().replace(/[.,!?]/g, "");
    setSubmitted(true);
    onAnswer({ correct: ok, score: ok ? 100 : 50 });
  };
  return (
    <div>
      <p className="mb-2 text-sm text-gray-600">Übersetze ins Deutsche:</p>
      <p className="mb-4 rounded-lg bg-gray-100 p-4 text-lg italic text-gray-800">
        {ex.source_text}
      </p>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={submitted}
        rows={3}
        className="w-full rounded-lg border-2 border-gray-200 p-3 text-sm focus:border-primary focus:outline-none"
        placeholder="Deine Übersetzung..."
      />
      {!submitted ? (
        <button
          onClick={handle}
          className="mt-3 rounded-lg bg-primary px-5 py-2 text-sm font-bold text-white hover:bg-primary-dark"
        >
          Überprüfen
        </button>
      ) : (
        <div className="mt-3 rounded-lg bg-blue-50 p-4">
          <p className="text-sm font-bold text-gray-900">Musterlösung:</p>
          <p className="mt-1 text-sm text-gray-700">{ex.model_answer}</p>
        </div>
      )}
    </div>
  );
}

// ---------- speaking prompt ----------
function SpeakingPrompt({
  ex,
  lessonId,
  onAnswer,
}: {
  ex: Extract<Exercise, { type: "speaking_prompt" }>;
  lessonId?: number;
  onAnswer: (r: AnswerResult) => void;
}) {
  const navigate = useNavigate();
  return (
    <div className="rounded-lg border-2 border-primary bg-primary-light p-6">
      <p className="mb-2 text-sm font-bold uppercase text-primary-dark">
        Sprechübung
      </p>
      <p className="text-lg text-gray-900">{ex.prompt_text}</p>
      <p className="mt-2 text-xs text-gray-600">
        Min. {ex.min_words} Wörter
      </p>
      <button
        onClick={() => {
          onAnswer({ correct: true, score: 100 });
          const params = new URLSearchParams({ text: ex.prompt_text });
          if (lessonId) params.set("lesson", String(lessonId));
          navigate(`/voice?${params.toString()}`);
        }}
        className="mt-4 inline-flex items-center gap-2 rounded-lg bg-primary px-5 py-2 text-sm font-bold text-white hover:bg-primary-dark"
      >
        <Mic size={16} />
        Zur Sprachübung
      </button>
    </div>
  );
}

// ---------- listening ----------
function Listening({
  ex,
  onAnswer,
}: {
  ex: Extract<Exercise, { type: "listening" }>;
  onAnswer: (r: AnswerResult) => void;
}) {
  const [played, setPlayed] = useState(false);
  const [picks, setPicks] = useState<Record<number, number>>({});

  const total = ex.questions.length;
  const allAnswered = Object.keys(picks).length === total;

  const handleCheck = () => {
    let correctCount = 0;
    ex.questions.forEach((q, idx) => {
      if (picks[idx] === q.correct_index) correctCount++;
    });
    onAnswer({
      correct: correctCount === total,
      score: total > 0 ? Math.round((correctCount / total) * 100) : 0,
    });
  };

  return (
    <div>
      <div className="mb-4 rounded-lg bg-gray-100 p-4">
        <p className="text-xs uppercase text-gray-500">Hörtext</p>
        <p className="mt-1 text-sm text-gray-700">{ex.audio_script}</p>
        <button
          onClick={() => setPlayed(true)}
          className="mt-3 rounded-lg bg-primary px-4 py-2 text-xs font-bold text-white hover:bg-primary-dark"
        >
          ▶ Abspielen (simuliert)
        </button>
      </div>
      {played && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="space-y-4"
        >
          {ex.questions.map((q, qIdx) => (
            <div key={qIdx}>
              <p className="mb-2 font-medium text-gray-900">{q.question}</p>
              <div className="grid grid-cols-2 gap-2">
                {q.options.map((opt, oIdx) => {
                  const picked = picks[qIdx] === oIdx;
                  return (
                    <button
                      key={oIdx}
                      onClick={() => setPicks({ ...picks, [qIdx]: oIdx })}
                      className={`rounded-lg border-2 px-3 py-2 text-sm ${
                        picked
                          ? "border-primary bg-primary-light"
                          : "border-gray-200 bg-white hover:border-primary"
                      }`}
                    >
                      {opt}
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
          {allAnswered && (
            <button
              onClick={handleCheck}
              className="rounded-lg bg-primary px-5 py-2 text-sm font-bold text-white hover:bg-primary-dark"
            >
              Antworten überprüfen
            </button>
          )}
        </motion.div>
      )}
    </div>
  );
}
