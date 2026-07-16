"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, meaningsList, type DailySession } from "@/lib/api";
import { Card, Button, SectionTitle } from "@/components/ui";
import PronunciationButton from "@/components/PronunciationButton";
import { useBadgeToast } from "@/components/BadgeToast";
import { speak } from "@/lib/speech";
import { usePreferredLevel } from "@/lib/level";

function LevelBadge({ level }: { level: number }) {
  return (
    <span className="rounded-full bg-jade-soft px-2 py-0.5 font-data text-xs text-jade">HSK {level}</span>
  );
}

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

  const reviewWords = session?.blocks.review ?? [];
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
      <SectionTitle sub="4 khối: ôn từ · nghe · nói · hội thoại — khoảng 5 phút, giới hạn theo cấp HSK bạn chọn">
        Phiên học hôm nay
      </SectionTitle>

      <p className="font-data text-sm text-ink-soft">
        Đang ôn HSK {level} —{" "}
        <Link href="/" className="text-jade underline">
          đổi cấp ở Trang chủ
        </Link>
      </p>

      {!session ? (
        <p className="text-ink-soft">Đang soạn phiên học cho bạn...</p>
      ) : (
        <>
          {session.focus_skill && (
            <p className="rounded-full bg-seal-soft px-4 py-2 text-center text-sm text-seal">
              Hôm nay tập trung vào kỹ năng:{" "}
              <b>{session.skills[session.focus_skill as keyof typeof session.skills].label}</b>
            </p>
          )}

          <Card>
            <div className="mb-3 flex items-center justify-between">
              <p className="font-semibold">1. Ôn từ (spaced repetition)</p>
              {reviewWords.length > 0 && !reviewDone && <LevelBadge level={reviewWords[reviewIndex].hsk_level} />}
            </div>
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
            <div className="mb-3 flex items-center justify-between">
              <p className="font-semibold">2. Nghe hiểu</p>
              {session.blocks.listening && <LevelBadge level={session.blocks.listening.hsk_level} />}
            </div>
            {session.blocks.listening ? (
              <div className="flex flex-col items-center gap-2 text-center">
                <button
                  onClick={() => speak(session.blocks.listening!.simplified)}
                  className="rounded-full bg-jade-soft px-5 py-2 font-semibold text-jade"
                >
                  🔊 Nghe câu
                </button>
                {listeningRevealed ? (
                  <>
                    <p className="text-lg">{session.blocks.listening.simplified}</p>
                    <p className="font-data text-jade">{session.blocks.listening.pinyin}</p>
                    <p className="text-ink-soft">{session.blocks.listening.vietnamese}</p>
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
            <div className="mb-3 flex items-center justify-between">
              <p className="font-semibold">3. Luyện nói</p>
              {session.blocks.speaking && <LevelBadge level={session.blocks.speaking.hsk_level} />}
            </div>
            {session.blocks.speaking ? (
              <div className="flex flex-col items-center gap-2 text-center">
                <p className="font-display text-5xl">{session.blocks.speaking.simplified}</p>
                <p className="font-data text-jade">{session.blocks.speaking.pinyin}</p>
                <p>{meaningsList(session.blocks.speaking.meanings)[0]}</p>
                <PronunciationButton targetText={session.blocks.speaking.simplified} wordId={session.blocks.speaking.id} />
              </div>
            ) : (
              <p className="text-sm text-ink-soft">Không có dữ liệu.</p>
            )}
          </Card>

          <Card>
            <div className="mb-3 flex items-center justify-between">
              <p className="font-semibold">4. Hội thoại ngắn</p>
              {session.blocks.conversation_hsk_level != null && <LevelBadge level={session.blocks.conversation_hsk_level} />}
            </div>
            {session.blocks.conversation_scenario_id ? (
              <Link href={`/conversation/${session.blocks.conversation_scenario_id}`}>
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
        </>
      )}
    </div>
  );
}
