export function Card({
  children,
  className = "",
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={`rounded-2xl border border-line bg-paper-raised p-4 shadow-[0_1px_0_var(--line)] ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function StatChip({
  value,
  label,
  onClick,
}: {
  value: React.ReactNode;
  label: string;
  onClick?: () => void;
}) {
  const Comp = onClick ? "button" : "div";
  return (
    <Comp
      onClick={onClick}
      className="flex shrink-0 items-center gap-1.5 rounded-full border border-line bg-paper-raised px-3.5 py-1.5 text-sm whitespace-nowrap"
    >
      <span className="font-data font-bold text-jade">{value}</span>
      <span className="text-ink-soft">{label}</span>
    </Comp>
  );
}

export function ProgressBar({ value }: { value: number }) {
  return (
    <div className="h-2 w-full overflow-hidden rounded-full bg-line">
      <div
        className="h-full rounded-full bg-jade transition-all duration-300"
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  );
}

export function Button({
  variant = "primary",
  className = "",
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "primary" | "secondary" | "ghost" }) {
  const base = "rounded-full px-5 py-2.5 text-sm font-semibold transition-colors disabled:opacity-40 disabled:pointer-events-none";
  const styles = {
    primary: "bg-seal text-white hover:opacity-90",
    secondary: "bg-jade text-white hover:opacity-90",
    ghost: "border border-line text-ink hover:bg-paper",
  };
  return <button className={`${base} ${styles[variant]} ${className}`} {...props} />;
}

export function SectionTitle({ children, sub }: { children: React.ReactNode; sub?: string }) {
  return (
    <div className="mb-4">
      <h2 className="font-display text-2xl font-bold">{children}</h2>
      {sub && <p className="mt-1 text-sm text-ink-soft">{sub}</p>}
    </div>
  );
}
