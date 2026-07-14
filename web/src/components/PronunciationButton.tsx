"use client";

import { useState } from "react";
import { getSpeechRecognition, scorePronunciation, describeSpeechError, listenOnce, SpeechRecognitionError } from "@/lib/speech";
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

  async function start() {
    setListening(true);
    setResult(null);
    try {
      const recognized = await listenOnce("zh-CN");
      const score = scorePronunciation(targetText, recognized);
      setResult({ score, text: recognized });
      api.logPronunciation({ word_id: wordId, target_text: targetText, recognized_text: recognized, score }).catch(() => {});
    } catch (e) {
      const code = e instanceof SpeechRecognitionError ? e.code : "unknown";
      setResult({ score: "warn", text: describeSpeechError(code) });
    } finally {
      setListening(false);
    }
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
