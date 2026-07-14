"use client";

import { useEffect, useRef, useState } from "react";
import Script from "next/script";
import { api, meaningsList, type WritingChar } from "@/lib/api";
import { Button, Card } from "@/components/ui";
import { useBadgeToast } from "@/components/BadgeToast";

// HanziWriter types aren't published standalone; declare the minimal shape we use.
interface HanziWriterInstance {
  showCharacter: () => void;
  animateCharacter: () => void;
  quiz: (opts: { showOutline: boolean; onComplete: (summary: { totalMistakes: number }) => void }) => void;
}
declare global {
  interface Window {
    HanziWriter?: {
      create: (elId: string, char: string, opts: Record<string, unknown>) => HanziWriterInstance;
    };
  }
}

export default function WritingPage() {
  const { announce, toastNode } = useBadgeToast();
  const [level, setLevel] = useState(1);
  const [chars, setChars] = useState<WritingChar[]>([]);
  const [active, setActive] = useState<string | null>(null);
  const [wordInfo, setWordInfo] = useState<string>("");
  const [status, setStatus] = useState("");
  const [result, setResult] = useState<{ mistakes: number } | null>(null);
  const [scriptReady, setScriptReady] = useState(() => typeof window !== "undefined" && !!window.HanziWriter);
  const writerRef = useRef<HanziWriterInstance | null>(null);

  useEffect(() => {
    api.writingCharacters(level).then((d) => setChars(d.characters.filter((c) => c.hsk_level === level)));
  }, [level]);

  useEffect(() => {
    if (!active || !scriptReady || !window.HanziWriter) return;
    // eslint-disable-next-line react-hooks/set-state-in-effect -- reset practice UI when switching characters
    setResult(null);
    setStatus("");
    api.wordsByLevel(level).then((d) => {
      const w = d.words.find((w) => w.simplified.includes(active));
      setWordInfo(w ? `${w.pinyin} — ${meaningsList(w.meanings)[0]}${w.sino_viet ? ` (${w.sino_viet})` : ""}` : "");
    });
    const el = document.getElementById("hanziTarget");
    if (el) el.innerHTML = "";
    writerRef.current = window.HanziWriter.create("hanziTarget", active, {
      width: 240,
      height: 240,
      padding: 12,
      strokeColor: "#16201c",
      outlineColor: "#dee2e6",
      showCharacter: true,
      showOutline: true,
      strokeAnimationSpeed: 1,
      delayBetweenStrokes: 200,
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [active, scriptReady]);

  function animate() {
    if (!writerRef.current) return;
    setResult(null);
    setStatus("Xem cách viết");
    writerRef.current.showCharacter();
    writerRef.current.animateCharacter();
  }

  function startQuiz() {
    if (!writerRef.current || !active) return;
    setResult(null);
    setStatus("Vẽ từng nét theo thứ tự");
    writerRef.current.quiz({
      showOutline: true,
      onComplete: async (summary) => {
        const mistakes = summary.totalMistakes;
        const r = await api.completeWriting(active, mistakes);
        announce(r.newly_earned_badges);
        setResult({ mistakes });
        setStatus("");
      },
    });
  }

  return (
    <div className="mx-auto max-w-lg space-y-5">
      <Script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3/dist/hanzi-writer.min.js" onLoad={() => setScriptReady(true)} />
      {toastNode}
      <h1 className="font-display text-2xl font-bold">Luyện viết chữ Hán</h1>

      {!active ? (
        <>
          <div className="flex gap-2">
            {[1, 2].map((lv) => (
              <button
                key={lv}
                onClick={() => setLevel(lv)}
                className={`rounded-full px-4 py-1.5 text-sm font-semibold ${
                  level === lv ? "bg-jade text-white" : "border border-line"
                }`}
              >
                HSK {lv}
              </button>
            ))}
          </div>
          <div className="grid grid-cols-6 gap-2 sm:grid-cols-8">
            {chars.map((c) => (
              <button
                key={c.character}
                onClick={() => setActive(c.character)}
                title={c.mastered ? "Đã thành thạo" : c.practiced ? `Đã luyện ${c.attempts} lần` : "Chưa luyện"}
                className={`font-display flex aspect-square items-center justify-center rounded-xl border text-2xl ${
                  c.mastered
                    ? "border-jade bg-jade-soft"
                    : c.practiced
                    ? "border-brass bg-brass-soft"
                    : "border-line bg-paper-raised"
                }`}
              >
                {c.character}
              </button>
            ))}
          </div>
        </>
      ) : (
        <Card className="flex flex-col items-center gap-3 py-6">
          <div className="flex w-full items-center justify-between">
            <button onClick={() => setActive(null)} className="text-sm text-ink-soft">
              ← Quay lại
            </button>
            <span className="font-display text-2xl font-bold">{active}</span>
            <span className="font-data text-xs text-ink-soft">{status}</span>
          </div>
          <p className="text-sm text-ink-soft">{wordInfo}</p>
          <div id="hanziTarget" className="rounded-xl border border-line bg-paper-raised" />
          <div className="flex gap-2">
            <Button variant="ghost" onClick={animate}>
              Xem cách viết
            </Button>
            <Button onClick={startQuiz}>Tự viết</Button>
          </div>
          {result && (
            <p className={`text-sm font-semibold ${result.mistakes === 0 ? "text-jade" : "text-brass"}`}>
              {result.mistakes === 0
                ? "🎉 Hoàn hảo! Không sai nét nào (+30 XP)"
                : `✅ Hoàn thành — sai ${result.mistakes} nét (+15 XP). Thử lại để đạt hoàn hảo!`}
            </p>
          )}
        </Card>
      )}
    </div>
  );
}
