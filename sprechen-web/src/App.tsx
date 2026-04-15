import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/hooks/useApi";
import { Layout } from "@/components/layout/Layout";
import { AchievementToast } from "@/components/ui/AchievementToast";
import { AchievementWatcher } from "@/components/AchievementWatcher";
import { OfflineNotice } from "@/components/ui/OfflineNotice";
import { KeyboardShortcuts } from "@/components/ui/KeyboardShortcuts";
import { HomePage } from "@/pages/HomePage";
import { LessonsPage } from "@/pages/LessonsPage";
import { LessonDetailPage } from "@/pages/LessonDetailPage";
import { VoiceExercisePage } from "@/pages/VoiceExercisePage";
import { ConversationPage } from "@/pages/ConversationPage";
import { VocabularyPage } from "@/pages/VocabularyPage";
import { ExamPage } from "@/pages/ExamPage";
import { ExamResultPage } from "@/pages/ExamResultPage";
import { ProgressPage } from "@/pages/ProgressPage";
import { SettingsPage } from "@/pages/SettingsPage";

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AchievementToast />
      <OfflineNotice />
      <BrowserRouter>
        <AchievementWatcher />
        <KeyboardShortcuts />
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/lessons" element={<LessonsPage />} />
            <Route path="/lessons/:id" element={<LessonDetailPage />} />
            <Route path="/voice" element={<VoiceExercisePage />} />
            <Route path="/conversation" element={<ConversationPage />} />
            <Route path="/vocabulary" element={<VocabularyPage />} />
            <Route path="/exam" element={<ExamPage />} />
            <Route path="/exam/result" element={<ExamResultPage />} />
            <Route path="/progress" element={<ProgressPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
