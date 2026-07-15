import { api } from "@/lib/api";
import { Card, SectionTitle, ProgressBar } from "@/components/ui";
import SkillRadar from "@/components/SkillRadar";
import { TIERS } from "@/lib/hsk";

export default async function ProgressPage() {
  const [progress, gamify, skillData, badges] = await Promise.all([
    api.progress(),
    api.gamifyState(),
    api.skillBreakdown(),
    api.badges(),
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
