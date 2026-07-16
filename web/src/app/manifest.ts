import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Hán Ngữ+ — Học tiếng Trung cho người Việt",
    short_name: "Hán Ngữ+",
    description:
      "Học HSK qua lợi thế Hán-Việt: từ vựng, ngữ pháp, nghe, nói và luyện viết chữ Hán — miễn phí, cá nhân hoá mỗi ngày.",
    start_url: "/",
    display: "standalone",
    background_color: "#f6f1e7",
    theme_color: "#3f6659",
    lang: "vi",
    icons: [
      {
        src: "/favicon.ico",
        sizes: "any",
        type: "image/x-icon",
      },
    ],
  };
}
