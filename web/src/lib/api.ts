// Typed client for the Hán Ngữ+ FastAPI backend. All calls go through
// Next.js `/api/*` rewrites (see next.config.ts), so this file uses
// relative paths and works identically on server and client.

// Server-side fetches (in Server Components) run in Node and need an
// absolute URL — they bypass Next's own rewrite proxy. Client-side fetches
// stay relative so they go through the browser's same-origin request to
// Next.js, which then rewrites `/api/*` to the FastAPI backend (see
// next.config.ts) without needing CORS.
const SERVER_API_BASE = process.env.API_ORIGIN || "http://127.0.0.1:8000";

export class ApiError extends Error {
  status: number;
  constructor(path: string, status: number) {
    super(`API ${path} failed: ${status}`);
    this.status = status;
  }
}

async function jsonFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const base = typeof window === "undefined" ? SERVER_API_BASE : "";
  const res = await fetch(`${base}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    cache: "no-store",
  });
  if (!res.ok) throw new ApiError(path, res.status);
  return res.json();
}

export type Word = {
  id: number;
  simplified: string;
  pinyin: string;
  meanings: string | string[];
  hsk_level: number;
  radical?: string;
  sino_viet?: string;
  repetitions?: number;
  sentence_cn?: string;
  sentence_vi?: string;
  context_note?: string;
};

export type GamifyState = {
  xp: number;
  current_streak: number;
  longest_streak: number;
  placement_level: number;
  badges: { badge_id: string; name: string; icon: string; desc: string; earned_at: string }[];
};

export type Badge = { badge_id: string; name: string; icon: string; desc: string; earned: boolean };

export type Stats = {
  hsk1: number;
  hsk2: number;
  due: number;
  total: number;
  learned: number;
  due_hsk1: number;
  due_hsk2: number;
  dialogues: number;
  by_level: { level: number; total: number; due: number }[];
};

export type Theme = {
  id: string;
  name: string;
  icon: string;
  description: string;
  total_words: number;
  learned_words: number;
};

export type QuizChoice = {
  word_id: number;
  simplified: string;
  pinyin: string;
  hsk_level: number;
  correct_meaning: string;
  choices: string[];
};

export type DialogueSummary = {
  id: string;
  title: string;
  context: string;
  hsk_level: number;
  line_count: number;
};

export type DialogueLine = {
  id: number;
  dialogue_id: string;
  speaker: string;
  simplified: string;
  pinyin: string;
  vietnamese: string;
  sort_order: number;
};

export type WritingChar = {
  character: string;
  hsk_level: number;
  practiced: boolean;
  attempts: number;
  best_mistakes: number | null;
  mastered: boolean;
};

export type SkillBreakdown = {
  skills: Record<"vocab" | "grammar" | "listening" | "speaking", { label: string; score: number | null }>;
  weakest_skill: string | null;
  strongest_skill: string | null;
  explanation_vi: string;
};

export type DailySession = {
  focus_skill: string | null;
  skills: SkillBreakdown["skills"];
  blocks: {
    review: Word[];
    listening: { dialogue_id: string; simplified: string; pinyin: string; vietnamese: string; hsk_level: number } | null;
    speaking: Word | null;
    conversation_scenario_id: string | null;
    conversation_hsk_level: number | null;
  };
};

export type ExamMCQuestion = {
  word_id: number;
  simplified: string;
  pinyin: string;
  hsk_level: number;
  correct_meaning: string;
  choices: string[];
  section: "listening" | "reading";
};
export type ExamClozeQuestion = {
  word_id: number;
  section: "grammar";
  sentence_blanked: string;
  sentence_vi: string;
  correct_word: string;
  choices: string[];
};
export type ExamQuestion = ExamMCQuestion | ExamClozeQuestion;

export type ExamStart = { hsk_level: number; questions: ExamQuestion[]; time_limit_seconds: number };
export type ExamSectionScore = { total: number; correct: number; pct: number | null };
export type ExamSubmitResult = {
  score_pct: number;
  passed: boolean;
  correct_count: number;
  total_questions: number;
  section_scores: Record<string, ExamSectionScore>;
  newly_earned_badges: string[];
};
export type ExamSession = {
  id: number;
  hsk_level: number;
  total_questions: number;
  correct_count: number;
  section_scores: Record<string, ExamSectionScore>;
  score_pct: number;
  passed: number;
  duration_seconds: number;
  created_at: string;
};
export type ExamBestLevel = { hsk_level: number; best_pct: number | null; pass_count: number; attempt_count: number };

export type ConversationChoice = { id: string; cn: string; pinyin: string; vi: string; next: string };
export type ConversationNode = {
  npc: { cn: string; pinyin: string; vi: string };
  choices: ConversationChoice[];
};
export type ConversationStart = {
  scenario_id: string;
  title: string;
  hsk_level: number;
  start: string;
  node: ConversationNode;
};

export const api = {
  stats: () => jsonFetch<Stats>("/api/stats"),
  gamifyState: () => jsonFetch<GamifyState>("/api/gamify/state"),
  badges: () => jsonFetch<{ badges: Badge[] }>("/api/badges"),
  themes: (level?: number) => jsonFetch<{ themes: Theme[] }>(`/api/themes${level ? `?level=${level}` : ""}`),
  theme: (id: string, level?: number) =>
    jsonFetch<{ theme: Theme; words: Word[] }>(`/api/themes/${id}${level ? `?level=${level}` : ""}`),
  learnThemeWord: (themeId: string, wordId: number) =>
    jsonFetch<{ ok: true; newly_earned_badges: string[] }>(`/api/themes/${themeId}/learn/${wordId}`, {
      method: "POST",
    }),
  relatedDialogues: (themeId: string) =>
    jsonFetch<{ dialogues: DialogueSummary[] }>(`/api/themes/${themeId}/related-dialogues`),
  quizChoices: (hskLevel: number, opts?: { themeId?: string; count?: number }) =>
    jsonFetch<{ questions: QuizChoice[] }>(
      `/api/quiz/choices/${hskLevel}?${new URLSearchParams({
        ...(opts?.themeId ? { theme_id: opts.themeId } : {}),
        ...(opts?.count ? { count: String(opts.count) } : {}),
      })}`
    ),
  submitThemeQuiz: (themeId: string, results: { word_id: number; correct: boolean }[]) =>
    jsonFetch<{ ok: true; correct: number; total: number; newly_earned_badges: string[] }>(`/api/quiz/theme-result`, {
      method: "POST",
      body: JSON.stringify({ theme_id: themeId, results }),
    }),
  submitQuiz: (wordId: number, correct: boolean, quizType: "quiz" | "listening" = "quiz") =>
    jsonFetch<{ ok: true }>(`/api/quiz`, {
      method: "POST",
      body: JSON.stringify({ word_id: wordId, correct, quiz_type: quizType }),
    }),
  reviewWords: (hskLevel: number, limit = 20) =>
    jsonFetch<{ words: Word[] }>(`/api/review/${hskLevel}?limit=${limit}`),
  submitReview: (wordId: number, quality: number) =>
    jsonFetch<{ next_review: string; repetitions: number; easiness: number; interval: number; newly_earned_badges: string[] }>(
      `/api/review`,
      { method: "POST", body: JSON.stringify({ word_id: wordId, quality }) }
    ),
  wordsByLevel: (hskLevel: number) => jsonFetch<{ words: Word[] }>(`/api/words/${hskLevel}`),
  progress: () =>
    jsonFetch<{
      levels: { hsk_level: number; total: number; mastered: number; seen: number; accuracy: number | null }[];
      today_reviewed: number;
    }>("/api/progress"),
  dialogues: (level?: number) =>
    jsonFetch<{ dialogues: DialogueSummary[] }>(`/api/dialogues${level ? `?level=${level}` : ""}`),
  dialogue: (id: string) => jsonFetch<{ dialogue: DialogueSummary; lines: DialogueLine[] }>(`/api/dialogues/${id}`),
  placementQuestions: (perLevel = 2) =>
    jsonFetch<{ questions: QuizChoice[] }>(`/api/placement/questions?per_level=${perLevel}`),
  submitPlacement: (answers: { word_id: number; hsk_level: number; correct: boolean }[]) =>
    jsonFetch<{ recommended_level: number; accuracy: number; newly_earned_badges: string[] }>(`/api/placement/submit`, {
      method: "POST",
      body: JSON.stringify({ answers }),
    }),
  writingCharacters: (hskLevel = 1) =>
    jsonFetch<{ characters: WritingChar[] }>(`/api/writing/characters?hsk_level=${hskLevel}`),
  completeWriting: (character: string, mistakes: number) =>
    jsonFetch<{ ok: true; newly_earned_badges: string[] }>(`/api/writing/complete`, {
      method: "POST",
      body: JSON.stringify({ character, mistakes }),
    }),
  logPronunciation: (data: { word_id?: number; target_text: string; recognized_text: string; score: "ok" | "warn" | "fail" }) =>
    jsonFetch(`/api/pronunciation/log`, { method: "POST", body: JSON.stringify(data) }),
  skillBreakdown: () => jsonFetch<SkillBreakdown>("/api/skills/breakdown"),
  hskMapping: () =>
    jsonFetch<{ mapping: { old: number; new_range: [number, number]; desc: string }[] }>("/api/hsk-mapping"),
  dailySession: (level?: number) => jsonFetch<DailySession>(`/api/daily-session${level ? `?level=${level}` : ""}`),
  conversation: (scenarioId: string) => jsonFetch<ConversationStart>(`/api/conversation/${scenarioId}`),
  conversationRespond: (scenarioId: string, nodeId: string, choiceId: string) =>
    jsonFetch<{ node_id: string; node: ConversationNode; is_end: boolean; newly_earned_badges: string[] }>(
      `/api/conversation/${scenarioId}/respond`,
      { method: "POST", body: JSON.stringify({ node_id: nodeId, choice_id: choiceId }) }
    ),
  examStart: (hskLevel: number, count?: number) =>
    jsonFetch<ExamStart>(`/api/exam/${hskLevel}/start${count ? `?count=${count}` : ""}`),
  examSubmit: (hskLevel: number, answers: { section: string; correct: boolean }[], durationSeconds: number) =>
    jsonFetch<ExamSubmitResult>(`/api/exam/${hskLevel}/submit`, {
      method: "POST",
      body: JSON.stringify({ answers, duration_seconds: durationSeconds }),
    }),
  examHistory: (hskLevel?: number) =>
    jsonFetch<{ sessions: ExamSession[] }>(`/api/exam/history${hskLevel ? `?hsk_level=${hskLevel}` : ""}`),
  examBest: () => jsonFetch<{ levels: ExamBestLevel[] }>(`/api/exam/best`),
};

export function meaningsList(m: string | string[]): string[] {
  return Array.isArray(m) ? m : m.split(",").map((s) => s.trim());
}
