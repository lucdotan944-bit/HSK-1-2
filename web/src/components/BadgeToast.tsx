"use client";

import { useEffect, useState } from "react";
import { api, type Badge } from "@/lib/api";

export function useBadgeToast() {
  const [queue, setQueue] = useState<string[]>([]);
  const [catalog, setCatalog] = useState<Record<string, Badge> | null>(null);

  useEffect(() => {
    if (queue.length && !catalog) {
      api.badges().then(
        (r) => {
          const map: Record<string, Badge> = {};
          r.badges.forEach((b) => (map[b.badge_id] = b));
          setCatalog(map);
        },
        () => {
          // Falls back to raw badge id + generic icon in the toast below; not worth retrying per-announce.
          setCatalog({});
        }
      );
    }
  }, [queue.length, catalog]);

  function announce(badgeIds: string[] | undefined) {
    if (!badgeIds || !badgeIds.length) return;
    setQueue((q) => [...q, ...badgeIds]);
    setTimeout(() => setQueue((q) => q.filter((id) => !badgeIds.includes(id))), 3200);
  }

  const node =
    queue.length > 0 ? (
      <div className="pointer-events-none fixed inset-x-0 top-4 z-50 flex flex-col items-center gap-2">
        {queue.map((id, i) => {
          const b = catalog?.[id];
          return (
            <div
              key={`${id}-${i}`}
              className="pointer-events-auto flex items-center gap-2 rounded-full border border-brass bg-brass-soft px-4 py-2 text-sm font-semibold shadow-lg"
            >
              <span className="text-lg">{b?.icon ?? "🏅"}</span>
              Đạt huy hiệu: {b?.name ?? id}
            </div>
          );
        })}
      </div>
    ) : null;

  return { announce, toastNode: node };
}
