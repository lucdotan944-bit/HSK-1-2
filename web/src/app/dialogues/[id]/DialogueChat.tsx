"use client";

import type { DialogueLine } from "@/lib/api";
import { speak } from "@/lib/speech";

export default function DialogueChat({ lines }: { lines: DialogueLine[] }) {
  return (
    <div className="space-y-3">
      {lines.map((l, i) => {
        const isA = i % 2 === 0;
        return (
          <div key={l.id} className={`flex ${isA ? "justify-start" : "justify-end"}`}>
            <button
              onClick={() => speak(l.simplified)}
              className={`max-w-[85%] rounded-2xl border px-4 py-2.5 text-left ${
                isA ? "border-line bg-paper-raised" : "border-jade/40 bg-jade-soft"
              }`}
            >
              <p className="text-xs font-semibold text-ink-soft">{l.speaker}</p>
              <p className="text-lg">{l.simplified}</p>
              <p className="font-data text-sm text-jade">{l.pinyin}</p>
              <p className="text-sm text-ink-soft">{l.vietnamese}</p>
            </button>
          </div>
        );
      })}
    </div>
  );
}
