import type { SkillBreakdown } from "@/lib/api";

const ORDER: (keyof SkillBreakdown["skills"])[] = ["vocab", "listening", "grammar", "speaking"];

export default function SkillRadar({ skills }: { skills: SkillBreakdown["skills"] }) {
  const size = 220;
  const c = size / 2;
  const maxR = c - 36;
  const angleFor = (i: number) => (Math.PI * 2 * i) / ORDER.length - Math.PI / 2;

  const points = ORDER.map((key, i) => {
    const score = skills[key]?.score ?? 0;
    const r = (score / 100) * maxR;
    const a = angleFor(i);
    return [c + r * Math.cos(a), c + r * Math.sin(a)] as const;
  });
  const polygon = points.map((p) => p.join(",")).join(" ");

  const rings = [0.25, 0.5, 0.75, 1];

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="mx-auto w-full max-w-[260px]">
      {rings.map((f) => (
        <polygon
          key={f}
          points={ORDER.map((_, i) => {
            const a = angleFor(i);
            return `${c + maxR * f * Math.cos(a)},${c + maxR * f * Math.sin(a)}`;
          }).join(" ")}
          fill="none"
          stroke="var(--line)"
        />
      ))}
      {ORDER.map((_, i) => {
        const a = angleFor(i);
        return (
          <line
            key={i}
            x1={c}
            y1={c}
            x2={c + maxR * Math.cos(a)}
            y2={c + maxR * Math.sin(a)}
            stroke="var(--line)"
          />
        );
      })}
      <polygon points={polygon} fill="var(--seal-soft)" stroke="var(--seal)" strokeWidth={2} />
      {ORDER.map((key, i) => {
        const a = angleFor(i);
        const lx = c + (maxR + 22) * Math.cos(a);
        const ly = c + (maxR + 22) * Math.sin(a);
        const s = skills[key];
        return (
          <text
            key={key}
            x={lx}
            y={ly}
            textAnchor="middle"
            dominantBaseline="middle"
            className="fill-ink font-body text-[11px] font-semibold"
          >
            {s.label} {s.score !== null ? `${s.score}%` : "–"}
          </text>
        );
      })}
    </svg>
  );
}
