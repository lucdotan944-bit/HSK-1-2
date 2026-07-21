"use client";

import { useEffect } from "react";

// Đăng ký service worker (public/sw.js) — bật cache offline cho nội dung
// giáo trình. Chỉ chạy ở production để không phá HMR khi dev.
export default function ServiceWorkerRegister() {
  useEffect(() => {
    if (process.env.NODE_ENV !== "production") return;
    if (!("serviceWorker" in navigator)) return;
    navigator.serviceWorker.register("/sw.js").catch(() => {
      // Không có SW cũng không sao — app vẫn hoạt động bình thường online.
    });
  }, []);
  return null;
}
