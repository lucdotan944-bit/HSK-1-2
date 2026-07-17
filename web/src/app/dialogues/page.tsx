"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type DialogueSummary } from "@/lib/api";
import { Card, SectionTitle } from "@/components/ui";
import { usePreferredLevel } from "@/lib/level";

export default function DialoguesPage() {
  const [level] = usePreferredLevel(1);
  const [dialogues, setDialogues] = useState<DialogueSummary[]>([]);
  const [loadError, setLoadError] = useState(false);

  useEffect(() => {
    let active = true;
    api.dialogues().then(
      (d) => {
        if (active) setDialogues(d.dialogues);
      },
      () => {
        if (active) setLoadError(true);
      }
    );
    return () => {
      active = false;
    };
  }, []);

  const shown = dialogues.filter((d) => d.hsk_level === level);

  return (
    <div className="space-y-5">
      <SectionTitle sub="Hội thoại giao tiếp thực tế, có phiên âm và audio">Hội thoại</SectionTitle>
      <p className="font-data text-sm text-ink-soft">
        Đang xem HSK {level} —{" "}
        <Link href="/" className="text-jade underline">
          đổi cấp ở Trang chủ
        </Link>
      </p>
      {loadError ? (
        <p className="text-sm text-seal">Không tải được danh sách hội thoại. Vui lòng thử lại.</p>
      ) : shown.length === 0 ? (
        <p className="text-sm text-ink-soft">Chưa có hội thoại nào cho HSK {level}.</p>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2">
          {shown.map((d) => (
            <Link key={d.id} href={`/dialogues/${d.id}`}>
              <Card className="flex h-full flex-col gap-1 transition-transform hover:-translate-y-0.5">
                <div className="flex items-center justify-between">
                  <span className="font-semibold">{d.title}</span>
                  <span className="rounded-full bg-jade-soft px-2 py-0.5 font-data text-xs text-jade">HSK {d.hsk_level}</span>
                </div>
                <p className="text-sm text-ink-soft">{d.context}</p>
                <p className="font-data text-xs text-ink-soft">{d.line_count} câu</p>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
