"use client";

import { useEffect, useRef, useState } from "react";
import { Card, Button } from "@/components/ui";
import {
  getSpeechRecognition,
  openMicLevelMeter,
  scorePronunciation,
  speak,
  describeSpeechError,
  listenOnce,
  SpeechRecognitionError,
  MIC_CHECK_PHRASES,
  type PronScore,
} from "@/lib/speech";

type Step = "support" | "level" | "speak" | "done";

const ICONS: Record<PronScore, string> = { ok: "✅", warn: "⚠️", fail: "❌" };

export default function MicCheck({ onFinished }: { onFinished?: () => void }) {
  const [step, setStep] = useState<Step>("support");
  const [speechSupported, setSpeechSupported] = useState<boolean | null>(null);
  const [micError, setMicError] = useState<string | null>(null);
  const [level, setLevel] = useState(0);
  const [heardSound, setHeardSound] = useState(false);
  const closeMeterRef = useRef<(() => void) | null>(null);

  const [phrase, setPhrase] = useState(MIC_CHECK_PHRASES[0]);
  const [listening, setListening] = useState(false);
  const [speakResult, setSpeakResult] = useState<{ score: PronScore; text: string } | null>(null);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- one-time client-only checks on mount
    setSpeechSupported(!!getSpeechRecognition() && !!navigator.mediaDevices?.getUserMedia);
    setPhrase(MIC_CHECK_PHRASES[Math.floor(Math.random() * MIC_CHECK_PHRASES.length)]);
  }, []);

  useEffect(() => {
    return () => closeMeterRef.current?.();
  }, []);

  async function startLevelCheck() {
    setMicError(null);
    setStep("level");
    try {
      closeMeterRef.current = await openMicLevelMeter((lv) => {
        setLevel(lv);
        if (lv > 0.08) setHeardSound(true);
      });
    } catch {
      setMicError("Không thể truy cập micro. Hãy cấp quyền micro cho trang này trong cài đặt trình duyệt rồi thử lại.");
    }
  }

  function goToSpeakStep() {
    closeMeterRef.current?.();
    closeMeterRef.current = null;
    setStep("speak");
  }

  async function trySpeak() {
    setListening(true);
    setSpeakResult(null);
    try {
      const recognized = await listenOnce("zh-CN");
      const score = scorePronunciation(phrase.simplified, recognized);
      setSpeakResult({ score, text: recognized });
    } catch (e) {
      const code = e instanceof SpeechRecognitionError ? e.code : "unknown";
      setSpeakResult({ score: "fail", text: describeSpeechError(code) });
    } finally {
      setListening(false);
    }
  }

  if (step === "support") {
    return (
      <Card className="mx-auto max-w-md space-y-4 text-center">
        <p className="text-4xl">🎙️</p>
        <h2 className="font-display text-xl font-bold">Kiểm tra giọng nói đầu vào</h2>
        <p className="text-sm text-ink-soft">
          Trước khi luyện nói, hãy kiểm tra micro để chắc chắn tính năng nhận diện giọng nói hoạt động tốt.
        </p>
        {speechSupported === false && (
          <p className="rounded-xl border border-seal/40 bg-seal-soft p-3 text-sm text-ink">
            Trình duyệt này chưa hỗ trợ nhận diện giọng nói. Hãy dùng Chrome hoặc Edge trên máy tính hoặc Android để
            luyện phát âm.
          </p>
        )}
        <Button onClick={startLevelCheck} disabled={speechSupported !== true}>
          Bắt đầu kiểm tra
        </Button>
      </Card>
    );
  }

  if (step === "level") {
    return (
      <Card className="mx-auto max-w-md space-y-4 text-center">
        <p className="text-4xl">🎤</p>
        <h2 className="font-display text-xl font-bold">Nói thử vài từ...</h2>
        <p className="text-sm text-ink-soft">Hãy nói to bất kỳ điều gì để kiểm tra micro có nhận được âm thanh không.</p>
        {micError ? (
          <div className="space-y-3">
            <p className="rounded-xl border border-seal/40 bg-seal-soft p-3 text-sm text-ink">{micError}</p>
            <Button onClick={startLevelCheck}>Thử lại</Button>
          </div>
        ) : (
          <>
            <div className="h-4 w-full overflow-hidden rounded-full bg-line">
              <div
                className="h-full rounded-full bg-jade transition-[width] duration-75"
                style={{ width: `${Math.round(level * 100)}%` }}
              />
            </div>
            <p className="font-data text-xs text-ink-soft">
              {heardSound ? "✅ Đã nhận được âm thanh từ micro" : "Đang chờ âm thanh..."}
            </p>
            <Button onClick={goToSpeakStep} disabled={!heardSound}>
              Tiếp tục
            </Button>
          </>
        )}
      </Card>
    );
  }

  if (step === "speak") {
    return (
      <Card className="mx-auto max-w-md space-y-4 text-center">
        <p className="text-4xl">🗣️</p>
        <h2 className="font-display text-xl font-bold">Đọc to từ này</h2>
        <button
          onClick={() => speak(phrase.simplified)}
          className="mx-auto flex flex-col items-center gap-1 rounded-xl border border-line bg-paper-raised px-6 py-4 hover:bg-paper"
        >
          <span className="font-display text-4xl">{phrase.simplified}</span>
          <span className="font-data text-base text-jade">{phrase.pinyin}</span>
          <span className="text-xs text-ink-soft">(bấm để nghe mẫu)</span>
        </button>
        <button
          onClick={trySpeak}
          aria-label="Ghi âm"
          className={`mx-auto flex h-14 w-14 items-center justify-center rounded-full border border-line text-2xl transition-colors ${
            listening ? "animate-pulse bg-seal-soft" : "bg-paper-raised hover:bg-paper"
          }`}
        >
          🎤
        </button>
        {speakResult && (
          <p className="text-sm text-ink-soft">
            {ICONS[speakResult.score]} {speakResult.text}
          </p>
        )}
        <div className="flex justify-center gap-2">
          {speakResult && speakResult.score !== "fail" ? (
            <Button onClick={() => setStep("done")}>Micro hoạt động tốt →</Button>
          ) : (
            speakResult && <Button variant="ghost" onClick={trySpeak}>Thử lại</Button>
          )}
        </div>
      </Card>
    );
  }

  return (
    <Card className="mx-auto max-w-md space-y-4 text-center">
      <p className="text-4xl">✅</p>
      <h2 className="font-display text-xl font-bold">Micro đã sẵn sàng!</h2>
      <p className="text-sm text-ink-soft">Bạn có thể bắt đầu luyện nói và các bài học có phần phát âm.</p>
      <Button onClick={onFinished}>Tiếp tục</Button>
    </Card>
  );
}
