"use client";

import { useEffect, useState } from "react";
import { api, type GrammarPoint } from "@/lib/api";
import { speak } from "@/lib/speech";
import LevelPicker from "@/components/LevelPicker";
import { Card, SectionTitle } from "@/components/ui";
import { usePreferredLevel } from "@/lib/level";

export default function GrammarPage() {
  const [level, setLevel] = usePreferredLevel(1);
  const [points, setPoints] = useState<GrammarPoint[]>([]);
  const [open, setOpen] = useState<string | null>(null);
  const [loadError, setLoadError] = useState(false);

  useEffect(() => {
    let active = true;
    // eslint-disable-next-line react-hooks/set-state-in-effect -- reset state when level changes
    setLoadError(false);
    setOpen(null);
    api.grammarPoints(level).then(
      (d) => {
        if (active) setPoints(d.points);
      },
      () => {
        if (active) setLoadError(true);
      }
    );
    return () => {
      active = false;
    };
  }, [level]);

  return (
    <div className="space-y-5">
      <SectionTitle sub="Các điểm ngữ pháp trọng tâm theo từng cấp, giải thích tiếng Việt kèm neo nhớ Hán-Việt">
        Ngữ pháp HSK
      </SectionTitle>
      <LevelPicker level={level} onChange={setLevel} />
      {loadError && <p className="text-sm text-seal">Không tải được nội dung. Vui lòng thử lại.</p>}

      <div className="space-y-3">
        {points.map((p, i) => {
          const isOpen = open === p.id;
          return (
            <Card key={p.id} className="p-0 overflow-hidden">
              <button
                onClick={() => setOpen(isOpen ? null : p.id)}
                className="flex w-full items-center justify-between gap-3 p-4 text-left"
              >
                <div>
                  <p className="font-semibold">
                    <span className="mr-2 font-data text-xs text-ink-soft">{i + 1}.</span>
                    {p.title}
                  </p>
                  <p className="mt-0.5 font-data text-sm text-jade">{p.pattern}</p>
                </div>
                <span className="text-ink-soft">{isOpen ? "−" : "+"}</span>
              </button>

              {isOpen && (
                <div className="space-y-4 border-t border-line p-4">
                  <p className="text-sm leading-relaxed">{p.explanation}</p>
                  {p.examples.map((ex) => (
                    <div key={ex.cn} className="rounded-xl bg-paper p-3">
                      <div className="flex items-start justify-between gap-2">
                        <p className="font-display text-lg leading-snug">{ex.cn}</p>
                        <button
                          onClick={() => speak(ex.cn)}
                          aria-label="Nghe phát âm"
                          className="shrink-0 rounded-full border border-line px-2.5 py-1 text-sm hover:bg-paper-raised"
                        >
                          🔊
                        </button>
                      </div>
                      <p className="mt-1 text-sm text-ink-soft">{ex.pinyin}</p>
                      <p className="text-sm italic text-jade">Hán-Việt: {ex.hv}</p>
                      <p className="mt-1 text-sm">{ex.vi}</p>
                    </div>
                  ))}
                </div>
              )}
            </Card>
          );
        })}
      </div>

      {points.length === 0 && !loadError && (
        <p className="text-center text-sm text-ink-soft">Đang tải…</p>
      )}
    </div>
  );
}
