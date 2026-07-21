"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import SealStamp from "./SealStamp";
import { api, AuthMe } from "@/lib/api";

const NAV = [
  { href: "/", label: "Trang chủ", icon: "宅" },
  { href: "/daily", label: "Học 5 phút", icon: "钟" },
  { href: "/review", label: "Ôn tập", icon: "复" },
  { href: "/grammar", label: "Ngữ pháp", icon: "法" },
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

function AccountButton() {
  const pathname = usePathname();
  const [me, setMe] = useState<AuthMe | null>(null);

  // Refetch khi đổi trang: login/logout điều hướng nên trạng thái luôn mới.
  useEffect(() => {
    let cancelled = false;
    api.authMe().then((m) => {
      if (!cancelled) setMe(m);
    }).catch(() => {});
    return () => {
      cancelled = true;
    };
  }, [pathname]);

  const authed = me?.authenticated;
  const initial = (me?.display_name || me?.email || "").charAt(0).toUpperCase();
  return (
    <Link
      href={authed ? "/account" : "/login"}
      aria-label={authed ? "Tài khoản" : "Đăng nhập"}
      className={`flex h-9 w-9 items-center justify-center rounded-full border text-sm font-semibold transition-colors ${
        authed
          ? "border-jade bg-jade text-white"
          : "border-line text-ink-soft hover:bg-paper-raised hover:text-ink"
      }`}
    >
      {authed && initial ? initial : "登"}
    </Link>
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
          <div className="flex items-center gap-2">
            <AccountButton />
            <ThemeToggle />
          </div>
        </div>
      </header>

      <main className="mx-auto w-full max-w-5xl flex-1 px-4 pb-24 pt-6 md:pb-10">{children}</main>

      <footer className="hidden border-t border-line px-4 py-4 text-center text-xs text-ink-soft md:block">
        <Link href="/privacy" className="hover:text-ink hover:underline">
          Chính sách bảo mật
        </Link>
      </footer>

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
