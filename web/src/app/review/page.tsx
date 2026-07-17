"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, meaningsList, type Word } from "@/lib/api";
import { Card, Button, ProgressBar } from "@/components/ui";
import PronunciationButton from "@/components/PronunciationButton";
import { useBadgeToast } from "@/components/BadgeToast";
import { speak } from "@/lib/speech";
import { usePreferredLevel } from "@/lib/level";
import { formatDueCount } from "@/lib/hsk";

const GRADES = [
  { q: 0, icon: "😵", label: "Quên" },
  { q: 1, icon: "😓", label: "Khó" },
  { q: 3, icon: "🤔", label: "Hơi nhớ" },
  { q: 4, icon: "😊", label: "Dễ" },
  { q: 5, icon: "😎", label: "Hoàn hảo" },
];

export default function ReviewPage() {
  const { announce, toastNode } = useBadgeToast();
  const [level] = usePreferredLevel(2);
  const [due, setDue] = useState<number | null>(null);
  const [words, setWords] = useState<Word[] | null>(null);
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState(false);

  useEffect(() => {
    let active = true;
    api.stats().then(
      (s) => {
        if (!active) return;
        const cumulativeDue = s.by_level.filter((l) => l.level <= level).reduce((sum, l) => sum + l.due, 0);
        setDue(cumulativeDue);
      },
      () => {
        if (active) setError(true);
      }
    );
    return () => {
      active = false;
    };
  }, [level]);

  async function start() {
    try {
      const data = await api.reviewWords(level, 20);
      if (!data.words.length) {
        setDone(true);
        return;
      }
      setWords(data.words);
      setIndex(0);
      setFlipped(false);
      setDone(false);
      speak(data.words[0].simplified);
    } catch {
      setError(true);
    }
  }

  async function grade(quality: number) {
    if (!words) return;
    const w = words[index];
    try {
      const r = await api.submitReview(w.id, quality);
      announce(r.newly_earned_badges);
    } catch {
      setError(true);
      return;
    }
    const next = index + 1;
    if (next >= words.length) {
      setWords(null);
      setDone(true);
    } else {
      setIndex(next);
      setFlipped(false);
      speak(words[next].simplified);
    }
  }

  if (error) {
    return (
      <div className="mx-auto max-w-md space-y-4 text-center">
        <p className="font-display text-xl font-bold">Không tải được dữ liệu ôn tập</p>
        <p className="text-ink-soft">Có lỗi kết nối. Vui lòng thử lại.</p>
        <Button
          onClick={() => {
            setError(false);
            setWords(null);
            setDone(false);
          }}
        >
          Thử lại
        </Button>
      </div>
    );
  }

  if (!words && !done) {
    return (
      <div className="mx-auto max-w-md space-y-4 text-center">
        <h1 className="font-display text-2xl font-bold">Ôn tập theo Spaced Repetition</h1>
        <p className="font-data text-sm text-ink-soft">
          Đang ôn HSK {level} —{" "}
          <Link href="/" className="text-jade underline">
            đổi cấp ở Trang chủ
          </Link>
        </p>
        <p className="text-ink-soft">
          {due !== null ? `${formatDueCount(due)} từ (HSK ≤ ${level}) cần ôn hôm nay` : "Đang tải..."}
        </p>
        <Button onClick={start} disabled={due === 0}>
          Bắt đầu ôn tập
        </Button>
      </div>
    );
  }

  if (done) {
    return (
      <div className="mx-auto max-w-md space-y-4 text-center">
        {toastNode}
        <p className="text-5xl">🎉</p>
        <h1 className="font-display text-2xl font-bold">Hết từ cần ôn!</h1>
        <p className="text-ink-soft">Quay lại sau để ôn tiếp theo lịch trình spaced repetition.</p>
        <Link href="/">
          <Button variant="ghost">Về trang chủ</Button>
        </Link>
      </div>
    );
  }

  const w = words![index];
  const meanings = meaningsList(w.meanings);

  return (
    <div className="mx-auto max-w-md space-y-5">
      {toastNode}
      <ProgressBar value={(index / words!.length) * 100} />
      <p className="text-center font-data text-sm text-ink-soft">
        {index + 1}/{words!.length}
      </p>

      <Card
        onClick={() => setFlipped((f) => !f)}
        className="flex min-h-[280px] cursor-pointer flex-col items-center justify-center gap-2 py-10 text-center"
      >
        <span className="rounded-full bg-jade-soft px-2 py-0.5 font-data text-xs text-jade">HSK {w.hsk_level}</span>
        <p className="font-display text-7xl">{w.simplified}</p>
        <p className="font-data text-xl text-jade">{w.pinyin}</p>
        {flipped && (
          <div className="mt-2 space-y-2">
            <p className="text-lg font-medium">{meanings[0]}</p>
            {w.sino_viet && (
              <p className="rounded-full bg-brass-soft px-3 py-1 text-sm font-semibold text-brass">
                Hán-Việt: {w.sino_viet}
              </p>
            )}
            {w.sentence_cn && (
              <div className="border-t border-line pt-2 text-sm">
                <p>{w.sentence_cn}</p>
                <p className="text-ink-soft">{w.sentence_vi}</p>
              </div>
            )}
            {w.context_note && <p className="text-sm text-ink-soft">💡 {w.context_note}</p>}
          </div>
        )}
        {!flipped && <p className="text-sm text-ink-soft">Chạm để xem nghĩa</p>}
      </Card>

      <div className="flex justify-center" onClick={(e) => e.stopPropagation()}>
        <PronunciationButton targetText={w.simplified} wordId={w.id} />
      </div>

      {flipped ? (
        <div className="grid grid-cols-5 gap-1.5">
          {GRADES.map((g) => (
            <button
              key={g.q}
              onClick={() => grade(g.q)}
              className="flex flex-col items-center gap-1 rounded-xl border border-line bg-paper-raised py-2 text-xs hover:bg-paper"
            >
              <span className="text-xl">{g.icon}</span>
              {g.label}
            </button>
          ))}
        </div>
      ) : (
        <p className="text-center text-sm text-ink-soft">Nhớ được không? Chạm vào thẻ để lật.</p>
      )}
    </div>
  );
}
