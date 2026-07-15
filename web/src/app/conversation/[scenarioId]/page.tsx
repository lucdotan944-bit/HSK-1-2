"use client";

import { useEffect, useState, use as usePromise } from "react";
import Link from "next/link";
import { api, type ConversationNode } from "@/lib/api";
import { Card, Button } from "@/components/ui";
import { useBadgeToast } from "@/components/BadgeToast";
import { speak } from "@/lib/speech";

export default function ConversationPage({ params }: { params: Promise<{ scenarioId: string }> }) {
  const { scenarioId } = usePromise(params);
  const { announce, toastNode } = useBadgeToast();
  const [title, setTitle] = useState("");
  const [nodeId, setNodeId] = useState<string | null>(null);
  const [node, setNode] = useState<ConversationNode | null>(null);
  const [isEnd, setIsEnd] = useState(false);
  const [history, setHistory] = useState<{ speaker: "npc" | "user"; cn: string; pinyin: string; vi: string }[]>([]);

  useEffect(() => {
    api.conversation(scenarioId).then((d) => {
      setTitle(d.title);
      setNodeId(d.start);
      setNode(d.node);
      setHistory([{ speaker: "npc", ...d.node.npc }]);
      speak(d.node.npc.cn);
    });
  }, [scenarioId]);

  async function choose(choiceId: string) {
    if (!nodeId || !node) return;
    const chosen = node.choices.find((c) => c.id === choiceId);
    if (chosen) setHistory((h) => [...h, { speaker: "user", cn: chosen.cn, pinyin: chosen.pinyin, vi: chosen.vi }]);
    const r = await api.conversationRespond(scenarioId, nodeId, choiceId);
    announce(r.newly_earned_badges);
    setNodeId(r.node_id);
    setNode(r.node);
    setIsEnd(r.is_end);
    setHistory((h) => [...h, { speaker: "npc", ...r.node.npc }]);
    speak(r.node.npc.cn);
  }

  if (!node) return <p className="text-ink-soft">Đang tải hội thoại...</p>;

  return (
    <div className="mx-auto max-w-lg space-y-4">
      {toastNode}
      <Link href="/daily" className="text-sm text-ink-soft">
        ← Học 5 phút
      </Link>
      <h1 className="font-display text-2xl font-bold">{title}</h1>

      <div className="space-y-3">
        {history.map((h, i) => (
          <div key={i} className={`flex ${h.speaker === "npc" ? "justify-start" : "justify-end"}`}>
            <button
              onClick={() => speak(h.cn)}
              className={`max-w-[85%] rounded-2xl border px-4 py-2.5 text-left ${
                h.speaker === "npc" ? "border-line bg-paper-raised" : "border-jade/40 bg-jade-soft"
              }`}
            >
              <p className="text-lg">{h.cn}</p>
              <p className="font-data text-sm text-jade">{h.pinyin}</p>
              <p className="text-sm text-ink-soft">{h.vi}</p>
            </button>
          </div>
        ))}
      </div>

      {!isEnd ? (
        <Card>
          <p className="mb-2 text-sm text-ink-soft">Bạn trả lời:</p>
          <div className="grid gap-2">
            {node.choices.map((c) => (
              <button
                key={c.id}
                onClick={() => choose(c.id)}
                className="rounded-xl border border-line bg-paper-raised px-4 py-2.5 text-left hover:bg-paper"
              >
                <p>{c.cn}</p>
                <p className="font-data text-xs text-ink-soft">{c.pinyin} — {c.vi}</p>
              </button>
            ))}
          </div>
        </Card>
      ) : (
        <div className="text-center">
          <p className="mb-3 font-display text-xl font-bold text-jade">🎉 Hoàn thành hội thoại! (+20 XP)</p>
          <Link href="/daily">
            <Button>Quay lại phiên học</Button>
          </Link>
        </div>
      )}
    </div>
  );
}
