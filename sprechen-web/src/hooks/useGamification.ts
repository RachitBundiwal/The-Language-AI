import { useEffect, useRef } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { get, post, queryClient } from "@/hooks/useApi";
import { API } from "@/constants/api";
import { useToastStore } from "@/store/toastStore";
import type {
  AchievementInfo,
  FullAnalytics,
  HeatmapCell,
  PronunciationResponse,
  PronunciationTrendPoint,
  WeeklyStats,
  XPProgression,
} from "@/types";

export function useAchievements() {
  return useQuery<AchievementInfo[]>({
    queryKey: ["achievements"],
    queryFn: () => get<AchievementInfo[]>(API.analyticsAchievements),
    staleTime: 30_000,
  });
}

export function useFullAnalytics() {
  return useQuery<FullAnalytics>({
    queryKey: ["analytics-full"],
    queryFn: () => get<FullAnalytics>(API.analyticsFull),
    staleTime: 30_000,
  });
}

export function useWeeklyStats() {
  return useQuery<WeeklyStats>({
    queryKey: ["analytics-weekly"],
    queryFn: () => get<WeeklyStats>(API.analyticsWeekly),
    staleTime: 30_000,
  });
}

export function useStudyHeatmap() {
  return useQuery<HeatmapCell[]>({
    queryKey: ["analytics-heatmap"],
    queryFn: () => get<HeatmapCell[]>(API.analyticsHeatmap),
    staleTime: 60_000,
  });
}

export function usePronunciationTrend(days = 30) {
  return useQuery<PronunciationTrendPoint[]>({
    queryKey: ["analytics-pron-trend", days],
    queryFn: () =>
      get<PronunciationTrendPoint[]>(
        `${API.analyticsPronunciationTrend}?days=${days}`,
      ),
    staleTime: 30_000,
  });
}

export function useXPProgression() {
  return useQuery<XPProgression>({
    queryKey: ["analytics-xp-progression"],
    queryFn: () => get<XPProgression>(API.analyticsXpProgression),
    staleTime: 30_000,
  });
}

async function checkNewAchievements(
  knownIds: Set<string>,
): Promise<AchievementInfo[]> {
  const list = await get<AchievementInfo[]>(API.analyticsAchievements);
  const earnedNew = list.filter((a) => a.earned && !knownIds.has(a.achievement_id));
  queryClient.setQueryData(["achievements"], list);
  return earnedNew;
}

function invalidateProgressQueries() {
  queryClient.invalidateQueries({ queryKey: ["stats"] });
  queryClient.invalidateQueries({ queryKey: ["analytics-full"] });
  queryClient.invalidateQueries({ queryKey: ["analytics-weekly"] });
  queryClient.invalidateQueries({ queryKey: ["analytics-heatmap"] });
  queryClient.invalidateQueries({ queryKey: ["analytics-xp-progression"] });
}

/**
 * Tracks earned achievement IDs across mounts so we only toast newly-earned ones.
 * Initialized lazily on first call from any hook consumer.
 */
const knownEarnedIds = new Set<string>();
let knownInitialized = false;

export function useAchievementWatcher() {
  const pushMany = useToastStore((s) => s.pushMany);
  const initRef = useRef(false);

  useEffect(() => {
    if (initRef.current || knownInitialized) return;
    initRef.current = true;
    (async () => {
      try {
        const list = await get<AchievementInfo[]>(API.analyticsAchievements);
        list.filter((a) => a.earned).forEach((a) => knownEarnedIds.add(a.achievement_id));
        knownInitialized = true;
        queryClient.setQueryData(["achievements"], list);
      } catch {
        // ignore — will retry on next mutation
      }
    })();
  }, [pushMany]);
}

async function pushNewAchievements(
  pushMany: (a: AchievementInfo[]) => void,
): Promise<void> {
  const newOnes = await checkNewAchievements(knownEarnedIds);
  if (newOnes.length > 0) {
    newOnes.forEach((a) => knownEarnedIds.add(a.achievement_id));
    pushMany(newOnes);
  }
}

export function useCompleteLesson() {
  const pushMany = useToastStore((s) => s.pushMany);
  return useMutation({
    mutationFn: async (payload: { lessonId: number; score: number }) => {
      await post(API.completeLesson(payload.lessonId), {
        score: payload.score,
      });
    },
    onSuccess: async () => {
      invalidateProgressQueries();
      queryClient.invalidateQueries({ queryKey: ["lessons"] });
      await pushNewAchievements(pushMany);
    },
  });
}

export function useSavePronunciation() {
  const pushMany = useToastStore((s) => s.pushMany);
  return useMutation({
    mutationFn: async (payload: {
      reference_text: string;
      pronunciation: PronunciationResponse;
      lesson_id?: number;
    }) => {
      await post("/api/v1/progress/pronunciation/save", payload);
    },
    onSuccess: async () => {
      invalidateProgressQueries();
      queryClient.invalidateQueries({ queryKey: ["pronunciation-history"] });
      await pushNewAchievements(pushMany);
    },
  });
}

export function useExamCompleted() {
  const pushMany = useToastStore((s) => s.pushMany);
  return useMutation({
    mutationFn: async () => {
      // Exam submission already happened separately; this just refreshes + checks.
      return;
    },
    onSuccess: async () => {
      invalidateProgressQueries();
      queryClient.invalidateQueries({ queryKey: ["exam-history"] });
      queryClient.invalidateQueries({ queryKey: ["exam-readiness"] });
      await pushNewAchievements(pushMany);
    },
  });
}
