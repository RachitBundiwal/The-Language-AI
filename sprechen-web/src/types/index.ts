export type CEFRLevel = "A1" | "A2" | "B1" | "B2" | "C1" | "C2";

export interface User {
  id: number;
  name: string;
  level: CEFRLevel;
  xp: number;
  streak: number;
}

// ---------- Lessons ----------
export interface Vocabulary {
  word: string;
  translation: string;
  phonetic?: string | null;
  example_sentence: string;
}

export interface PhonemeHint {
  phoneme: string;
  tip: string;
}

export interface DialogueTurn {
  role: "native" | "learner";
  german: string;
  english: string;
  vocabulary?: Vocabulary[];
  pronunciation_tips?: PhonemeHint[];
}

export interface GrammarExample {
  german: string;
  english: string;
  breakdown?: string | null;
}

export interface GrammarFocus {
  rule_name: string;
  explanation: string;
  formula: string;
  examples: GrammarExample[];
  common_mistakes: string[];
}

export interface FillInBlankExercise {
  type: "fill_in_blank";
  sentence_with_blank: string;
  options: string[];
  correct_index: number;
  hint: string;
}

export interface MultipleChoiceExercise {
  type: "multiple_choice";
  question: string;
  options: string[];
  correct_index: number;
  explanation: string;
}

export interface ArrangeWordsExercise {
  type: "arrange_words";
  scrambled_words: string[];
  correct_sentence: string;
  hint: string;
}

export interface TranslateExercise {
  type: "translate";
  source_text: string;
  source_lang: string;
  target_lang: string;
  model_answer: string;
}

export interface SpeakingPromptExercise {
  type: "speaking_prompt";
  prompt_text: string;
  expected_topic: string;
  min_words: number;
}

export interface ListeningExerciseQuestion {
  question: string;
  options: string[];
  correct_index: number;
}

export interface ListeningExercise {
  type: "listening";
  audio_script: string;
  questions: ListeningExerciseQuestion[];
}

export type Exercise =
  | FillInBlankExercise
  | MultipleChoiceExercise
  | ArrangeWordsExercise
  | TranslateExercise
  | SpeakingPromptExercise
  | ListeningExercise;

export interface LessonSummary {
  id: number;
  title: string;
  level: CEFRLevel;
  scenario: string;
  topic: string;
  estimated_minutes: number;
  completed: boolean;
  score: number | null;
  attempts?: number;
}

export interface LessonDetail {
  id: number;
  title: string;
  level: CEFRLevel;
  scenario: string;
  topic: string;
  learning_objectives: string[];
  estimated_minutes: number;
  cultural_note: string;
  dialogue: DialogueTurn[];
  grammar_focus: GrammarFocus;
  exercises: Exercise[];
  vocabulary_list: Vocabulary[];
}

export interface VocabularyCard {
  id: number;
  german_word: string;
  english_translation: string;
  example_sentence: string | null;
  phonetic: string | null;
  next_review_at: string;
  interval_days: number;
  ease_factor: number;
  repetitions: number;
}

// ---------- Voice / Pronunciation ----------
export interface PhonemeScore {
  phoneme: string;
  score: number;
  feedback?: string | null;
}

export interface PronunciationResponse {
  overall_score: number;
  pronunciation_score: number;
  fluency_score: number;
  accuracy_score: number;
  completeness_score: number;
  prosody_score?: number | null;
  phoneme_scores: PhonemeScore[];
  problem_phonemes: string[];
  ai_feedback: string;
}

export interface TranscriptionResponse {
  transcript: string;
  language: string;
  confidence: number;
  word_timestamps: Array<{
    word: string;
    start: number;
    end: number;
    probability: number;
  }>;
  duration_seconds: number;
}

export interface VoiceExerciseResult {
  transcription: TranscriptionResponse;
  pronunciation: PronunciationResponse;
  conversation?: ConversationResponse | null;
}

// ---------- Conversation ----------
export interface ConversationMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ConversationCorrection {
  original: string;
  corrected: string;
  explanation: string;
}

export interface ConversationVocab {
  word: string;
  translation: string;
  example: string;
}

export interface ConversationResponse {
  reply: string;
  translation?: string | null;
  corrections: ConversationCorrection[];
  new_vocabulary: ConversationVocab[];
  audio_url?: string | null;
}

// ---------- Exam ----------
export interface ReadingText {
  title: string;
  text: string;
  source_note?: string | null;
}

export interface ReadingQuestion {
  question: string;
  options: string[];
  correct_index: number;
  question_type: string;
}

export interface ReadingPart {
  part_number: number;
  instruction: string;
  texts: ReadingText[];
  questions: ReadingQuestion[];
  max_points: number;
}

export interface ListeningScript {
  title: string;
  script: string;
  speaker_context: string;
}

export interface ListeningPart {
  part_number: number;
  instruction: string;
  scripts: ListeningScript[];
  questions: ReadingQuestion[];
  max_points: number;
}

export interface WritingTask {
  task_number: number;
  instruction: string;
  prompt: string;
  min_words: number;
  max_words: number;
  format_hint: string;
  model_answer: string;
  max_points: number;
}

export interface SpeakingCard {
  card_number: number;
  task_type: string;
  prompt: string;
  supporting_questions: string[];
  time_allowed_seconds: number;
}

export interface ExamPaper {
  level: string;
  section: string;
  time_limit_minutes: number;
  max_score: number;
  instructions: string;
  parts: Array<Record<string, unknown>>;
}

export interface ExamResult {
  level: string;
  section: string;
  score: number;
  max_score: number;
  percentage: number;
  passed: boolean;
  grade: string;
  detailed_results: Array<Record<string, unknown>>;
  feedback: string;
  strengths: string[];
  improvements: string[];
}

export interface ExamReadiness {
  overall: number;
  by_section: Record<string, number>;
  recommendation: string;
  predicted_weeks: number;
}

export interface ExamHistoryEntry {
  id: number;
  level: string;
  section: string;
  score: number;
  max_score: number;
  percentage: number;
  duration_seconds: number;
  passed: boolean;
  created_at: string | null;
}

// ---------- Stats / Progress ----------
export interface DashboardStats {
  xp: number;
  streak: number;
  level: CEFRLevel;
  total_minutes: number;
  lessons_completed: number;
  vocab_due_count: number;
  pronunciation_avg: number;
  next_lesson?: LessonSummary | null;
}

export interface PronunciationHistoryEntry {
  id: number;
  reference_text: string;
  overall_score: number;
  pronunciation_score: number;
  fluency_score: number;
  accuracy_score: number;
  problem_phonemes: string[];
  created_at: string;
}

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  unlocked: boolean;
  unlocked_at?: string | null;
}

export interface GrammarAnalysisError {
  original: string;
  corrected: string;
  rule_id: string;
  explanation: string;
}

export interface GrammarAnalysis {
  errors: GrammarAnalysisError[];
  score: number;
}

// ---------- Gamification / Analytics ----------
export interface AchievementInfo {
  achievement_id: string;
  title: string;
  emoji: string;
  description: string;
  earned: boolean;
  earned_at: string | null;
}

export interface WeeklyStats {
  lessons_this_week: number;
  minutes_studied: number;
  vocab_learned: number;
  pronunciation_sessions: number;
  avg_pronunciation: number | null;
  xp_earned: number;
  per_day: Array<{ date: string; lessons: number }>;
}

export interface PronunciationTrendPoint {
  date: string;
  avg_score: number;
  session_count: number;
}

export interface HeatmapCell {
  date: string;
  count: number;
  level: 0 | 1 | 2 | 3 | 4;
}

export interface XPProgressionPoint {
  date: string;
  cumulative_xp: number;
  level_at_time: CEFRLevel;
}

export interface XPProgression {
  points: XPProgressionPoint[];
  thresholds: Record<CEFRLevel, number>;
}

export interface FullAnalytics {
  weekly_stats: WeeklyStats;
  pronunciation_trend: PronunciationTrendPoint[];
  exam_readiness: ExamReadiness;
  achievements: { earned: number; total: number };
  grammar_weak_areas: Array<{ rule_id: string; count: number }>;
}
