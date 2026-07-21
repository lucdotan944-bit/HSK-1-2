// Service worker của Hán Ngữ+ — cache offline có chọn lọc.
//
// Nguyên tắc: KHÔNG cache dữ liệu cá nhân (tiến độ, XP, auth) — chỉ cache
// nội dung giáo trình bất biến và asset tĩnh, để mở lại app khi mất mạng vẫn
// xem được từ vựng/ngữ pháp/bài học đã mở.
const CACHE_VERSION = "hanngu-v1";
const RUNTIME_CACHE = `${CACHE_VERSION}-runtime`;

// API dữ liệu giáo trình (giống nhau cho mọi user) — stale-while-revalidate.
const CACHEABLE_API = [
  /^\/api\/words\//,
  /^\/api\/grammar/,
  /^\/api\/dialogues/,
  /^\/api\/sentence\//,
  /^\/api\/note\//,
  /^\/api\/hsk-mapping/,
  /^\/api\/conversation\//,
  /^\/api\/tts\?/,
];

// Dữ liệu nét chữ HanziWriter tải từ jsdelivr — cache để luyện viết offline.
const HANZI_DATA_HOST = "cdn.jsdelivr.net";

self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => !k.startsWith(CACHE_VERSION)).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

function staleWhileRevalidate(request) {
  return caches.open(RUNTIME_CACHE).then((cache) =>
    cache.match(request).then((cached) => {
      const network = fetch(request)
        .then((response) => {
          if (response.ok) cache.put(request, response.clone());
          return response;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
}

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET") return;

  // Asset build của Next (đã hash tên) + font — cache-first, bất biến.
  if (url.origin === self.location.origin && url.pathname.startsWith("/_next/static/")) {
    event.respondWith(
      caches.open(RUNTIME_CACHE).then((cache) =>
        cache.match(event.request).then(
          (cached) =>
            cached ||
            fetch(event.request).then((response) => {
              if (response.ok) cache.put(event.request, response.clone());
              return response;
            })
        )
      )
    );
    return;
  }

  // Dữ liệu giáo trình + TTS — stale-while-revalidate.
  if (
    url.origin === self.location.origin &&
    CACHEABLE_API.some((re) => re.test(url.pathname + url.search))
  ) {
    event.respondWith(staleWhileRevalidate(event.request));
    return;
  }

  // Dữ liệu nét chữ HanziWriter (CORS, cache được).
  if (url.host === HANZI_DATA_HOST) {
    event.respondWith(staleWhileRevalidate(event.request));
    return;
  }

  // Điều hướng trang: mạng trước, rơi về cache khi offline.
  if (event.request.mode === "navigate") {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const copy = response.clone();
          caches.open(RUNTIME_CACHE).then((cache) => cache.put(event.request, copy));
          return response;
        })
        .catch(() =>
          caches.match(event.request).then((cached) => cached || caches.match("/"))
        )
    );
  }
});
