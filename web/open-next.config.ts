// Cấu hình OpenNext cho Cloudflare — mặc định là đủ cho app này
// (không dùng ISR/cache đặc biệt; trang động render trong Worker).
import { defineCloudflareConfig } from "@opennextjs/cloudflare";

export default defineCloudflareConfig();
