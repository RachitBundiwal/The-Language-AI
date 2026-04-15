import { useQuery } from "@tanstack/react-query";
import { get } from "@/hooks/useApi";
import { API } from "@/constants/api";
import type {
  DashboardStats,
  ExamHistoryEntry,
  ExamReadiness,
  LessonSummary,
  PronunciationHistoryEntry,
  VocabularyCard,
} from "@/types";

export function useStats() {
  return useQuery<DashboardStats>({
    queryKey: ["stats"],
    queryFn: () => get<DashboardStats>(API.stats),
    staleTime: 60_000,
  });
}

export function useLessons(level?: string) {
  return useQuery<Record<string, LessonSummary[]> | LessonSummary[]>({
    queryKey: ["lessons", level ?? "all"],
    queryFn: () => {
      const url = level && level !== "all" ? `${API.lessons}/level/${level}` : `${API.lessons}/`;
      return get(url);
    },
  });
}

export function useVocabDue() {
  return useQuery<VocabularyCard[]>({
    queryKey: ["vocab-due"],
    queryFn: () => get<VocabularyCard[]>(API.vocabDue),
  });
}

export function usePronunciationHistory() {
  return useQuery<PronunciationHistoryEntry[]>({
    queryKey: ["pronunciation-history"],
    queryFn: () => get<PronunciationHistoryEntry[]>(API.pronunciationHistory),
  });
}

export function useExamReadiness() {
  return useQuery<ExamReadiness>({
    queryKey: ["exam-readiness"],
    queryFn: () => get<ExamReadiness>(API.examReadiness),
  });
}

export function useExamHistory() {
  return useQuery<ExamHistoryEntry[]>({
    queryKey: ["exam-history"],
    queryFn: () => get<ExamHistoryEntry[]>(API.examHistory),
  });
}
