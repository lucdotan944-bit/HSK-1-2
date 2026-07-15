"use client";

import { Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import MicCheck from "@/components/MicCheck";

function MicCheckInner() {
  const router = useRouter();
  const params = useSearchParams();
  const next = params.get("next") || "/";

  return (
    <div className="mx-auto max-w-md space-y-4">
      <MicCheck onFinished={() => router.push(next)} />
    </div>
  );
}

export default function MicCheckPage() {
  return (
    <Suspense>
      <MicCheckInner />
    </Suspense>
  );
}
