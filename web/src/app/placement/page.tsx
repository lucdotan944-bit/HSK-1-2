"use client";

import { useState } from "react";
import Link from "next/link";
import { api, type QuizChoice } from "@/lib/api";
import { Card, Button, ProgressBar } from "@/components/ui";
import { useBadgeToast } from "@/components/BadgeToast";
import { speak } from "@/lib/speech";

type Stage = "intro" | "quiz" | "done";

export default function PlacementPage() {
  const { announce, toastNode } = useBadgeToast();
  const [stage, setStage] = useState<Stage>("intro");
  const [questions, setQuestions] = useState<QuizChoice[]>([]);
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<{ word_id: number; hsk_level: number; correct: boolean }[]>([]);
  const [answered, setAnswered] = useState<string | null>(null);
  const [resultData, setResultData] = useState<{ recommended_level: number; accuracy: number } | null>(null);
  const [mapDesc, setMapDesc] = useState<string>("");

  async function start() {
    const data = await api.placementQuestions(15);
    setQuestions(data.questions);
    setIndex(0);
    setAnswers([]);
    setAnswered(null);
    setStage("quiz");
    if (data.questions[0]) speak(data.questions[0].simplified);
  }

  function answer(choice: string, q: QuizChoice) {
    if (answered) return;
    setAnswered(choice);
    const correct = choice === q.correct_meaning;
    const next = [...answers, { word_id: q.word_id, hsk_level: q.hsk_level, correct }];
    setAnswers(next);
    setTimeout(
      () => {
        const nextIndex = index + 1;
        if (nextIndex >= questions.length) {
          finish(next);
        } else {
          setIndex(nextIndex);
          setAnswered(null);
          speak(questions[nextIndex].simplified);
        }
      },
      correct ? 600 : 1300
    );
  }

  async function finish(finalAnswers: typeof answers) {
    const r = await api.submitPlacement(finalAnswers);
    announce(r.newly_earned_badges);
    setResultData(r);
    const mapping = await api.hskMapping();
    const row = mapping.mapping.find((m) => m.old === r.recommended_level);
    setMapDesc(row?.desc ?? "");
    setStage("done");
  }

  if (stage === "intro") {
    return (
      <div className="mx-auto max-w-md space-y-4 text-center">
        <h1 className="font-display text-2xl font-bold">Test xếp trình độ</h1>
        <p className="text-ink-soft">
          15 câu, khoảng 5 phút. Chọn nghĩa đúng cho mỗi từ — hệ thống sẽ gợi ý điểm bắt đầu HSK1 hoặc HSK2 phù hợp.
        </p>
        <div className="flex justify-center gap-2">
          <Link href="/mic-check?next=/placement">
            <Button variant="ghost">🎤 Kiểm tra mic trước</Button>
          </Link>
          <Button onClick={start}>Bắt đầu</Button>
        </div>
      </div>
    );
  }

  if (stage === "quiz") {
    const q = questions[index];
    if (!q) return null;
    return (
      <div className="mx-auto max-w-md space-y-5">
        <ProgressBar value={(index / questions.length) * 100} />
        <p className="text-center font-data text-sm text-ink-soft">
          {index + 1}/{questions.length}
        </p>
        <Card className="flex flex-col items-center gap-2 py-8 text-center">
          <p className="font-display text-6xl">{q.simplified}</p>
          <p className="font-data text-lg text-jade">{q.pinyin}</p>
        </Card>
        <div className="grid gap-2">
          {q.choices.map((choice) => {
            const isCorrect = choice === q.correct_meaning;
            const show = answered !== null;
            return (
              <button
                key={choice}
                onClick={() => answer(choice, q)}
                disabled={!!answered}
                className={`rounded-xl border px-4 py-3 text-left font-medium ${
                  show && isCorrect
                    ? "border-jade bg-jade-soft"
                    : show && choice === answered
                    ? "border-seal bg-seal-soft"
                    : "border-line bg-paper-raised"
                }`}
              >
                {choice}
              </button>
            );
          })}
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-md space-y-4 text-center">
      {toastNode}
      <p className="text-5xl">🎉</p>
      <h1 className="font-display text-2xl font-bold">Hoàn thành!</h1>
      <p className="text-ink-soft">
        Bạn đúng {Math.round((resultData?.accuracy ?? 0) * 100)}% — gợi ý bắt đầu ở{" "}
        <b className="text-seal">HSK {resultData?.recommended_level}</b>.
      </p>
      {mapDesc && <p className="text-sm text-ink-soft">{mapDesc}</p>}
      <Link href="/">
        <Button>Về trang chủ</Button>
      </Link>
    </div>
  );
}
