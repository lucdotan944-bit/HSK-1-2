"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type Theme } from "@/lib/api";
import { Card, SectionTitle } from "@/components/ui";
import { usePreferredLevel } from "@/lib/level";

export default function HomeThemesSection({ initialThemes }: { initialThemes: Theme[] }) {
  const [level] = usePreferredLevel(1);
  const [themes, setThemes] = useState(initialThemes);

  useEffect(() => {
    let active = true;
    api.themes(level).then(
      (d) => {
        if (active) setThemes(d.themes);
      },
      () => {} // keep showing initialThemes (server-rendered fallback) on failure
    );
    return () => {
      active = false;
    };
  }, [level]);

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
