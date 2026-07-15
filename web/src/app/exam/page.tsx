"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type ExamBestLevel } from "@/lib/api";
import { Card, SectionTitle } from "@/components/ui";
import { TIERS } from "@/lib/hsk";

export default function ExamPickerPage() {
  const [best, setBest] = useState<Record<number, ExamBestLevel>>({});

  useEffect(() => {
    api.examBest().then((d) => {
      const map: Record<number, ExamBestLevel> = {};
      for (const l of d.levels) map[l.hsk_level] = l;
      setBest(map);
    });
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-display text-2xl font-bold">Thi thử HSK</h1>
        <p className="mt-1 text-ink-soft">
          Chọn cấp độ để làm bài thi thử — gồm 3 phần: Nghe, Đọc/Từ vựng, Ngữ pháp/Điền từ. Đạt từ 60% trở lên là Đạt.
        </p>
      </div>

      {TIERS.map((tier) => (
        <section key={tier.id}>
          <SectionTitle sub={tier.sublabel}>{tier.label}</SectionTitle>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
            {tier.levels.map((lv) => {
              const b = best[lv];
              return (
                <Link key={lv} href={`/exam/${lv}`}>
                  <Card className="flex h-full flex-col gap-2 transition-transform hover:-translate-y-0.5">
                    <div className="flex items-center justify-between">
                      <span className="font-display text-xl font-bold">HSK {lv}</span>
                      {b && (
                        <span
                          className={`rounded-full px-2 py-0.5 text-xs font-semibold ${
                            b.pass_count > 0 ? "bg-jade-soft text-jade" : "bg-brass-soft text-brass"
                          }`}
                        >
                          {b.pass_count > 0 ? "Đã đạt" : "Chưa đạt"}
                        </span>
                      )}
                    </div>
                    {b ? (
                      <p className="font-data text-sm text-ink-soft">
                        Điểm cao nhất: {b.best_pct}% · {b.attempt_count} lượt thi
                      </p>
                    ) : (
                      <p className="text-sm text-ink-soft">Chưa thi lần nào</p>
                    )}
                  </Card>
                </Link>
              );
            })}
          </div>
        </section>
      ))}
    </div>
  );
}
