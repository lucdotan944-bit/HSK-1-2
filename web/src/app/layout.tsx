import type { Metadata, Viewport } from "next";
import { Be_Vietnam_Pro, Noto_Serif_SC, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import AppShell from "@/components/AppShell";
import ServiceWorkerRegister from "@/components/ServiceWorkerRegister";

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

const SITE_URL = "https://hsk-1-2.vercel.app";
const TITLE = "Hán Ngữ+ — Học tiếng Trung cho người Việt";
const DESCRIPTION =
  "Học HSK qua lợi thế Hán-Việt: từ vựng, ngữ pháp, nghe, nói và luyện viết chữ Hán — miễn phí, cá nhân hoá mỗi ngày.";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: TITLE,
    template: "%s — Hán Ngữ+",
  },
  description: DESCRIPTION,
  keywords: ["học tiếng Trung", "HSK", "Hán Việt", "từ vựng HSK", "luyện viết chữ Hán", "học HSK online"],
  openGraph: {
    title: TITLE,
    description: DESCRIPTION,
    url: SITE_URL,
    siteName: "Hán Ngữ+",
    locale: "vi_VN",
    type: "website",
  },
  twitter: {
    card: "summary",
    title: TITLE,
    description: DESCRIPTION,
  },
  icons: {
    icon: [{ url: "/icon-192.png", sizes: "192x192", type: "image/png" }],
    apple: [{ url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" }],
  },
};

export const viewport: Viewport = {
  themeColor: "#3f6659",
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
        <ServiceWorkerRegister />
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
