"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type Theme } from "@/lib/api";
import { Card, SectionTitle, Button } from "@/components/ui";
import { usePreferredLevel } from "@/lib/level";

export default function HomeThemesSection({
  initialThemes,
  byLevel,
}: {
  initialThemes: Theme[];
  byLevel: { level: number; total: number; due: number }[];
}) {
  const [level] = usePreferredLevel(1);
  const [themes, setThemes] = useState(initialThemes);

  useEffect(() => {
    let active = true;
    api.themes(level).then((d) => {
      if (active) setThemes(d.themes);
    });
    return () => {
      active = false;
    };
  }, [level]);

  // Chủ đề hiện chỉ có dữ liệu thủ công cho HSK 1-2 — ở các cấp cao hơn,
  // thay bằng lối vào nhanh theo cấp thay vì hiển thị lưới chủ đề trống.
  if (level >= 3) {
    const stat = byLevel.find((b) => b.level === level);
    return (
      <section>
        <SectionTitle sub={`Chủ đề theo nhóm chưa có ở HSK ${level} — đây là lối vào nhanh cho cấp bạn đã chọn`}>
          Từ vựng HSK {level}
        </SectionTitle>
        <Card className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex gap-4 font-data text-sm">
            <span>
              <span className="font-bold text-jade">{stat?.total ?? 0}</span> từ
            </span>
            <span>
              <span className="font-bold text-seal">{stat?.due ?? 0}</span> cần ôn
            </span>
          </div>
          <div className="flex flex-wrap gap-2">
            <Link href="/words">
              <Button variant="ghost">Xem danh sách từ</Button>
            </Link>
            <Link href="/review">
              <Button variant="ghost">Ôn tập</Button>
            </Link>
            <Link href={`/exam/${level}`}>
              <Button variant="secondary">Thi thử HSK {level}</Button>
            </Link>
          </div>
        </Card>
      </section>
    );
  }

  const available = themes.filter((t) => t.total_words > 0);

  return (
    <section>
      <SectionTitle sub={`Chọn một chủ đề để học từ vựng HSK ${level} theo nhóm`}>Chủ đề</SectionTitle>
      {available.length === 0 ? (
        <p className="text-sm text-ink-soft">Chưa có chủ đề nào cho HSK {level}.</p>
      ) : (
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          {available.map((t) => (
            <Link key={t.id} href={`/lesson/${t.id}`}>
              <Card className="flex h-full flex-col gap-2 transition-transform hover:-translate-y-0.5">
                <span className="text-2xl">{t.icon}</span>
                <span className="font-semibold leading-tight">{t.name}</span>
                <span className="font-data text-xs text-ink-soft">
                  {t.learned_words}/{t.total_words} từ
                </span>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </section>
  );
}
