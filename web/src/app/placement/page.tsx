"use client";

import { useState } from "react";
import Link from "next/link";
import { api, type PlacementQuestion, type PlacementResult, type PlacementSection } from "@/lib/api";
import { Card, Button, ProgressBar } from "@/components/ui";
import { useBadgeToast } from "@/components/BadgeToast";
import {
  speak,
  listenOnce,
  scorePronunciation,
  describeSpeechError,
  getSpeechRecognition,
  SpeechRecognitionError,
} from "@/lib/speech";

type Stage = "intro" | "quiz" | "done" | "error";
type Answer = { word_id: number; hsk_level: number; correct: boolean; section: PlacementSection };

const SECTION_META: Record<PlacementSection, { icon: string; label: string; hint: string }> = {
  vocab: { icon: "📖", label: "Từ vựng", hint: "Chọn nghĩa tiếng Việt đúng cho từ." },
  listening: { icon: "🎧", label: "Nghe hiểu", hint: "Nghe audio (không nhìn chữ) rồi chọn nghĩa đúng. Bấm loa để nghe lại." },
  reading: { icon: "📚", label: "Đọc hiểu", hint: "Chọn từ đúng để điền vào chỗ trống trong câu." },
  speaking: { icon: "🎤", label: "Nói", hint: "Bấm micro và đọc to từ trên màn hình. Không có mic? Bấm Bỏ qua." },
};

export default function PlacementPage() {
  const { announce, toastNode } = useBadgeToast();
  const [stage, setStage] = useState<Stage>("intro");
  const [questions, setQuestions] = useState<PlacementQuestion[]>([]);
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [answered, setAnswered] = useState<string | null>(null);
  const [listening, setListening] = useState(false);
  const [speakResult, setSpeakResult] = useState<{ score: string; text: string } | null>(null);
  const [resultData, setResultData] = useState<PlacementResult | null>(null);
  const micSupported = typeof window !== "undefined" && !!getSpeechRecognition();

  async function start() {
    try {
      const data = await api.placementQuestions();
      setQuestions(data.questions);
      setIndex(0);
      setAnswers([]);
      setAnswered(null);
      setSpeakResult(null);
      setStage("quiz");
      const q = data.questions[0];
      if (q && q.section !== "reading") speak(q.simplified);
    } catch {
      setStage("error");
    }
  }

  function goNext(nextAnswers: Answer[]) {
    const nextIndex = index + 1;
    if (nextIndex >= questions.length) {
      finish(nextAnswers);
      return;
    }
    setIndex(nextIndex);
    setAnswered(null);
    setSpeakResult(null);
    const q = questions[nextIndex];
    // Listening plays its audio; vocab hears the word too. Reading stays
    // silent (the sentence would give the blank away), speaking waits for the mic.
    if (q.section === "vocab" || q.section === "listening") speak(q.simplified);
  }

  function answerChoice(choice: string, q: PlacementQuestion) {
    if (answered) return;
    setAnswered(choice);
    const correctValue = q.section === "reading" ? q.correct_word : q.correct_meaning;
    const correct = choice === correctValue;
    const next = [...answers, { word_id: q.word_id, hsk_level: q.hsk_level, correct, section: q.section }];
    setAnswers(next);
    setTimeout(() => goNext(next), correct ? 600 : 1500);
  }

  async function recordSpeaking(q: PlacementQuestion) {
    setListening(true);
    setSpeakResult(null);
    try {
      const recognized = await listenOnce("zh-CN");
      const score = scorePronunciation(q.simplified, recognized);
      setSpeakResult({ score, text: recognized });
      api.logPronunciation({ word_id: q.word_id, target_text: q.simplified, recognized_text: recognized, score }).catch(() => {});
      const next = [...answers, { word_id: q.word_id, hsk_level: q.hsk_level, correct: score !== "fail", section: q.section }];
      setAnswers(next);
      setTimeout(() => goNext(next), 1400);
    } catch (e) {
      const code = e instanceof SpeechRecognitionError ? e.code : "unknown";
      setSpeakResult({ score: "error", text: describeSpeechError(code) });
    } finally {
      setListening(false);
    }
  }

  function skipSpeaking() {
    // Skipped speaking questions are simply not submitted, so they don't
    // drag the level ladder or the speaking score down.
    goNext(answers);
  }

  async function finish(finalAnswers: Answer[]) {
    try {
      const r = await api.submitPlacement(finalAnswers);
      announce(r.newly_earned_badges);
      setResultData(r);
      setStage("done");
    } catch {
      setStage("error");
    }
  }

  if (stage === "error") {
    return (
      <div className="mx-auto max-w-md space-y-4 text-center">
        <p className="font-display text-xl font-bold">Có lỗi xảy ra</p>
        <p className="text-ink-soft">Không thể tải hoặc nộp bài test. Vui lòng thử lại.</p>
        <div className="flex justify-center gap-2">
          <Link href="/">
            <Button variant="ghost">Về trang chủ</Button>
          </Link>
          <Button onClick={start}>Thử lại</Button>
        </div>
      </div>
    );
  }

  if (stage === "intro") {
    return (
      <div className="mx-auto max-w-md space-y-4 text-center">
        <h1 className="font-display text-2xl font-bold">Test xếp trình độ</h1>
        <p className="text-ink-soft">
          Bài test đánh giá đủ 4 kỹ năng trên thang HSK 1-9, khoảng 10 phút:
        </p>
        <div className="grid grid-cols-2 gap-2 text-left text-sm">
          {(Object.keys(SECTION_META) as PlacementSection[]).map((s) => (
            <div key={s} className="rounded-xl border border-line bg-paper-raised px-3 py-2">
              <p className="font-semibold">
                {SECTION_META[s].icon} {SECTION_META[s].label}
              </p>
              <p className="text-xs text-ink-soft">{SECTION_META[s].hint}</p>
            </div>
          ))}
        </div>
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
    const meta = SECTION_META[q.section];
    const isNewSection = index === 0 || questions[index - 1].section !== q.section;
    return (
      <div className="mx-auto max-w-md space-y-5">
        <ProgressBar value={(index / questions.length) * 100} />
        <div className="flex items-center justify-between">
          <span className="rounded-full bg-jade-soft px-3 py-1 font-data text-xs font-semibold text-jade">
            {meta.icon} {meta.label}
          </span>
          <span className="font-data text-sm text-ink-soft">
            {index + 1}/{questions.length}
          </span>
        </div>
        {isNewSection && <p className="text-center text-sm text-ink-soft">{meta.hint}</p>}

        {q.section === "listening" ? (
          <Card className="flex flex-col items-center gap-3 py-8 text-center">
            <button
              onClick={() => speak(q.simplified)}
              aria-label="Nghe lại"
              className="flex h-16 w-16 items-center justify-center rounded-full border border-line bg-paper-raised text-3xl hover:bg-paper"
            >
              🔊
            </button>
            {answered ? (
              <>
                <p className="font-display text-4xl">{q.simplified}</p>
                <p className="font-data text-lg text-jade">{q.pinyin}</p>
              </>
            ) : (
              <p className="text-sm text-ink-soft">Nghe rồi chọn nghĩa đúng</p>
            )}
          </Card>
        ) : q.section === "reading" ? (
          <Card className="flex flex-col items-center gap-2 py-8 text-center">
            <p className="font-display text-2xl leading-relaxed">{q.sentence_blanked}</p>
            {answered && q.sentence_vi && <p className="text-sm text-ink-soft">{q.sentence_vi}</p>}
          </Card>
        ) : (
          <Card className="flex flex-col items-center gap-2 py-8 text-center">
            <p className="font-display text-6xl">{q.simplified}</p>
            <p className="font-data text-lg text-jade">{q.pinyin}</p>
            {q.section === "speaking" && <p className="text-ink-soft">{q.correct_meaning}</p>}
          </Card>
        )}

        {q.section === "speaking" ? (
          <div className="flex flex-col items-center gap-3">
            {micSupported ? (
              <button
                onClick={() => recordSpeaking(q)}
                disabled={listening}
                aria-label="Bấm để nói"
                className={`flex h-16 w-16 items-center justify-center rounded-full border border-line text-3xl transition-colors ${
                  listening ? "animate-pulse bg-seal-soft" : "bg-paper-raised hover:bg-paper"
                }`}
              >
                🎤
              </button>
            ) : (
              <p className="text-sm text-ink-soft">Trình duyệt này không hỗ trợ nhận diện giọng nói.</p>
            )}
            {speakResult && (
              <p className="text-center text-sm text-ink-soft">
                {speakResult.score === "ok" ? "✅" : speakResult.score === "warn" ? "⚠️" : speakResult.score === "fail" ? "❌" : ""}{" "}
                {speakResult.text}
              </p>
            )}
            <Button variant="ghost" onClick={skipSpeaking} disabled={listening}>
              Bỏ qua câu này
            </Button>
          </div>
        ) : (
          <div className="grid gap-2">
            {q.choices.map((choice) => {
              const correctValue = q.section === "reading" ? q.correct_word : q.correct_meaning;
              const isCorrect = choice === correctValue;
              const show = answered !== null;
              return (
                <button
                  key={choice}
                  onClick={() => answerChoice(choice, q)}
                  disabled={!!answered}
                  className={`rounded-xl border px-4 py-3 text-left font-medium ${
                    q.section === "reading" ? "text-center font-display text-xl" : ""
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
        )}
      </div>
    );
  }

  const skillOrder: PlacementSection[] = ["vocab", "listening", "reading", "speaking"];
  return (
    <div className="mx-auto max-w-md space-y-5 text-center">
      {toastNode}
      <p className="text-5xl">🎉</p>
      <h1 className="font-display text-2xl font-bold">Hoàn thành!</h1>
      <p className="text-ink-soft">
        Bạn đúng {Math.round((resultData?.accuracy ?? 0) * 100)}% — gợi ý bắt đầu ở{" "}
        <b className="text-seal">HSK {resultData?.recommended_level}</b>.
      </p>
      {resultData?.skills && (
        <Card className="space-y-2 text-left">
          <p className="font-semibold">Kết quả theo kỹ năng</p>
          {skillOrder
            .filter((s) => resultData.skills[s])
            .map((s) => {
              const sk = resultData.skills[s];
              return (
                <div key={s} className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <span>
                      {SECTION_META[s].icon} {SECTION_META[s].label}
                    </span>
                    <span className="font-data text-ink-soft">
                      {sk.correct}/{sk.total} · {sk.pct}%
                    </span>
                  </div>
                  <ProgressBar value={sk.pct} />
                </div>
              );
            })}
        </Card>
      )}
      <Link href="/">
        <Button>Về trang chủ</Button>
      </Link>
    </div>
  );
}
