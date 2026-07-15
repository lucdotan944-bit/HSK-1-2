import Link from "next/link";
import { api } from "@/lib/api";
import DialogueChat from "./DialogueChat";

export default async function DialogueDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const { dialogue, lines } = await api.dialogue(id);

  return (
    <div className="mx-auto max-w-lg space-y-4">
      <Link href="/dialogues" className="text-sm text-ink-soft">
        ← Hội thoại
      </Link>
      <h1 className="font-display text-2xl font-bold">{dialogue.title}</h1>
      <p className="text-ink-soft">{dialogue.context}</p>
      <DialogueChat lines={lines} />
    </div>
  );
}
