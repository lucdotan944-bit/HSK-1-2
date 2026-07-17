// Shared HSK 1-9 tier configuration — groups the 9 official HSK 3.0 levels
// into 3 difficulty bands for navigation (words, review, writing, exam...).
export type Tier = {
  id: string;
  label: string;
  sublabel: string;
  levels: number[];
};

export const TIERS: Tier[] = [
  { id: "so-cap", label: "Sơ cấp", sublabel: "HSK 1-3", levels: [1, 2, 3] },
  { id: "trung-cap", label: "Trung cấp", sublabel: "HSK 4-6", levels: [4, 5, 6] },
  { id: "cao-cap", label: "Cao cấp", sublabel: "HSK 7-9", levels: [7, 8, 9] },
];

export function tierForLevel(level: number): Tier {
  return TIERS.find((t) => t.levels.includes(level)) ?? TIERS[0];
}

export const ALL_LEVELS = TIERS.flatMap((t) => t.levels);

// A fresh account starts with every word already due (next_review defaults to
// now), so the raw due-count can read as an intimidating backlog (e.g.
// "10943 cần ôn") even though a review session only ever pulls one batch at
// a time. Cap the *displayed* number at that batch size — the real count is
// unaffected, this only softens how it's framed to the learner.
export const REVIEW_SESSION_SIZE = 20;

export function formatDueCount(due: number): string {
  return due > REVIEW_SESSION_SIZE ? `${REVIEW_SESSION_SIZE}+` : String(due);
}
