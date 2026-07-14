// Typed client for the Hán Ngữ+ FastAPI backend. All calls go through
// Next.js `/api/*` rewrites (see next.config.ts), so this file uses
// relative paths and works identically on server and client.

// Server-side fetches (in Server Components) run in Node and need an
// absolute URL — they bypass Next's own rewrite proxy. Client-side fetches
// stay relative so they go through the browser's same-origin request to
// Next.js, which then rewrites `/api/*` to the FastAPI backend (see
// next.config.ts) without needing CORS.
const SERVER_API_BASE = process.env.API_ORIGIN || "http://127.0.0.1:8000";

async function jsonFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const base = typeof window === "undefined" ? SERVER_API_BASE : "";
  const res = await fetch(`${base}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`API ${path} failed: ${res.status}`);
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
    listening: { dialogue_id: string; simplified: string; pinyin: string; vietnamese: string } | null;
    speaking: Word | null;
    conversation_scenario_id: string | null;
  };
};

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
  themes: () => jsonFetch<{ themes: Theme[] }>("/api/themes"),
  theme: (id: string) => jsonFetch<{ theme: Theme; words: Word[] }>(`/api/themes/${id}`),
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
  placementQuestions: (count = 15) => jsonFetch<{ questions: QuizChoice[] }>(`/api/quiz/choices/2?count=${count}`),
  submitPlacement: (answers: { word_id: number; hsk_level: number; correct: boolean }[]) =>
    jsonFetch<{ recommended_level: number; accuracy: number; newly_earned_badges: string[] }>(`/api/placement/submit`, {
      method: "POST",
      body: JSON.stringify({ answers }),
    }),
  writingCharacters: (hskLevel = 2) =>
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
  dailySession: () => jsonFetch<DailySession>("/api/daily-session"),
  conversation: (scenarioId: string) => jsonFetch<ConversationStart>(`/api/conversation/${scenarioId}`),
  conversationRespond: (scenarioId: string, nodeId: string, choiceId: string) =>
    jsonFetch<{ node_id: string; node: ConversationNode; is_end: boolean; newly_earned_badges: string[] }>(
      `/api/conversation/${scenarioId}/respond`,
      { method: "POST", body: JSON.stringify({ node_id: nodeId, choice_id: choiceId }) }
    ),
};

export function meaningsList(m: string | string[]): string[] {
  return Array.isArray(m) ? m : m.split(",").map((s) => s.trim());
}
