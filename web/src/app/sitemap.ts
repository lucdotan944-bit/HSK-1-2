import type { MetadataRoute } from "next";

const BASE_URL = "https://hsk-1-2.vercel.app";

export default function sitemap(): MetadataRoute.Sitemap {
  const staticRoutes = [
    { path: "/", priority: 1 },
    { path: "/daily", priority: 0.8 },
    { path: "/review", priority: 0.8 },
    { path: "/words", priority: 0.7 },
    { path: "/grammar", priority: 0.7 },
    { path: "/dialogues", priority: 0.7 },
    { path: "/writing", priority: 0.6 },
    { path: "/exam", priority: 0.6 },
    { path: "/placement", priority: 0.5 },
    { path: "/progress", priority: 0.4 },
  ];

  const examLevels = Array.from({ length: 9 }, (_, i) => ({
    path: `/exam/${i + 1}`,
    priority: 0.4,
  }));

  return [...staticRoutes, ...examLevels].map((r) => ({
    url: `${BASE_URL}${r.path}`,
    lastModified: new Date(),
    priority: r.priority,
  }));
}
