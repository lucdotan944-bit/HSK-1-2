"use client";

import { useEffect, useState, use as usePromise, useCallback, useRef } from "react";
import Link from "next/link";
import { api, type ExamQuestion, type ExamSubmitResult } from "@/lib/api";
import { Card, Button, ProgressBar } from "@/components/ui";
import { useBadgeToast } from "@/components/BadgeToast";
import { speak } from "@/lib/speech";

type Stage = "intro" | "exam" | "submitting" | "result";

const SECTION_LABEL: Record<string, string> = {
  listening: "🎧 Nghe",
  reading: "📖 Đọc — Từ vựng",
  grammar: "✍️ Ngữ pháp — Điền từ",
};

function isCloze(q: ExamQuestion): q is Extract<ExamQuestion, { section: "grammar" }> {
  return q.section === "grammar";
}

function fmtTime(sec: number) {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export default function ExamRunnerPage({ params }: { params: Promise<{ level: string }> }) {
  const { level: levelParam } = usePromise(params);
  const level = Math.max(1, Math.min(9, parseInt(levelParam, 10) || 1));
  const { announce, toastNode } = useBadgeToast();

  const [stage, setStage] = useState<Stage>("intro");
  const [questions, setQuestions] = useState<ExamQuestion[]>([]);
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<{ section: string; correct: boolean }[]>([]);
  const [answered, setAnswered] = useState<string | null>(null);
  const [timeLeft, setTimeLeft] = useState(0);
  const [result, setResult] = useState<ExamSubmitResult | null>(null);
  const startedAt = useRef<number>(0);
  const submittedRef = useRef(false);

  const finish = useCallback(
    async (finalAnswers: { section: string; correct: boolean }[]) => {
      if (submittedRef.current) return;
      submittedRef.current = true;
      setStage("submitting");
      const duration = Math.round((Date.now() - startedAt.current) / 1000);
      const r = await api.examSubmit(level, finalAnswers, duration);
      announce(r.newly_earned_badges);
      setResult(r);
      setStage("result");
    },
    [level, announce]
  );

  useEffect(() => {
    if (stage !== "exam" || timeLeft <= 0) return;
    const t = setInterval(() => setTimeLeft((s) => s - 1), 1000);
    return () => clearInterval(t);
  }, [stage, timeLeft]);

  useEffect(() => {
    if (stage === "exam" && timeLeft === 0 && questions.length > 0) {
      finish(answers);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeLeft, stage]);

  async function start() {
    const data = await api.examStart(level);
    setQuestions(data.questions);
    setTimeLeft(data.time_limit_seconds);
    setIndex(0);
    setAnswers([]);
    setAnswered(null);
    submittedRef.current = false;
    startedAt.current = Date.now();
    setStage("exam");
    const q0 = data.questions[0];
    if (q0 && q0.section === "listening") speak(q0.simplified);
  }

  function answer(choice: string, q: ExamQuestion) {
    if (answered) return;
    setAnswered(choice);
    const correct = isCloze(q) ? choice === q.correct_word : choice === q.correct_meaning;
    const next = [...answers, { section: q.section, correct }];
    setAnswers(next);
    setTimeout(
      () => {
        const nextIndex = index + 1;
        if (nextIndex >= questions.length) {
          finish(next);
        } else {
          setIndex(nextIndex);
          setAnswered(null);
          const nq = questions[nextIndex];
          if (nq.section === "listening") speak(nq.simplified);
        }
      },
      correct ? 500 : 1100
    );
  }

  if (stage === "intro") {
    return (
      <div className="mx-auto max-w-md space-y-4 text-center">
        <h1 className="font-display text-2xl font-bold">Thi thử HSK {level}</h1>
        <Card className="space-y-2 text-left text-sm text-ink-soft">
          <p>Bài thi gồm 3 phần, trộn ngẫu nhiên:</p>
          <ul className="list-inside list-disc space-y-1">
            <li>🎧 Nghe — nghe từ và chọn nghĩa đúng</li>
            <li>📖 Đọc/Từ vựng — chọn nghĩa đúng của chữ Hán</li>
            <li>✍️ Ngữ pháp — điền từ còn thiếu vào câu</li>
          </ul>
          <p>Đạt từ 60% câu đúng trở lên là Đạt bài thi.</p>
        </Card>
        <Button onClick={start}>Bắt đầu thi</Button>
        <div>
          <Link href="/exam" className="text-sm text-ink-soft underline">
            ← Chọn cấp khác
          </Link>
        </div>
      </div>
    );
  }

  if (stage === "submitting") {
    return <p className="text-center text-ink-soft">Đang chấm điểm...</p>;
  }

  if (stage === "result" && result) {
    return (
      <div className="mx-auto max-w-md space-y-4 text-center">
        {toastNode}
        <p className="text-5xl">{result.passed ? "🎉" : "💪"}</p>
        <h1 className="font-display text-2xl font-bold">{result.passed ? "Đạt!" : "Chưa đạt"}</h1>
        <p className="text-ink-soft">
          Bạn đúng {result.correct_count}/{result.total_questions} câu —{" "}
          <b className={result.passed ? "text-jade" : "text-seal"}>{result.score_pct}%</b>
        </p>
        <div className="grid gap-2 text-left">
          {Object.entries(result.section_scores).map(([section, s]) => (
            <Card key={section} className="flex items-center justify-between py-2.5">
              <span className="text-sm font-medium">{SECTION_LABEL[section] ?? section}</span>
              <span className="font-data text-sm text-ink-soft">
                {s.correct}/{s.total} ({s.pct ?? 0}%)
              </span>
            </Card>
          ))}
        </div>
        <div className="flex justify-center gap-2">
          <Link href="/exam">
            <Button variant="ghost">Chọn cấp khác</Button>
          </Link>
          <Button onClick={start}>Thi lại</Button>
        </div>
      </div>
    );
  }

  const q = questions[index];
  if (!q) return null;

  return (
    <div className="mx-auto max-w-md space-y-5">
      <div className="flex items-center justify-between">
        <ProgressBar value={(index / questions.length) * 100} />
      </div>
      <div className="flex items-center justify-between font-data text-sm text-ink-soft">
        <span>
          {index + 1}/{questions.length}
        </span>
        <span className={timeLeft < 60 ? "font-bold text-seal" : ""}>⏱ {fmtTime(timeLeft)}</span>
      </div>

      <p className="text-center text-xs font-semibold uppercase tracking-wide text-jade">
        {SECTION_LABEL[q.section] ?? q.section}
      </p>

      {isCloze(q) ? (
        <Card className="flex flex-col items-center gap-2 py-8 text-center">
          <p className="font-display text-2xl leading-relaxed">{q.sentence_blanked}</p>
          <p className="text-sm text-ink-soft">{q.sentence_vi}</p>
        </Card>
      ) : q.section === "listening" ? (
        <Card className="flex flex-col items-center gap-3 py-8 text-center">
          <button
            onClick={() => speak(q.simplified)}
            className="flex h-16 w-16 items-center justify-center rounded-full bg-jade-soft text-3xl hover:opacity-80"
            aria-label="Nghe lại"
          >
            🔊
          </button>
          <p className="text-sm text-ink-soft">Nghe và chọn nghĩa đúng</p>
        </Card>
      ) : (
        <Card className="flex flex-col items-center gap-2 py-8 text-center">
          <p className="font-display text-6xl">{q.simplified}</p>
          <p className="font-data text-lg text-jade">{q.pinyin}</p>
        </Card>
      )}

      <div className="grid gap-2">
        {q.choices.map((choice) => {
          const correctChoice = isCloze(q) ? q.correct_word : q.correct_meaning;
          const isCorrect = choice === correctChoice;
          const show = answered !== null;
          return (
            <button
              key={choice}
              onClick={() => answer(choice, q)}
              disabled={!!answered}
              className={`rounded-xl border px-4 py-3 text-left font-medium ${
                isCloze(q) ? "font-display text-xl" : ""
              } ${
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
