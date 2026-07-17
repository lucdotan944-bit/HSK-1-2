"use client";

import { useEffect, useMemo, useState } from "react";
import { api, meaningsList, type Word } from "@/lib/api";
import { speak } from "@/lib/speech";
import LevelPicker from "@/components/LevelPicker";
import { Button } from "@/components/ui";
import { usePreferredLevel } from "@/lib/level";

const PAGE_SIZE = 150;

export default function WordsPage() {
  const [level, setLevel] = usePreferredLevel(1);
  const [words, setWords] = useState<Word[]>([]);
  const [search, setSearch] = useState("");
  const [visible, setVisible] = useState(PAGE_SIZE);
  const [loadError, setLoadError] = useState(false);

  useEffect(() => {
    let active = true;
    // eslint-disable-next-line react-hooks/set-state-in-effect -- reset error banner when level changes
    setLoadError(false);
    api.wordsByLevel(level).then(
      (d) => {
        if (active) setWords(d.words);
      },
      () => {
        if (active) setLoadError(true);
      }
    );
    setVisible(PAGE_SIZE);
    return () => {
      active = false;
    };
  }, [level]);

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return words;
    return words.filter(
      (w) =>
        w.simplified.includes(q) ||
        w.pinyin.toLowerCase().includes(q) ||
        meaningsList(w.meanings).join(", ").toLowerCase().includes(q)
    );
  }, [words, search]);

  const shown = filtered.slice(0, visible);

  return (
    <div className="space-y-5">
      <h1 className="font-display text-2xl font-bold">Danh sách từ vựng</h1>
      <LevelPicker level={level} onChange={setLevel} />
      {loadError && <p className="text-sm text-seal">Không tải được danh sách từ. Vui lòng thử lại.</p>}
      <div className="flex items-center justify-between gap-3">
        <input
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setVisible(PAGE_SIZE);
          }}
          placeholder="Tìm theo chữ Hán, pinyin, nghĩa..."
          className="w-full max-w-xs rounded-full border border-line bg-paper px-4 py-1.5 text-sm outline-none focus:border-jade"
        />
        <span className="shrink-0 font-data text-xs text-ink-soft">
          {filtered.length} từ
        </span>
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
            {shown.map((w) => (
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
      {visible < filtered.length && (
        <div className="flex justify-center">
          <Button variant="ghost" onClick={() => setVisible((v) => v + PAGE_SIZE)}>
            Xem thêm ({filtered.length - visible} từ còn lại)
          </Button>
        </div>
      )}
    </div>
  );
}
