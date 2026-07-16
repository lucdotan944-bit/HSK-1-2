"use client";

export default function GlobalError({
  unstable_retry,
}: {
  error: Error & { digest?: string };
  unstable_retry: () => void;
}) {
  return (
    <html lang="vi">
      <body
        style={{
          display: "flex",
          minHeight: "100vh",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          textAlign: "center",
          fontFamily: "system-ui, sans-serif",
          padding: "2rem",
        }}
      >
        <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "0.5rem" }}>
          Ứng dụng gặp sự cố
        </h2>
        <p style={{ color: "#666", marginBottom: "1.5rem" }}>
          Vui lòng thử lại. Nếu vẫn lỗi, hãy tải lại trang.
        </p>
        <button
          onClick={() => unstable_retry()}
          style={{
            borderRadius: "9999px",
            padding: "0.625rem 1.25rem",
            fontWeight: 600,
            background: "#b23a2e",
            color: "white",
          }}
        >
          Thử lại
        </button>
      </body>
    </html>
  );
}
