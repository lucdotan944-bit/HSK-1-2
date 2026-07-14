// Web Speech API helpers — free, browser-native ASR/TTS (Chrome/Edge).
// No paid pronunciation-assessment API; scoring is a simple hanzi character
// overlap heuristic, same approach as the previous vanilla-JS app.

export function speak(text: string, rate = 0.85) {
  if (typeof window === "undefined" || !window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "zh-CN";
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

export interface SpeechRecognitionLike {
  lang: string;
  interimResults: boolean;
  maxAlternatives: number;
  onresult: ((e: { results: { [i: number]: { [j: number]: { transcript: string } } } }) => void) | null;
  onerror: ((e: { error: string }) => void) | null;
  onend: (() => void) | null;
  start: () => void;
}
