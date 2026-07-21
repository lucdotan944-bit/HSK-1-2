# Đưa Hán Ngữ+ lên CH Play và App Store

Checklist thực hiện theo thứ tự. Đã chuẩn bị sẵn: manifest PWA, icon, chính sách bảo
mật (`/privacy`), file xác minh Digital Asset Links (`.well-known/assetlinks.json`,
còn thiếu fingerprint — điền ở Bước 3).

## Giá trị dùng chung

| Trường            | Giá trị                                          |
| ----------------- | ------------------------------------------------- |
| URL web (nguồn)   | `https://hsk-1-2.vercel.app`                       |
| Package name gợi ý | `com.hanngu.plus`                                  |
| Tên hiển thị       | `Hán Ngữ+`                                         |
| Theme color        | `#3f6659`                                          |
| Background color   | `#f6f1e7`                                          |
| Icon               | `https://hsk-1-2.vercel.app/icon-512.png`          |
| URL chính sách bảo mật | `https://hsk-1-2.vercel.app/privacy`           |
| Email hỗ trợ       | `lucdotan944@gmail.com`                            |

## Android — Google Play (làm trước, ít rào cản hơn)

Dùng **PWABuilder.com** (chạy trên cloud, máy không cần cài Android SDK/Java —
quan trọng vì ổ đĩa máy hiện gần hết dung lượng).

1. Vào [pwabuilder.com](https://www.pwabuilder.com), dán `https://hsk-1-2.vercel.app`,
   bấm Start. Công cụ tự đọc `manifest.json` và service worker sẵn có.
2. Chọn tab **Android** → **Generate Package**. Điền:
   - Package ID: `com.hanngu.plus`
   - App name: `Hán Ngữ+`
   - Giữ nguyên theme/background color đã tự nhận diện.
3. Bấm Generate — PWABuilder tự tạo **signing key** (keystore) và file AAB, tải về
   một .zip chứa: file `.aab`, keystore `.jks`/`.keystore`, và **fingerprint SHA-256**
   (trong file `signing-key-info.txt` bên trong zip).
   - ⚠️ **Lưu file keystore + mật khẩu vào nơi an toàn (không phải Downloads/Desktop
     tạm)** — mất file này thì không update được app nữa.
4. Copy chuỗi SHA-256 fingerprint, dán vào
   `web/public/.well-known/assetlinks.json` thay cho
   `REPLACE_WITH_SHA256_FINGERPRINT_FROM_SIGNING_KEY`, commit + push (đổi này *phải*
   lên production để Android xác minh app).
5. Tạo tài khoản [Google Play Console](https://play.google.com/console) — phí một
   lần $25.
6. Tạo app mới → App bundle explorer → upload file `.aab`.
7. Điền store listing:
   - Ảnh chụp màn hình (tối thiểu 2, khuyến nghị 4–8): chụp các trang chủ,
     ôn tập, luyện viết, thi thử trên điện thoại.
   - Icon 512×512: dùng `web/public/icon-512.png` có sẵn.
   - Mô tả ngắn (80 ký tự) + mô tả đầy đủ — nhấn mạnh điểm khác biệt "học qua âm
     Hán-Việt".
   - Privacy Policy URL: `https://hsk-1-2.vercel.app/privacy`
   - Data safety form: khai thu thập email, tiến độ học tập (không chia sẻ bên thứ
     ba, có mã hoá khi truyền tải).
   - Content rating questionnaire: chọn "Education", không có nội dung nhạy cảm.
8. Release qua **Internal testing** trước (mời vài người test), rồi mới **Production**.

## iOS — App Store (làm sau, khó hơn)

Apple từ chối app chỉ là WebView bọc website thuần (Guideline 4.2). App đã có viết
chữ bằng canvas + nhận diện giọng nói — nên nhấn mạnh các tính năng này khi submit.

1. Cần máy Mac + Xcode, hoặc dịch vụ Mac cloud (MacStadium, MacinCloud...) nếu chưa
   có Mac.
2. Đăng ký [Apple Developer Program](https://developer.apple.com/programs/) — $99/năm.
3. Dùng [Capacitor](https://capacitorjs.com) để bọc web app + bổ sung tính năng
   native thật (push notification, share) — không dùng wrapper WebView đơn thuần.
4. Trong Xcode: cấu hình Bundle ID, icon, splash screen (dùng icon 512 có sẵn).
5. App Store Connect:
   - Ảnh chụp màn hình nhiều size thiết bị (6.7", 6.5", 5.5" tối thiểu).
   - **Privacy Nutrition Label**: khai chi tiết data type (Contact Info: email;
     User Content: tiến độ học) — dùng đúng nội dung ở `/privacy`.
   - Privacy Policy URL: `https://hsk-1-2.vercel.app/privacy`
6. Submit **TestFlight** beta trước để tự test, sau đó mới nộp App Store Review
   (thường 1–3 ngày, có thể bị từ chối lần đầu — sửa theo phản hồi và nộp lại).

## Sau khi lên store

- Cập nhật link CH Play / App Store vào trang chủ (nút tải app).
- Theo dõi rating & review sớm để sửa lỗi UX kịp thời.
