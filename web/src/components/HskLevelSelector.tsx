"use client";

import { Card } from "@/components/ui";
import { ALL_LEVELS, tierForLevel } from "@/lib/hsk";
import { usePreferredLevel } from "@/lib/level";

export default function HskLevelSelector({
  byLevel,
}: {
  byLevel: { level: number; total: number; due: number }[];
}) {
  const [level, setLevel] = usePreferredLevel(1);
  const tier = tierForLevel(level);
  const stat = byLevel.find((b) => b.level === level);

  return (
    <Card className="flex flex-col gap-3 border-jade/30 bg-jade-soft/60 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex-1">
        <p className="font-display text-base font-bold">Trình độ HSK bạn muốn học</p>
        <p className="mt-0.5 text-sm text-ink-soft">
          Chọn cấp độ — Từ vựng, Ôn tập, Luyện viết, Thi thử và Chủ đề sẽ tự động đồng bộ theo.
        </p>
      </div>
      <div className="flex shrink-0 items-center gap-3">
        {stat && (
          <span className="font-data text-xs text-ink-soft whitespace-nowrap">
            {stat.total} từ{stat.due > 0 ? ` · ${stat.due} cần ôn` : ""}
          </span>
        )}
        <div className="relative">
          <select
            value={level}
            onChange={(e) => setLevel(Number(e.target.value))}
            className="appearance-none rounded-full border border-jade/40 bg-paper-raised py-2 pl-4 pr-9 text-sm font-semibold text-ink outline-none focus:border-jade"
            aria-label="Chọn trình độ HSK"
          >
            {ALL_LEVELS.map((lv) => (
              <option key={lv} value={lv}>
                HSK {lv} · {tierForLevel(lv).label}
              </option>
            ))}
          </select>
          <span className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-ink-soft">
            ▾
          </span>
        </div>
      </div>
      <span className="sr-only">{tier.sublabel}</span>
    </Card>
  );
}
