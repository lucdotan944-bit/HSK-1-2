"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, meaningsList, type DailySession } from "@/lib/api";
import { Card, Button, SectionTitle } from "@/components/ui";
import PronunciationButton from "@/components/PronunciationButton";
import { useBadgeToast } from "@/components/BadgeToast";
import { speak } from "@/lib/speech";
import { usePreferredLevel } from "@/lib/level";

const GRADES = [
  { q: 0, icon: "😵" },
  { q: 3, icon: "🤔" },
  { q: 5, icon: "😎" },
];

export default function DailySessionPage() {
  const { announce, toastNode } = useBadgeToast();
  const [level] = usePreferredLevel(1);
  const [session, setSession] = useState<DailySession | null>(null);
  const [reviewIndex, setReviewIndex] = useState(0);
  const [reviewDone, setReviewDone] = useState(false);
  const [listeningRevealed, setListeningRevealed] = useState(false);
  const [listeningDone, setListeningDone] = useState(false);

  useEffect(() => {
    let active = true;
    api.dailySession(level).then((d) => {
      if (active) setSession(d);
    });
    return () => {
      active = false;
    };
  }, [level]);

  if (!session) return <p className="text-ink-soft">Đang soạn phiên học cho bạn...</p>;

  const { blocks } = session;
  const reviewWords = blocks.review;
  const allDone = reviewDone && listeningDone;

  async function gradeReview(q: number) {
    const w = reviewWords[reviewIndex];
    const r = await api.submitReview(w.id, q);
    announce(r.newly_earned_badges);
    if (reviewIndex + 1 >= reviewWords.length) setReviewDone(true);
    else setReviewIndex((i) => i + 1);
  }

  return (
    <div className="mx-auto max-w-lg space-y-6">
      {toastNode}
      <SectionTitle sub="4 khối: ôn từ · nghe · nói · hội thoại — khoảng 5 phút">Phiên học hôm nay</SectionTitle>

      {session.focus_skill && (
        <p className="rounded-full bg-seal-soft px-4 py-2 text-center text-sm text-seal">
          Hôm nay tập trung vào kỹ năng: <b>{session.skills[session.focus_skill as keyof typeof session.skills].label}</b>
        </p>
      )}

      <Card>
        <p className="mb-3 font-semibold">1. Ôn từ (spaced repetition)</p>
        {reviewWords.length === 0 || reviewDone ? (
          <p className="text-sm text-jade">✅ Xong — không còn từ cần ôn ngay bây giờ.</p>
        ) : (
          <div className="flex flex-col items-center gap-3 text-center">
            <button onClick={() => speak(reviewWords[reviewIndex].simplified)} className="font-display text-5xl">
              {reviewWords[reviewIndex].simplified}
            </button>
            <p className="font-data text-jade">{reviewWords[reviewIndex].pinyin}</p>
            <p>{meaningsList(reviewWords[reviewIndex].meanings)[0]}</p>
            <div className="flex gap-2">
              {GRADES.map((g) => (
                <button
                  key={g.q}
                  onClick={() => gradeReview(g.q)}
                  className="rounded-full border border-line px-4 py-2 text-lg hover:bg-paper"
                >
                  {g.icon}
                </button>
              ))}
            </div>
            <p className="font-data text-xs text-ink-soft">
              {reviewIndex + 1}/{reviewWords.length}
            </p>
          </div>
        )}
      </Card>

      <Card>
        <p className="mb-3 font-semibold">2. Nghe hiểu</p>
        {blocks.listening ? (
          <div className="flex flex-col items-center gap-2 text-center">
            <button
              onClick={() => speak(blocks.listening!.simplified)}
              className="rounded-full bg-jade-soft px-5 py-2 font-semibold text-jade"
            >
              🔊 Nghe câu
            </button>
            {listeningRevealed ? (
              <>
                <p className="text-lg">{blocks.listening.simplified}</p>
                <p className="font-data text-jade">{blocks.listening.pinyin}</p>
                <p className="text-ink-soft">{blocks.listening.vietnamese}</p>
                {!listeningDone && (
                  <Button variant="secondary" onClick={() => setListeningDone(true)}>
                    Đã hiểu, tiếp tục
                  </Button>
                )}
                {listeningDone && <p className="text-sm text-jade">✅ Xong</p>}
              </>
            ) : (
              <Button variant="ghost" onClick={() => setListeningRevealed(true)}>
                Xem nghĩa
              </Button>
            )}
          </div>
        ) : (
          <p className="text-sm text-ink-soft">Không có dữ liệu.</p>
        )}
      </Card>

      <Card>
        <p className="mb-3 font-semibold">3. Luyện nói</p>
        {blocks.speaking ? (
          <div className="flex flex-col items-center gap-2 text-center">
            <p className="font-display text-5xl">{blocks.speaking.simplified}</p>
            <p className="font-data text-jade">{blocks.speaking.pinyin}</p>
            <p>{meaningsList(blocks.speaking.meanings)[0]}</p>
            <PronunciationButton targetText={blocks.speaking.simplified} wordId={blocks.speaking.id} />
          </div>
        ) : (
          <p className="text-sm text-ink-soft">Không có dữ liệu.</p>
        )}
      </Card>

      <Card>
        <p className="mb-3 font-semibold">4. Hội thoại ngắn</p>
        {blocks.conversation_scenario_id ? (
          <Link href={`/conversation/${blocks.conversation_scenario_id}`}>
            <Button variant="secondary">Bắt đầu hội thoại</Button>
          </Link>
        ) : (
          <p className="text-sm text-ink-soft">Không có kịch bản.</p>
        )}
      </Card>

      {allDone && (
        <div className="text-center">
          <p className="mb-2 font-display text-xl font-bold text-jade">🎉 Hoàn thành phiên học hôm nay!</p>
          <Link href="/">
            <Button>Về trang chủ</Button>
          </Link>
        </div>
      )}
    </div>
  );
}
