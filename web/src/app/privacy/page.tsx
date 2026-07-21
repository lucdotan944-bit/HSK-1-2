import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Chính sách bảo mật",
  description: "Chính sách bảo mật và quyền riêng tư của Hán Ngữ+.",
};

export default function PrivacyPage() {
  return (
    <div className="mx-auto max-w-2xl space-y-6 text-sm leading-relaxed">
      <div>
        <h1 className="font-display text-2xl font-bold">Chính sách bảo mật</h1>
        <p className="mt-1 text-ink-soft">Cập nhật lần cuối: 21/07/2026</p>
      </div>

      <p>
        Hán Ngữ+ (&quot;chúng tôi&quot;) tôn trọng quyền riêng tư của người dùng. Trang này giải
        thích chúng tôi thu thập, sử dụng và bảo vệ dữ liệu nào khi bạn dùng ứng dụng học tiếng
        Trung Hán Ngữ+ (website, ứng dụng web tiến bộ và bản đóng gói trên CH Play/App Store nếu
        có).
      </p>

      <section className="space-y-2">
        <h2 className="font-display text-lg font-semibold">1. Dữ liệu chúng tôi thu thập</h2>
        <ul className="list-inside list-disc space-y-1.5">
          <li>
            <b>Thông tin tài khoản:</b> địa chỉ email và mật khẩu (đã băm, không lưu dạng chữ
            thường) nếu bạn đăng ký bằng email; hoặc email, tên hiển thị và mã định danh Google
            nếu bạn đăng nhập bằng Google. Chúng tôi không bao giờ nhìn thấy hay lưu mật khẩu
            Google của bạn.
          </li>
          <li>
            <b>Dữ liệu học tập:</b> tiến độ ôn tập (spaced repetition), điểm kinh nghiệm, streak,
            kết quả quiz/thi thử, lượt luyện viết chữ, huy hiệu đã đạt — để cá nhân hoá lộ trình
            học và hiển thị thống kê cho bạn.
          </li>
          <li>
            <b>Dữ liệu kỹ thuật tối thiểu:</b> cookie phiên đăng nhập (để giữ bạn đăng nhập), và
            với người dùng chưa đăng ký, một mã khách ẩn danh lưu trên trình duyệt để lưu tạm tiến
            độ.
          </li>
        </ul>
      </section>

      <section className="space-y-2">
        <h2 className="font-display text-lg font-semibold">2. Cách chúng tôi sử dụng dữ liệu</h2>
        <p>
          Dữ liệu chỉ được dùng để vận hành và cải thiện trải nghiệm học tập: cá nhân hoá lịch ôn
          tập, hiển thị tiến độ, phân tích lỗi sai để gợi ý ôn lại. Chúng tôi{" "}
          <b>không bán, không cho thuê và không chia sẻ dữ liệu cá nhân</b> của bạn cho bên thứ ba
          vì mục đích quảng cáo.
        </p>
      </section>

      <section className="space-y-2">
        <h2 className="font-display text-lg font-semibold">3. Dịch vụ bên thứ ba</h2>
        <ul className="list-inside list-disc space-y-1.5">
          <li>
            <b>Google Sign-In</b> (tuỳ chọn): dùng để xác thực nếu bạn chọn đăng nhập bằng Google.
            Xem thêm{" "}
            <a
              className="text-jade underline"
              href="https://policies.google.com/privacy"
              target="_blank"
              rel="noreferrer"
            >
              chính sách bảo mật của Google
            </a>
            .
          </li>
          <li>
            <b>Hạ tầng lưu trữ và vận hành:</b> dữ liệu được lưu trữ trên máy chủ của Render; giao
            diện web được phân phối qua Vercel và Cloudflare.
          </li>
        </ul>
      </section>

      <section className="space-y-2">
        <h2 className="font-display text-lg font-semibold">4. Lưu trữ và xoá dữ liệu</h2>
        <p>
          Dữ liệu được lưu trong suốt thời gian bạn sử dụng tài khoản. Bạn có thể yêu cầu xoá toàn
          bộ dữ liệu cá nhân bất kỳ lúc nào bằng cách gửi email theo địa chỉ ở mục 6 — chúng tôi sẽ
          xử lý trong vòng 30 ngày.
        </p>
      </section>

      <section className="space-y-2">
        <h2 className="font-display text-lg font-semibold">5. Trẻ em</h2>
        <p>
          Hán Ngữ+ phù hợp cho mọi lứa tuổi học tiếng Trung. Chúng tôi không cố ý thu thập nhiều
          hơn thông tin cần thiết để vận hành tài khoản, và không hiển thị quảng cáo nhắm mục tiêu
          theo hành vi.
        </p>
      </section>

      <section className="space-y-2">
        <h2 className="font-display text-lg font-semibold">6. Liên hệ</h2>
        <p>
          Mọi câu hỏi về quyền riêng tư, vui lòng liên hệ:{" "}
          <a className="text-jade underline" href="mailto:lucdotan944@gmail.com">
            lucdotan944@gmail.com
          </a>
        </p>
      </section>
    </div>
  );
}
