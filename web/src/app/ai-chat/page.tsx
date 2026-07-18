"use client";

import { Suspense, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import {
  api,
  ApiError,
  type AiChatReply,
  type AiChatStatus,
  type AiChatSuggestion,
  type Theme,
} from "@/lib/api";
import { Button, Card } from "@/components/ui";
import { useBadgeToast } from "@/components/BadgeToast";
import { usePreferredLevel } from "@/lib/level";
import { speak, listenOnce, getSpeechRecognition, describeSpeechError, SpeechRecognitionError } from "@/lib/speech";

type ChatMessage =
  | { role: "user"; content: string }
  | {
      role: "assistant";
      content: string; // reply_cn — what gets sent back as history
      pinyin: string;
      vi: string;
      correction: AiChatReply["correction"];
    };

const STARTERS: AiChatSuggestion[] = [
  { cn: "你好！", pinyin: "Nǐ hǎo!", vi: "Xin chào!" },
  { cn: "你好，你叫什么名字？", pinyin: "Nǐ hǎo, nǐ jiào shénme míngzi?", vi: "Chào bạn, bạn tên gì?" },
];

function AiChatInner() {
  const params = useSearchParams();
  const topicId = params.get("topic") || undefined;
  const [level] = usePreferredLevel(1);
  const { announce, toastNode } = useBadgeToast();

  const [status, setStatus] = useState<AiChatStatus | null>(null);
  const [topicName, setTopicName] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [suggestions, setSuggestions] = useState<AiChatSuggestion[]>(STARTERS);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [listening, setListening] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showVi, setShowVi] = useState<Record<number, boolean>>({});
  const [micSupported, setMicSupported] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- must be set after mount: deciding this during SSR causes a hydration mismatch
    setMicSupported(!!getSpeechRecognition());
    api.aiChatStatus().then(setStatus, () => setStatus(null));
  }, []);

  useEffect(() => {
    if (!topicId) return;
    let active = true;
    api.themes().then(
      (t) => {
        if (!active) return;
        const theme = t.themes.find((x: Theme) => x.id === topicId);
        if (theme) setTopicName(theme.name);
      },
      () => {}
    );
    return () => {
      active = false;
    };
  }, [topicId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, busy]);

  async function send(text: string) {
    const content = text.trim();
    if (!content || busy) return;
    setError(null);
    setInput("");
    const history = [...messages, { role: "user" as const, content }];
    setMessages(history);
    setSuggestions([]);
    setBusy(true);
    try {
      const r = await api.aiChatRespond(
        history.map((m) => ({ role: m.role, content: m.content })),
        level,
        topicId
      );
      announce(r.newly_earned_badges || []);
      setMessages([
        ...history,
        { role: "assistant", content: r.reply_cn, pinyin: r.reply_pinyin, vi: r.reply_vi, correction: r.correction },
      ]);
      setSuggestions(r.suggestions || []);
      if (status && r.remaining_today !== null) setStatus({ ...status, remaining_today: r.remaining_today });
      speak(r.reply_cn);
    } catch (e) {
      const detail = e instanceof ApiError ? e.detail : undefined;
      setError(detail || "Không gửi được tin nhắn, vui lòng thử lại.");
      setMessages(history.slice(0, -1));
      setInput(content);
    } finally {
      setBusy(false);
    }
  }

  async function listen() {
    setListening(true);
    setError(null);
    try {
      const transcript = await listenOnce("zh-CN");
      setInput(transcript);
    } catch (e) {
      const code = e instanceof SpeechRecognitionError ? e.code : "unknown";
      setError(describeSpeechError(code));
    } finally {
      setListening(false);
    }
  }

  const outOfTurns = status !== null && status.enabled && status.remaining_today <= 0;

  return (
    <div className="mx-auto flex max-w-md flex-col gap-4">
      {toastNode}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-xl font-bold">💬 Luyện nói với AI</h1>
          <p className="font-data text-xs text-ink-soft">
            {topicName ? `Chủ đề: ${topicName}` : "Trò chuyện tự do"} · HSK {level}
          </p>
        </div>
        {status?.enabled && (
          <span className="rounded-full border border-line bg-paper-raised px-3 py-1 font-data text-xs text-ink-soft">
            còn {status.remaining_today}/{status.limit} lượt
          </span>
        )}
      </div>

      {status !== null && !status.enabled && (
        <p className="rounded-xl border border-brass bg-brass-soft px-3 py-2 text-sm text-brass">
          🧪 Chế độ demo: bạn đang trò chuyện với kịch bản mẫu. Khi quản trị viên thêm API key, AI sẽ trò chuyện thật
          theo trình độ của bạn.
        </p>
      )}

      <div className="space-y-3">
        {messages.length === 0 && (
          <Card className="text-center text-sm text-ink-soft">
            👋 Hãy mở lời bằng tiếng Trung để bắt đầu — chọn câu gợi ý bên dưới, gõ chữ, hoặc bấm 🎤 để nói. AI sẽ trả
            lời kèm pinyin, nghĩa tiếng Việt và sửa lỗi cho bạn.
          </Card>
        )}
        {messages.map((m, i) =>
          m.role === "user" ? (
            <div key={i} className="flex justify-end">
              <div className="max-w-[85%] rounded-2xl rounded-br-md bg-jade px-4 py-2.5 text-white">
                <p className="font-display text-lg">{m.content}</p>
              </div>
            </div>
          ) : (
            <div key={i} className="flex flex-col items-start gap-1.5">
              {m.correction && (
                <div className="max-w-[90%] rounded-xl border border-brass bg-brass-soft px-3 py-2 text-sm">
                  <p className="font-semibold text-brass">💡 Gợi ý sửa: {m.correction.corrected_cn}</p>
                  <p className="text-ink-soft">{m.correction.explanation_vi}</p>
                </div>
              )}
              <div className="max-w-[90%] rounded-2xl rounded-bl-md border border-line bg-paper-raised px-4 py-2.5">
                <button onClick={() => speak(m.content)} className="text-left" aria-label="Nghe lại">
                  <p className="font-display text-xl">{m.content} 🔊</p>
                </button>
                <p className="font-data text-sm text-jade">{m.pinyin}</p>
                {showVi[i] ? (
                  <p className="text-sm text-ink-soft">{m.vi}</p>
                ) : (
                  <button
                    onClick={() => setShowVi((s) => ({ ...s, [i]: true }))}
                    className="text-xs text-ink-soft underline"
                  >
                    Xem nghĩa
                  </button>
                )}
              </div>
            </div>
          )
        )}
        {busy && <p className="text-sm text-ink-soft">AI đang trả lời…</p>}
        <div ref={bottomRef} />
      </div>

      {error && <p className="rounded-xl border border-seal bg-seal-soft px-3 py-2 text-sm text-seal">{error}</p>}

      {outOfTurns ? (
        <Card className="text-center text-sm text-ink-soft">
          Bạn đã dùng hết lượt trò chuyện AI hôm nay 🎉 Quay lại vào ngày mai, hoặc luyện tiếp với{" "}
          <Link href="/dialogues" className="text-jade underline">
            hội thoại mẫu
          </Link>
          .
        </Card>
      ) : (
        <>
          {suggestions.length > 0 && !busy && (
            <div className="flex flex-wrap gap-2">
              {suggestions.map((s) => (
                <button
                  key={s.cn}
                  onClick={() => send(s.cn)}
                  title={`${s.pinyin} — ${s.vi}`}
                  className="rounded-full border border-line bg-paper-raised px-3 py-1.5 text-sm hover:bg-paper"
                >
                  {s.cn} <span className="text-xs text-ink-soft">{s.vi}</span>
                </button>
              ))}
            </div>
          )}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              send(input);
            }}
            className="flex items-center gap-2"
          >
            {micSupported && (
              <button
                type="button"
                onClick={listen}
                disabled={listening || busy}
                aria-label="Nói bằng micro"
                className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-line text-lg transition-colors ${
                  listening ? "animate-pulse bg-seal-soft" : "bg-paper-raised hover:bg-paper"
                }`}
              >
                🎤
              </button>
            )}
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Gõ tiếng Trung (hoặc tiếng Việt nếu bí)…"
              className="min-w-0 flex-1 rounded-full border border-line bg-paper-raised px-4 py-2.5 text-sm outline-none focus:border-jade"
            />
            <Button type="submit" disabled={busy || !input.trim()}>
              Gửi
            </Button>
          </form>
        </>
      )}
    </div>
  );
}

export default function AiChatPage() {
  return (
    <Suspense>
      <AiChatInner />
    </Suspense>
  );
}
