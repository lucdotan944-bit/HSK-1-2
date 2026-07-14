import Link from "next/link";
import { api } from "@/lib/api";
import { Card, StatChip, SectionTitle, Button } from "@/components/ui";
import SealStamp from "@/components/SealStamp";

export default async function HomePage() {
  const [stats, gamify, themes] = await Promise.all([api.stats(), api.gamifyState(), api.themes()]);

  return (
    <div className="space-y-8">
      <section>
        <p className="font-data text-xs uppercase tracking-[0.2em] text-seal">你好 · Xin chào</p>
        <h1 className="mt-1 font-display text-3xl font-bold leading-tight md:text-4xl">
          Học tiếng Trung qua gốc Hán-Việt
        </h1>
        <p className="mt-2 max-w-xl text-ink-soft">
          Mỗi chữ Hán đi kèm âm Hán-Việt bạn đã biết từ tiếng mẹ đẻ — học nhanh hơn, nhớ lâu hơn.
        </p>
      </section>

      {gamify.placement_level === 0 && (
        <Card className="flex flex-col items-start gap-3 border-seal/40 bg-seal-soft md:flex-row md:items-center md:justify-between">
          <div>
            <p className="font-display text-lg font-bold">Chưa biết bắt đầu từ đâu?</p>
            <p className="text-sm text-ink-soft">Làm bài test xếp trình độ 5 phút để hệ thống gợi ý điểm bắt đầu phù hợp.</p>
          </div>
          <Link href="/placement">
            <Button>Làm test ngay</Button>
          </Link>
        </Card>
      )}

      <div className="flex gap-2 overflow-x-auto pb-1">
        <StatChip value={gamify.xp} label="XP" />
        <StatChip value={`🔥${gamify.current_streak}`} label="streak" />
        <StatChip value={stats.due} label="cần ôn" />
        <StatChip value={stats.learned} label="đã thuộc" />
        <StatChip value={stats.total} label="từ" />
        <StatChip value={stats.dialogues} label="hội thoại" />
      </div>

      <Card className="flex items-center justify-between gap-4 bg-jade-soft">
        <div className="flex items-center gap-3">
          <SealStamp size={44} animate>
            钟
          </SealStamp>
          <div>
            <p className="font-display text-lg font-bold">Phiên học 5 phút hôm nay</p>
            <p className="text-sm text-ink-soft">Ôn từ · nghe · nói · hội thoại — cá nhân hoá theo điểm yếu của bạn.</p>
          </div>
        </div>
        <Link href="/daily">
          <Button variant="secondary">Bắt đầu</Button>
        </Link>
      </Card>

      <section>
        <SectionTitle sub="Chọn một chủ đề để học từ vựng theo nhóm">Chủ đề</SectionTitle>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          {themes.themes.map((t) => (
            <Link key={t.id} href={`/lesson/${t.id}`}>
              <Card className="flex h-full flex-col gap-2 transition-transform hover:-translate-y-0.5">
                <span className="text-2xl">{t.icon}</span>
                <span className="font-semibold leading-tight">{t.name}</span>
                <span className="font-data text-xs text-ink-soft">
                  {t.learned_words}/{t.total_words} từ
                </span>
              </Card>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
