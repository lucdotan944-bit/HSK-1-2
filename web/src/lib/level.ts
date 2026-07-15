"use client";

// Preferred HSK level (1-9), shared across the whole app via localStorage —
// selecting a level on the homepage keeps Words/Review/Writing in sync, and
// vice versa. A same-tab CustomEvent covers what the native `storage` event
// misses (it only fires in *other* tabs).
import { useCallback, useEffect, useState } from "react";

const KEY = "hanngu:preferred-level";
const EVENT = "hanngu:preferred-level-change";

export function getPreferredLevel(fallback = 1): number {
  if (typeof window === "undefined") return fallback;
  const v = Number(window.localStorage.getItem(KEY));
  return v >= 1 && v <= 9 ? v : fallback;
}

export function setPreferredLevel(level: number) {
  window.localStorage.setItem(KEY, String(level));
  window.dispatchEvent(new CustomEvent<number>(EVENT, { detail: level }));
}

export function usePreferredLevel(fallback = 1) {
  const [level, setLevel] = useState(fallback);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- hydrate from localStorage after mount (SSR has no access to it)
    setLevel(getPreferredLevel(fallback));
    const handler = (e: Event) => setLevel((e as CustomEvent<number>).detail);
    window.addEventListener(EVENT, handler);
    return () => window.removeEventListener(EVENT, handler);
    // eslint-disable-next-line react-hooks/exhaustive-deps -- fallback only used on mount
  }, []);

  const update = useCallback((next: number) => setPreferredLevel(next), []);

  return [level, update] as const;
}
