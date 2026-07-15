"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import SealStamp from "./SealStamp";

const NAV = [
  { href: "/", label: "Trang chủ", icon: "宅" },
  { href: "/daily", label: "Học 5 phút", icon: "钟" },
  { href: "/review", label: "Ôn tập", icon: "复" },
  { href: "/dialogues", label: "Hội thoại", icon: "话" },
  { href: "/exam", label: "Thi thử", icon: "试" },
  { href: "/progress", label: "Tiến độ", icon: "进" },
];

function ThemeToggle() {
  const [theme, setTheme] = useState<"light" | "dark">("light");

  useEffect(() => {
    const saved = (localStorage.getItem("hn-theme") as "light" | "dark" | null) ?? null;
    const initial = saved ?? (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    // eslint-disable-next-line react-hooks/set-state-in-effect -- one-time read of client-only storage/media on mount
    setTheme(initial);
    document.documentElement.setAttribute("data-theme", initial);
  }, []);

  function toggle() {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("hn-theme", next);
  }

  return (
    <button
      onClick={toggle}
      aria-label="Đổi giao diện sáng/tối"
      className="h-9 w-9 rounded-full border border-line flex items-center justify-center text-sm hover:bg-paper-raised transition-colors"
    >
      {theme === "dark" ? "☀︎" : "☾"}
    </button>
  );
}

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="flex min-h-full flex-col">
      <header className="sticky top-0 z-40 border-b border-line bg-paper/90 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
          <Link href="/" className="flex items-center gap-2">
            <SealStamp size={34}>汉</SealStamp>
            <span className="font-display text-lg font-bold tracking-tight">Hán Ngữ+</span>
          </Link>
          <nav className="hidden md:flex items-center gap-1">
            {NAV.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`rounded-full px-3.5 py-1.5 text-sm font-medium transition-colors ${
                  pathname === item.href
                    ? "bg-jade text-paper-raised"
                    : "text-ink-soft hover:bg-paper-raised hover:text-ink"
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>
          <ThemeToggle />
        </div>
      </header>

      <main className="mx-auto w-full max-w-5xl flex-1 px-4 pb-24 pt-6 md:pb-10">{children}</main>

      <nav className="fixed inset-x-0 bottom-0 z-40 border-t border-line bg-paper/95 backdrop-blur md:hidden">
        <div className="mx-auto flex max-w-5xl items-stretch justify-between px-1">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-1 flex-col items-center gap-0.5 py-2 text-[11px] font-medium ${
                pathname === item.href ? "text-seal" : "text-ink-soft"
              }`}
            >
              <span className="font-display text-lg leading-none">{item.icon}</span>
              {item.label}
            </Link>
          ))}
        </div>
      </nav>
    </div>
  );
}
