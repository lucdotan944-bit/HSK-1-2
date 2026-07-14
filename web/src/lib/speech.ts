// Web Speech API helpers — free, browser-native ASR/TTS (Chrome/Edge).
// No paid pronunciation-assessment API; scoring is a simple hanzi character
// overlap heuristic, same approach as the previous vanilla-JS app.

// Voice names known to speak standard Putonghua (Beijing/Mainland accent),
// checked in priority order against whatever zh-CN voices the OS/browser exposes.
const PREFERRED_MANDARIN_VOICE_NAMES = [
  "Tingting", // macOS
  "Xiaoxiao", // Edge neural
  "Yaoyao", // Windows
  "Huihui", // Windows
  "Google 普通话（中国大陆）", // Chrome
];

let voiceCache: SpeechSynthesisVoice[] = [];

function loadVoices(): SpeechSynthesisVoice[] {
  if (typeof window === "undefined" || !window.speechSynthesis) return [];
  const voices = window.speechSynthesis.getVoices();
  if (voices.length) voiceCache = voices;
  return voiceCache;
}

if (typeof window !== "undefined" && window.speechSynthesis) {
  loadVoices();
  window.speechSynthesis.onvoiceschanged = loadVoices;
}

// Mainland zh-CN only — excludes zh-TW/zh-HK, which use a different accent.
function pickMandarinVoice(): SpeechSynthesisVoice | undefined {
  const zhCN = loadVoices().filter((v) => v.lang.toLowerCase() === "zh-cn");
  if (zhCN.length === 0) return undefined;
  for (const name of PREFERRED_MANDARIN_VOICE_NAMES) {
    const match = zhCN.find((v) => v.name.includes(name));
    if (match) return match;
  }
  return zhCN[0];
}

export function speak(text: string, rate = 0.85) {
  if (typeof window === "undefined" || !window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "zh-CN";
  const voice = pickMandarinVoice();
  if (voice) u.voice = voice;
  u.rate = rate;
  u.pitch = 1.0;
  window.speechSynthesis.speak(u);
}

export type PronScore = "ok" | "warn" | "fail";

export function scorePronunciation(target: string, recognized: string): PronScore {
  const t = (target.match(/[一-鿿]/g) || []).join("");
  const r = (recognized.match(/[一-鿿]/g) || []).join("");
  if (t === r) return "ok";
  if (t.length === 0) return "fail";
  const rChars = r.split("");
  let overlap = 0;
  for (const ch of t) {
    const i = rChars.indexOf(ch);
    if (i >= 0) {
      overlap++;
      rChars.splice(i, 1);
    }
  }
  return overlap / t.length >= 0.6 ? "warn" : "fail";
}

export function getSpeechRecognition(): (new () => SpeechRecognitionLike) | null {
  if (typeof window === "undefined") return null;
  const w = window as unknown as {
    SpeechRecognition?: new () => SpeechRecognitionLike;
    webkitSpeechRecognition?: new () => SpeechRecognitionLike;
  };
  return w.SpeechRecognition || w.webkitSpeechRecognition || null;
}

// SpeechRecognition sends audio to the browser vendor's ASR service (e.g. Google for
// Chrome) — it needs internet access even though the mic itself is local. Map its
// error codes to actionable Vietnamese messages instead of a generic "mic error".
export function describeSpeechError(code: string): string {
  switch (code) {
    case "no-speech":
      return "Không nghe thấy gì, thử lại.";
    case "not-allowed":
    case "permission-denied":
      return "Trình duyệt chưa được cấp quyền micro. Bấm vào biểu tượng khóa/micro trên thanh địa chỉ để cho phép, rồi thử lại.";
    case "audio-capture":
      return "Không tìm thấy micro, hoặc micro đang được ứng dụng khác sử dụng.";
    case "network":
      return "Lỗi mạng: tính năng nhận diện giọng nói cần gửi âm thanh tới máy chủ của Google qua internet. Nguyên nhân thường gặp nhất: đang dùng trình duyệt Brave (tắt Shields cho trang này), có extension chặn quảng cáo/riêng tư (uBlock, Privacy Badger...), hoặc đang bật VPN/proxy. Hãy tắt các thứ trên rồi thử lại.";
    case "service-not-allowed":
      return "Trình duyệt hoặc quản trị hệ thống đã tắt tính năng nhận diện giọng nói.";
    case "aborted":
      return "Đã hủy ghi âm, thử lại.";
    default:
      return `Lỗi micro (${code}). Thử lại hoặc đổi sang Chrome mới nhất.`;
  }
}

export interface SpeechRecognitionLike {
  lang: string;
  interimResults: boolean;
  maxAlternatives: number;
  onresult: ((e: { results: { [i: number]: { [j: number]: { transcript: string } } } }) => void) | null;
  onerror: ((e: { error: string }) => void) | null;
  onend: (() => void) | null;
  start: () => void;
}

export class SpeechRecognitionError extends Error {
  constructor(public code: string) {
    super(code);
  }
}

/**
 * Runs one recognition pass and resolves with the transcript. "network" errors
 * (the most common failure — the browser's ASR call to Google's servers glitching)
 * are retried a couple of times with a short backoff before giving up.
 */
export function listenOnce(lang = "zh-CN", { networkRetries = 2 }: { networkRetries?: number } = {}): Promise<string> {
  const Rec = getSpeechRecognition();
  if (!Rec) return Promise.reject(new SpeechRecognitionError("not-supported"));

  return new Promise((resolve, reject) => {
    let retriesLeft = networkRetries;

    function attempt() {
      const rec = new Rec!();
      rec.lang = lang;
      rec.interimResults = false;
      rec.maxAlternatives = 1;
      rec.onresult = (e) => resolve(e.results[0][0].transcript);
      rec.onerror = (e) => {
        if (e.error === "network" && retriesLeft > 0) {
          retriesLeft--;
          setTimeout(attempt, 600);
          return;
        }
        reject(new SpeechRecognitionError(e.error));
      };
      rec.start();
    }
    attempt();
  });
}

// A few short, common HSK1 words used to sanity-check the mic + recognizer.
export const MIC_CHECK_PHRASES = [
  { simplified: "你好", pinyin: "nǐ hǎo" },
  { simplified: "谢谢", pinyin: "xièxie" },
  { simplified: "老师", pinyin: "lǎoshī" },
  { simplified: "再见", pinyin: "zàijiàn" },
];

/** Opens the mic and wires up a live 0–1 volume level via an AnalyserNode. */
export async function openMicLevelMeter(onLevel: (level: number) => void) {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
  const ctx = new AudioCtx();
  const source = ctx.createMediaStreamSource(stream);
  const analyser = ctx.createAnalyser();
  analyser.fftSize = 512;
  source.connect(analyser);
  const data = new Uint8Array(analyser.frequencyBinCount);

  let raf = 0;
  function tick() {
    analyser.getByteTimeDomainData(data);
    let sumSquares = 0;
    for (let i = 0; i < data.length; i++) {
      const v = (data[i] - 128) / 128;
      sumSquares += v * v;
    }
    const rms = Math.sqrt(sumSquares / data.length);
    onLevel(Math.min(1, rms * 4));
    raf = requestAnimationFrame(tick);
  }
  tick();

  return function close() {
    cancelAnimationFrame(raf);
    stream.getTracks().forEach((t) => t.stop());
    ctx.close();
  };
}
