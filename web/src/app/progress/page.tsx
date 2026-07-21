import Link from "next/link";
import { api } from "@/lib/api";
import { Card, SectionTitle, ProgressBar } from "@/components/ui";
import SkillRadar from "@/components/SkillRadar";
import { TIERS } from "@/lib/hsk";

export default async function ProgressPage() {
  const [progress, gamify, skillData, badges, mistakes] = await Promise.all([
    api.progress(),
    api.gamifyState(),
    api.skillBreakdown(),
    api.badges(),
    api.mistakesSummary(),
  ]);

  return (
    <div className="space-y-8">
      <SectionTitle sub="Điểm mạnh/yếu và huy hiệu bạn đã đạt được">Tiến độ</SectionTitle>

      <div className="grid gap-4 sm:grid-cols-3">
        <Card className="text-center">
          <p className="font-data text-3xl font-bold text-jade">{gamify.xp}</p>
          <p className="text-sm text-ink-soft">Tổng XP</p>
        </Card>
        <Card className="text-center">
          <p className="font-data text-3xl font-bold text-seal">🔥{gamify.current_streak}</p>
          <p className="text-sm text-ink-soft">Streak hiện tại (dài nhất: {gamify.longest_streak})</p>
        </Card>
        <Card className="text-center">
          <p className="font-data text-3xl font-bold">{progress.today_reviewed}</p>
          <p className="text-sm text-ink-soft">Đã ôn hôm nay</p>
        </Card>
      </div>

      <Card>
        <p className="mb-3 text-center font-semibold">Bản đồ kỹ năng</p>
        <SkillRadar skills={skillData.skills} />
        <p className="mt-3 text-center text-sm text-ink-soft">{skillData.explanation_vi}</p>
      </Card>

      <section className="space-y-5">
        <p className="font-semibold">Theo cấp độ HSK</p>
        {TIERS.map((tier) => {
          const levels = progress.levels.filter((l) => tier.levels.includes(l.hsk_level));
          if (!levels.length) return null;
          return (
            <div key={tier.id}>
              <p className="mb-2 font-data text-xs uppercase tracking-wide text-ink-soft">
                {tier.label} · {tier.sublabel}
              </p>
              <div className="space-y-3">
                {levels.map((l) => (
                  <Card key={l.hsk_level}>
                    <div className="mb-1 flex items-center justify-between text-sm">
                      <span className="font-semibold">HSK {l.hsk_level}</span>
                      <span className="font-data text-ink-soft">
                        {l.mastered}/{l.total} thuộc
                      </span>
                    </div>
                    <ProgressBar value={l.total ? (l.mastered / l.total) * 100 : 0} />
                  </Card>
                ))}
              </div>
            </div>
          );
        })}
      </section>

      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <p className="font-semibold">Phân tích lỗi sai (30 ngày qua)</p>
          {mistakes.total_wrong > 0 && (
            <Link
              href="/review?mode=mistakes"
              className="rounded-full bg-seal px-4 py-1.5 text-sm font-semibold text-white hover:opacity-90"
            >
              Ôn lại từ đã sai
            </Link>
          )}
        </div>

        {mistakes.total_wrong === 0 ? (
          <Card>
            <p className="text-sm text-ink-soft">
              Chưa có lỗi sai nào được ghi nhận gần đây. Làm bài ôn tập, quiz hoặc thi thử để hệ
              thống phân tích điểm yếu cho bạn.
            </p>
          </Card>
        ) : (
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <p className="mb-2 text-sm font-semibold">Từ sai nhiều nhất</p>
              <ul className="space-y-2">
                {mistakes.top_wrong_words.map((w) => (
                  <li key={w.id} className="flex items-center justify-between gap-2 text-sm">
                    <span>
                      <span className="font-display text-lg">{w.simplified}</span>{" "}
                      <span className="text-ink-soft">{w.pinyin}</span>
                      {w.sino_viet && <span className="ml-1 text-xs text-brass">({w.sino_viet})</span>}
                    </span>
                    <span className="shrink-0 rounded-full bg-seal/10 px-2 py-0.5 font-data text-xs text-seal">
                      sai {w.wrong_count} lần
                    </span>
                  </li>
                ))}
              </ul>
            </Card>
            <Card>
              <p className="mb-2 text-sm font-semibold">Chủ đề cần củng cố</p>
              {mistakes.weak_themes.length === 0 ? (
                <p className="text-sm text-ink-soft">Chưa đủ dữ liệu theo chủ đề.</p>
              ) : (
                <ul className="space-y-2">
                  {mistakes.weak_themes.map((t) => (
                    <li key={t.id} className="text-sm">
                      <div className="mb-1 flex items-center justify-between">
                        <span>
                          {t.icon} {t.name}
                        </span>
                        <span className="font-data text-xs text-ink-soft">
                          {t.correct}/{t.total} đúng ({t.pct}%)
                        </span>
                      </div>
                      <ProgressBar value={t.pct ?? 0} />
                    </li>
                  ))}
                </ul>
              )}
            </Card>
          </div>
        )}
      </section>

      <section>
        <p className="mb-3 font-semibold">Huy hiệu</p>
        <div className="grid grid-cols-3 gap-3 sm:grid-cols-5">
          {badges.badges.map((b) => (
            <div
              key={b.badge_id}
              title={b.desc}
              className={`flex flex-col items-center gap-1 rounded-xl border p-3 text-center ${
                b.earned ? "border-brass bg-brass-soft" : "border-line opacity-40"
              }`}
            >
              <span className="text-2xl">{b.icon}</span>
              <span className="text-xs font-medium">{b.name}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
