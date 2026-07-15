"use client";

import { useEffect, useState, use as usePromise } from "react";
import Link from "next/link";
import { api, meaningsList, type Word, type QuizChoice, type DialogueSummary } from "@/lib/api";
import { Card, Button } from "@/components/ui";
import PronunciationButton from "@/components/PronunciationButton";
import { useBadgeToast } from "@/components/BadgeToast";
import { speak } from "@/lib/speech";

type Stage = "loading" | "words" | "quiz" | "done";

export default function LessonPage({ params }: { params: Promise<{ themeId: string }> }) {
  const { themeId } = usePromise(params);
  const { announce, toastNode } = useBadgeToast();

  const [themeName, setThemeName] = useState("");
  const [stage, setStage] = useState<Stage>("loading");
  const [words, setWords] = useState<Word[]>([]);
  const [wordIndex, setWordIndex] = useState(0);

  const [quiz, setQuiz] = useState<QuizChoice[]>([]);
  const [quizIndex, setQuizIndex] = useState(0);
  const [quizResults, setQuizResults] = useState<{ word_id: number; correct: boolean }[]>([]);
  const [answered, setAnswered] = useState<string | null>(null);

  const [quizScore, setQuizScore] = useState<{ correct: number; total: number } | null>(null);
  const [related, setRelated] = useState<DialogueSummary[]>([]);

  useEffect(() => {
    api.theme(themeId).then((data) => {
      setThemeName(data.theme.name);
      setWords(data.words);
      setStage("words");
    });
  }, [themeId]);

  useEffect(() => {
    if (stage === "words" && words.length && wordIndex < words.length) {
      const w = words[wordIndex];
      if (!w.repetitions) {
        api.learnThemeWord(themeId, w.id).then((r) => announce(r.newly_earned_badges));
      }
      speak(w.simplified);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [stage, wordIndex, words]);

  async function startQuiz() {
    setStage("quiz");
    const count = Math.min(5, words.length);
    const data = await api.quizChoices(2, { themeId, count });
    if (!data.questions.length) return finishLesson(null);
    setQuiz(data.questions);
    setQuizIndex(0);
    setQuizResults([]);
    setAnswered(null);
    speak(data.questions[0].simplified);
  }

  function answer(choice: string, q: QuizChoice) {
    if (answered) return;
    const correct = choice === q.correct_meaning;
    setAnswered(choice);
    const results = [...quizResults, { word_id: q.word_id, correct }];
    setQuizResults(results);
    setTimeout(
      () => {
        const next = quizIndex + 1;
        if (next >= quiz.length) {
          submitQuiz(results);
        } else {
          setQuizIndex(next);
          setAnswered(null);
          speak(quiz[next].simplified);
        }
      },
      correct ? 700 : 1500
    );
  }

  async function submitQuiz(results: { word_id: number; correct: boolean }[]) {
    const r = await api.submitThemeQuiz(themeId, results);
    announce(r.newly_earned_badges);
    finishLesson({ correct: results.filter((x) => x.correct).length, total: results.length });
  }

  async function finishLesson(score: { correct: number; total: number } | null) {
    setQuizScore(score);
    const r = await api.relatedDialogues(themeId);
    setRelated(r.dialogues);
    setStage("done");
  }

  if (stage === "loading") return <p className="text-ink-soft">Đang tải...</p>;

  if (stage === "words") {
    const w = words[wordIndex];
    if (!w) return null;
    const isLast = wordIndex >= words.length - 1;
    const meanings = meaningsList(w.meanings);
    return (
      <div className="mx-auto max-w-md space-y-5">
        {toastNode}
        <div className="flex items-center justify-between">
          <Link href="/" className="text-sm text-ink-soft">
            ← {themeName}
          </Link>
          <span className="font-data text-sm text-ink-soft">
            {wordIndex + 1}/{words.length}
          </span>
        </div>

        <Card className="flex flex-col items-center gap-3 py-10 text-center">
          <button onClick={() => speak(w.simplified)} className="font-display text-7xl">
            {w.simplified}
          </button>
          <p className="font-data text-xl text-jade">{w.pinyin}</p>
          <p className="text-lg font-medium">{meanings[0]}</p>
          {w.sino_viet && (
            <p className="rounded-full bg-brass-soft px-3 py-1 text-sm font-semibold text-brass">
              Hán-Việt: {w.sino_viet}
            </p>
          )}
          {w.sentence_cn && (
            <div className="mt-2 border-t border-line pt-3 text-sm">
              <p>{w.sentence_cn}</p>
              <p className="text-ink-soft">{w.sentence_vi}</p>
            </div>
          )}
          {w.context_note && <p className="text-sm text-ink-soft">💡 {w.context_note}</p>}
          <PronunciationButton targetText={w.simplified} wordId={w.id} />
        </Card>

        <div className="flex items-center justify-between gap-3">
          <Button variant="ghost" onClick={() => setWordIndex((i) => Math.max(0, i - 1))} disabled={wordIndex === 0}>
            ◀ Trước
          </Button>
          <div className="flex gap-1">
            {words.map((_, i) => (
              <span
                key={i}
                className={`h-1.5 w-1.5 rounded-full ${i <= wordIndex ? "bg-jade" : "bg-line"}`}
              />
            ))}
          </div>
          <Button onClick={() => (isLast ? startQuiz() : setWordIndex((i) => i + 1))}>
            {isLast ? "✅ Hoàn thành" : "Tiếp ▶"}
          </Button>
        </div>
      </div>
    );
  }

  if (stage === "quiz") {
    const q = quiz[quizIndex];
    if (!q) return null;
    return (
      <div className="mx-auto max-w-md space-y-5">
        <p className="text-center font-data text-sm text-ink-soft">
          Câu {quizIndex + 1}/{quiz.length}
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
                className={`rounded-xl border px-4 py-3 text-left font-medium transition-colors ${
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
    <div className="mx-auto max-w-md space-y-5 text-center">
      {toastNode}
      <p className="font-display text-3xl font-bold">🎉 Xong chủ đề {themeName}!</p>
      <p className="text-ink-soft">Bạn đã học {words.length} từ trong chủ đề này.</p>
      {quizScore && quizScore.total > 0 && (
        <p className="font-data font-semibold text-jade">
          Mini-quiz: {quizScore.correct}/{quizScore.total} câu đúng
        </p>
      )}
      {related.length > 0 && (
        <Card className="text-left">
          <p className="mb-2 font-semibold">Luyện tiếp với hội thoại liên quan:</p>
          <div className="space-y-2">
            {related.map((d) => (
              <Link key={d.id} href={`/dialogues/${d.id}`} className="block rounded-lg border border-line px-3 py-2 hover:bg-paper">
                {d.title}
              </Link>
            ))}
          </div>
        </Card>
      )}
      <Link href="/">
        <Button>Về trang chủ</Button>
      </Link>
    </div>
  );
}
