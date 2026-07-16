"use client";

import { useEffect } from "react";
import Link from "next/link";
import { Card, Button, SectionTitle } from "@/components/ui";
import SealStamp from "@/components/SealStamp";

export default function Error({
  error,
  unstable_retry,
}: {
  error: Error & { digest?: string };
  unstable_retry: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="flex flex-col items-center py-12 text-center">
      <SealStamp size={64}>误</SealStamp>
      <div className="mt-6">
        <SectionTitle sub="Đã có lỗi xảy ra khi tải trang này. Bạn có thể thử lại hoặc quay về Trang chủ.">
          Có lỗi xảy ra
        </SectionTitle>
      </div>
      <Card className="max-w-sm">
        <p className="text-sm text-ink-soft">
          Nếu lỗi này lặp lại, hãy thử tải lại trang sau ít phút.
        </p>
      </Card>
      <div className="mt-6 flex gap-3">
        <Button variant="primary" onClick={() => unstable_retry()}>
          Thử lại
        </Button>
        <Link href="/">
          <Button variant="ghost">Về Trang chủ</Button>
        </Link>
      </div>
    </div>
  );
}
