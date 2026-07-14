"use client";

import { useEffect, useState } from "react";
import { api, meaningsList, type Word } from "@/lib/api";
import { speak } from "@/lib/speech";

export default function WordsPage() {
  const [level, setLevel] = useState(1);
  const [words, setWords] = useState<Word[]>([]);

  useEffect(() => {
    api.wordsByLevel(level).then((d) => setWords(d.words));
  }, [level]);

  return (
    <div className="space-y-5">
      <h1 className="font-display text-2xl font-bold">Danh sách từ vựng</h1>
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
      <div className="overflow-x-auto rounded-2xl border border-line">
        <table className="w-full text-sm">
          <thead className="bg-paper-raised text-left text-ink-soft">
            <tr>
              <th className="px-3 py-2">Hán tự</th>
              <th className="px-3 py-2">Pinyin</th>
              <th className="px-3 py-2">Nghĩa</th>
              <th className="px-3 py-2">Hán-Việt</th>
            </tr>
          </thead>
          <tbody>
            {words.map((w) => (
              <tr key={w.id} onClick={() => speak(w.simplified)} className="cursor-pointer border-t border-line hover:bg-paper-raised">
                <td className="font-display px-3 py-2 text-xl">{w.simplified}</td>
                <td className="font-data px-3 py-2 text-jade">{w.pinyin}</td>
                <td className="px-3 py-2">{meaningsList(w.meanings).join(", ")}</td>
                <td className="px-3 py-2 text-brass">{w.sino_viet || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
