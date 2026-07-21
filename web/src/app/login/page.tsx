"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { api, ApiError, AuthMe } from "@/lib/api";
import { Button, Card, SectionTitle } from "@/components/ui";

type Mode = "login" | "register";

export default function LoginPage() {
  // useSearchParams cần Suspense boundary khi prerender
  return (
    <Suspense>
      <LoginInner />
    </Suspense>
  );
}

function LoginInner() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [mode, setMode] = useState<Mode>("login");
  const [me, setMe] = useState<AuthMe | null>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api.authMe().then(setMe).catch(() => setMe(null));
    if (searchParams.get("error") === "google") {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- one-time read of the OAuth redirect param
      setError("Đăng nhập Google không thành công. Hãy thử lại hoặc dùng email.");
    }
  }, [searchParams]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setNotice("");
    setBusy(true);
    try {
      if (mode === "register") {
        const res = await api.authRegister(email, password, displayName);
        if (res.kept_progress) {
          setNotice("Đã tạo tài khoản và giữ nguyên toàn bộ tiến độ học của bạn!");
        }
      } else {
        await api.authLogin(email, password);
      }
      router.push("/account");
      router.refresh();
    } catch (err) {
      setError(err instanceof ApiError && err.detail ? err.detail : "Có lỗi xảy ra, hãy thử lại.");
    } finally {
      setBusy(false);
    }
  }

  if (me?.authenticated) {
    return (
      <div className="mx-auto max-w-md space-y-6">
        <SectionTitle sub="Bạn đã đăng nhập rồi">Tài khoản</SectionTitle>
        <Card className="space-y-3 text-center">
          <p>
            Đang đăng nhập với <span className="font-semibold">{me.email}</span>
          </p>
          <Link href="/account" className="inline-block">
            <Button>Xem tài khoản</Button>
          </Link>
        </Card>
      </div>
    );
  }

  const inputCls =
    "w-full rounded-xl border border-line bg-paper px-4 py-2.5 text-sm outline-none focus:border-jade";

  return (
    <div className="mx-auto max-w-md space-y-6">
      <SectionTitle
        sub={
          mode === "login"
            ? "Đăng nhập để đồng bộ tiến độ trên mọi thiết bị"
            : "Tạo tài khoản — tiến độ đang học trên máy này sẽ được giữ nguyên"
        }
      >
        {mode === "login" ? "Đăng nhập" : "Đăng ký"}
      </SectionTitle>

      <div className="flex rounded-full border border-line p-1">
        {(["login", "register"] as Mode[]).map((m) => (
          <button
            key={m}
            onClick={() => {
              setMode(m);
              setError("");
            }}
            className={`flex-1 rounded-full py-2 text-sm font-semibold transition-colors ${
              mode === m ? "bg-jade text-white" : "text-ink-soft hover:text-ink"
            }`}
          >
            {m === "login" ? "Đăng nhập" : "Đăng ký"}
          </button>
        ))}
      </div>

      <Card>
        <form onSubmit={submit} className="space-y-4">
          {mode === "register" && (
            <div>
              <label className="mb-1 block text-sm font-medium">Tên hiển thị</label>
              <input
                className={inputCls}
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                placeholder="Ví dụ: Lục"
                maxLength={60}
              />
            </div>
          )}
          <div>
            <label className="mb-1 block text-sm font-medium">Email</label>
            <input
              className={inputCls}
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="ban@example.com"
              autoComplete="email"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Mật khẩu</label>
            <input
              className={inputCls}
              type="password"
              required
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Ít nhất 8 ký tự"
              autoComplete={mode === "login" ? "current-password" : "new-password"}
            />
          </div>

          {error && <p className="text-sm text-seal">{error}</p>}
          {notice && <p className="text-sm text-jade">{notice}</p>}

          <Button type="submit" disabled={busy} className="w-full">
            {busy ? "Đang xử lý…" : mode === "login" ? "Đăng nhập" : "Tạo tài khoản"}
          </Button>
        </form>

        {me?.google_enabled && (
          <>
            <div className="my-4 flex items-center gap-3 text-xs text-ink-soft">
              <div className="h-px flex-1 bg-line" />
              hoặc
              <div className="h-px flex-1 bg-line" />
            </div>
            <a
              href="/api/auth/google/start"
              className="flex w-full items-center justify-center gap-2 rounded-full border border-line py-2.5 text-sm font-semibold hover:bg-paper"
            >
              <span aria-hidden>G</span> Tiếp tục với Google
            </a>
          </>
        )}
      </Card>

      <p className="text-center text-xs text-ink-soft">
        Chưa cần tài khoản vẫn học được — tiến độ lưu theo trình duyệt này. Đăng ký bất cứ lúc nào để
        không mất dữ liệu khi đổi máy.
      </p>
    </div>
  );
}
