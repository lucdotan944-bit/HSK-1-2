"use client";

import { TIERS } from "@/lib/hsk";

export default function LevelPicker({
  level,
  onChange,
}: {
  level: number;
  onChange: (level: number) => void;
}) {
  return (
    <div className="flex flex-col gap-2">
      {TIERS.map((tier) => (
        <div key={tier.id} className="flex flex-wrap items-center gap-1.5">
          <span className="w-24 shrink-0 text-xs font-medium text-ink-soft">
            {tier.label} <span className="font-data">({tier.sublabel})</span>
          </span>
          {tier.levels.map((lv) => (
            <button
              key={lv}
              onClick={() => onChange(lv)}
              className={`rounded-full px-3.5 py-1.5 text-sm font-semibold transition-colors ${
                level === lv ? "bg-jade text-white" : "border border-line text-ink hover:bg-paper-raised"
              }`}
            >
              HSK {lv}
            </button>
          ))}
        </div>
      ))}
    </div>
  );
}
