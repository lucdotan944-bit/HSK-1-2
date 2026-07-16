import Link from "next/link";
import { Card, Button, SectionTitle } from "@/components/ui";
import SealStamp from "@/components/SealStamp";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center py-12 text-center">
      <SealStamp size={64}>迷</SealStamp>
      <div className="mt-6">
        <SectionTitle sub="Trang bạn tìm không tồn tại, hoặc đã được chuyển đi nơi khác.">
          Không tìm thấy trang
        </SectionTitle>
      </div>
      <Card className="max-w-sm">
        <p className="text-sm text-ink-soft">
          Kiểm tra lại đường dẫn, hoặc quay về Trang chủ để tiếp tục học.
        </p>
      </Card>
      <Link href="/" className="mt-6">
        <Button variant="primary">Về Trang chủ</Button>
      </Link>
    </div>
  );
}
