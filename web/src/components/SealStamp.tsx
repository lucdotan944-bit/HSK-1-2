export default function SealStamp({
  children,
  size = 28,
  animate = false,
  className = "",
}: {
  children: React.ReactNode;
  size?: number;
  animate?: boolean;
  className?: string;
}) {
  return (
    <span
      className={`seal-stamp ${animate ? "seal-stamp-animate" : ""} ${className}`}
      style={{ width: size, height: size, fontSize: size * 0.5 }}
    >
      {children}
    </span>
  );
}
