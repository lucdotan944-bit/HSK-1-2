"use client";

import { useState } from "react";
import { getSpeechRecognition, scorePronunciation } from "@/lib/speech";
import { api } from "@/lib/api";

const ICONS: Record<string, string> = { ok: "✅", warn: "⚠️", fail: "❌" };

export default function PronunciationButton({
  targetText,
  wordId,
}: {
  targetText: string;
  wordId?: number;
}) {
  const [listening, setListening] = useState(false);
  const [result, setResult] = useState<{ score: string; text: string } | null>(null);
  const supported = typeof window !== "undefined" && !!getSpeechRecognition();

  function start() {
    const Rec = getSpeechRecognition();
    if (!Rec) return;
    const rec = new Rec();
    rec.lang = "zh-CN";
    rec.interimResults = false;
    rec.maxAlternatives = 1;
    setListening(true);
    setResult(null);

    rec.onresult = (e) => {
      const recognized = e.results[0][0].transcript;
      const score = scorePronunciation(targetText, recognized);
      setResult({ score, text: recognized });
      api.logPronunciation({ word_id: wordId, target_text: targetText, recognized_text: recognized, score }).catch(() => {});
    };
    rec.onerror = (e) => {
      setResult({ score: "warn", text: e.error === "no-speech" ? "Không nghe thấy gì, thử lại" : "Lỗi micro" });
    };
    rec.onend = () => setListening(false);
    rec.start();
  }

  if (!supported) return null;

  return (
    <div className="flex flex-col items-center gap-1.5">
      <button
        onClick={start}
        aria-label="Luyện nói"
        className={`flex h-11 w-11 items-center justify-center rounded-full border border-line text-lg transition-colors ${
          listening ? "animate-pulse bg-seal-soft" : "bg-paper-raised hover:bg-paper"
        }`}
      >
        🎤
      </button>
      {result && (
        <p className="text-center text-xs text-ink-soft">
          {ICONS[result.score] ?? ""} {result.text}
        </p>
      )}
    </div>
  );
}
