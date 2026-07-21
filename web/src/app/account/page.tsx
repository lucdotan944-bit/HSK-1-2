"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api, AuthMe, GamifyState } from "@/lib/api";
import { Button, Card, SectionTitle } from "@/components/ui";

export default function AccountPage() {
  const router = useRouter();
  const [me, setMe] = useState<AuthMe | null>(null);
  const [gamify, setGamify] = useState<GamifyState | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api.authMe().then(setMe).catch(() => setMe(null));
    api.gamifyState().then(setGamify).catch(() => setGamify(null));
  }, []);

  async function logout() {
    setBusy(true);
    try {
      await api.authLogout();
      router.push("/");
      router.refresh();
    } finally {
      setBusy(false);
    }
  }

  if (!me) {
    return <p className="text-center text-sm text-ink-soft">Đang tải…</p>;
  }

  if (!me.authenticated) {
    return (
      <div className="mx-auto max-w-md space-y-6">
        <SectionTitle sub="Bạn đang học với tư cách khách trên trình duyệt này">Tài khoản</SectionTitle>
        <Card className="space-y-4 text-center">
          <p className="text-sm text-ink-soft">
            Tiến độ hiện được lưu theo trình duyệt. Tạo tài khoản để giữ an toàn dữ liệu và đồng bộ
            giữa điện thoại với máy tính — toàn bộ XP, streak và lịch ôn tập hiện tại sẽ được giữ
            nguyên.
          </p>
          <Link href="/login" className="inline-block">
            <Button>Đăng nhập / Đăng ký</Button>
          </Link>
        </Card>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-md space-y-6">
      <SectionTitle sub="Thông tin tài khoản và đồng bộ">Tài khoản</SectionTitle>

      <Card className="space-y-3">
        <div className="flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-jade text-lg font-bold text-white">
            {(me.display_name || me.email || "?").charAt(0).toUpperCase()}
          </div>
          <div>
            <p className="font-semibold">{me.display_name || "Chưa đặt tên"}</p>
            <p className="text-sm text-ink-soft">{me.email}</p>
          </div>
        </div>
        <p className="text-sm text-jade">
          ✓ Tiến độ của bạn được lưu trên máy chủ — đăng nhập trên thiết bị khác là thấy ngay.
        </p>
      </Card>

      {gamify && (
        <div className="grid grid-cols-3 gap-3">
          <Card className="text-center">
            <p className="font-data text-2xl font-bold text-jade">{gamify.xp}</p>
            <p className="text-xs text-ink-soft">XP</p>
          </Card>
          <Card className="text-center">
            <p className="font-data text-2xl font-bold text-seal">🔥{gamify.current_streak}</p>
            <p className="text-xs text-ink-soft">Streak</p>
          </Card>
          <Card className="text-center">
            <p className="font-data text-2xl font-bold">{gamify.badges.length}</p>
            <p className="text-xs text-ink-soft">Huy hiệu</p>
          </Card>
        </div>
      )}

      <Button variant="ghost" onClick={logout} disabled={busy} className="w-full">
        {busy ? "Đang đăng xuất…" : "Đăng xuất"}
      </Button>
    </div>
  );
}
