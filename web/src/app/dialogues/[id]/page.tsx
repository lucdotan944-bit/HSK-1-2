import Link from "next/link";
import { notFound } from "next/navigation";
import { api, ApiError } from "@/lib/api";
import DialogueChat from "./DialogueChat";

export default async function DialogueDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  let result: Awaited<ReturnType<typeof api.dialogue>>;
  try {
    result = await api.dialogue(id);
  } catch (e) {
    if (e instanceof ApiError && e.status === 404) notFound();
    throw e;
  }
  const { dialogue, lines } = result;

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
