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
