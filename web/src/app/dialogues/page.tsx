import Link from "next/link";
import { api } from "@/lib/api";
import { Card, SectionTitle } from "@/components/ui";

export default async function DialoguesPage() {
  const { dialogues } = await api.dialogues();

  return (
    <div className="space-y-5">
      <SectionTitle sub="Hội thoại giao tiếp thực tế, có phiên âm và audio">Hội thoại</SectionTitle>
      <div className="grid gap-3 sm:grid-cols-2">
        {dialogues.map((d) => (
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
    </div>
  );
}
