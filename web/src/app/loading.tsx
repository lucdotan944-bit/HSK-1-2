export default function Loading() {
  return (
    <div className="flex flex-col items-center gap-3 py-24 text-center">
      <div className="h-10 w-10 animate-spin rounded-full border-2 border-line border-t-jade" />
      <p className="text-sm text-ink-soft">Đang tải...</p>
    </div>
  );
}
