import type { Metadata } from "next";
import { Be_Vietnam_Pro, Noto_Serif_SC, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import AppShell from "@/components/AppShell";

const bodySans = Be_Vietnam_Pro({
  variable: "--font-body",
  subsets: ["latin", "vietnamese"],
  weight: ["400", "500", "600", "700"],
});

const displaySerif = Noto_Serif_SC({
  variable: "--font-display",
  subsets: ["latin"],
  weight: ["600", "700", "900"],
});

const dataMono = JetBrains_Mono({
  variable: "--font-data",
  subsets: ["latin"],
  weight: ["400", "500", "700"],
});

export const metadata: Metadata = {
  title: "Hán Ngữ+ — Học tiếng Trung cho người Việt",
  description:
    "Học HSK qua lợi thế Hán-Việt: từ vựng, ngữ pháp, nghe, nói và luyện viết chữ Hán — miễn phí, cá nhân hoá mỗi ngày.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="vi"
      className={`${bodySans.variable} ${displaySerif.variable} ${dataMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-paper text-ink">
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
