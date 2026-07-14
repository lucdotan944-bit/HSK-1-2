# Hán Ngữ+ — Học tiếng Trung cho người Việt

Ứng dụng học tiếng Trung theo chuẩn HSK, khai thác lợi thế Hán-Việt cho người Việt. Miễn phí, không dùng API trả phí (không Azure/iFlytek/LLM) — mọi tính năng "cá nhân hoá" và "chấm điểm" chạy bằng logic rule-based trên dữ liệu tự có.

## Kiến trúc

- **Backend**: FastAPI + SQLite (`main.py`, `database.py`, `seed_data.py`, `sm2.py`, `gamify.py`, `hsk_mapping.py`, `conversations.py`) — giữ nguyên từ bản gốc, mở rộng thêm 4 endpoint mới.
- **Frontend**: Next.js 16 (App Router) + TypeScript + Tailwind CSS v4, trong thư mục [`web/`](web/) — thay thế hoàn toàn frontend vanilla JS cũ (`static/`, không còn dùng nữa).
- Next.js gọi backend qua rewrite `/api/*` → FastAPI (xem `web/next.config.ts`), nên không cần CORS ở trình duyệt.

## Tính năng

- 📚 268 từ vựng HSK1+HSK2 — pinyin, Hán-Việt, nghĩa tiếng Việt
- 🃏 Flashcard với spaced repetition (SM-2)
- 💬 9 hội thoại giao tiếp thực tế + 3 kịch bản hội thoại phân nhánh tương tác (order_food, ask_direction, shopping)
- 🎯 Test xếp trình độ, quiz theo chủ đề, quy đổi HSK cũ ↔ HSK 3.0
- ✍️ Luyện viết chữ Hán (HanziWriter)
- 🎤 Chấm phát âm qua Web Speech API (miễn phí, browser-native)
- 🔥 Gamification: XP, streak, huy hiệu
- 📊 Bản đồ kỹ năng (Từ vựng/Ngữ pháp/Nghe/Nói) tính từ lịch sử luyện tập, không dùng AI ngoài
- ⏱️ Phiên học 5 phút/ngày cá nhân hoá: ghép ôn từ + nghe + nói + hội thoại, ưu tiên kỹ năng yếu nhất

## Chạy dự án (development)

Cần 2 tiến trình chạy song song:

```bash
# 1. Backend — FastAPI (port 8000)
pip install -r requirements.txt
python3 -m uvicorn main:app --port 8000

# 2. Frontend — Next.js (port 3000), ở thư mục web/
cd web
npm install
npm run dev
```

Mở http://localhost:3000

## Build production

```bash
cd web
npm run build
npm start   # phục vụ trên port 3000, vẫn cần backend FastAPI chạy song song trên 8000
```

Đặt biến môi trường `API_ORIGIN` nếu backend không chạy ở `http://127.0.0.1:8000` (xem `web/next.config.ts`).

## Cấu trúc thư mục

```
├── main.py              # FastAPI server + API endpoints
├── database.py          # SQLite schema (16 tables)
├── seed_data.py         # 268 từ + 9 hội thoại + 22 context notes
├── sm2.py               # SM-2 spaced repetition algorithm
├── gamify.py            # XP, streak, huy hiệu
├── hsk_mapping.py        # Bảng quy đổi HSK cũ ↔ HSK 3.0
├── conversations.py      # Kịch bản hội thoại phân nhánh
├── requirements.txt
├── static/               # (cũ, không còn dùng — giữ lại tham khảo)
└── web/                  # Frontend Next.js
    ├── src/app/          # Route pages (App Router)
    ├── src/components/   # AppShell, SealStamp, ui.tsx, PronunciationButton, SkillRadar...
    └── src/lib/          # api.ts (typed client), speech.ts (Web Speech API helpers)
```

## API Endpoints

| Endpoint | Mô tả |
|----------|-------|
| `GET /api/stats` | Thống kê (từ, hội thoại, tiến độ) |
| `GET /api/words/{level}` | Danh sách từ theo HSK level |
| `GET /api/review/{level}` | Từ cần ôn tập theo SM-2 |
| `POST /api/review` | Ghi nhận kết quả ôn tập |
| `GET /api/dialogues`, `GET /api/dialogues/{id}` | Hội thoại |
| `GET /api/note/{word}` | Context note ngữ pháp |
| `GET /api/themes`, `GET /api/themes/{id}` | Chủ đề học |
| `POST /api/themes/{id}/learn/{word_id}` | Đánh dấu đã học từ trong chủ đề |
| `GET /api/themes/{id}/related-dialogues` | Hội thoại liên quan tới chủ đề |
| `GET /api/progress` | Tiến độ học tập |
| `GET /api/quiz/choices/{level}` | Câu hỏi trắc nghiệm |
| `POST /api/quiz`, `POST /api/quiz/theme-result` | Nộp kết quả quiz |
| `POST /api/placement/submit` | Nộp bài test xếp trình độ |
| `GET /api/gamify/state`, `GET /api/badges` | XP, streak, huy hiệu |
| `GET /api/writing/characters`, `POST /api/writing/complete` | Luyện viết chữ |
| `POST /api/pronunciation/log` | Log kết quả chấm phát âm |
| `GET /api/skills/breakdown` | Bản đồ kỹ năng 4 nhóm (rule-based) |
| `GET /api/daily-session` | Lắp ráp phiên học 5 phút/ngày |
| `GET /api/conversation/{scenario_id}`, `POST /api/conversation/{scenario_id}/respond` | Hội thoại phân nhánh |
| `GET /api/hsk-mapping` | Bảng quy đổi HSK cũ ↔ HSK 3.0 |

## Công nghệ

- **Backend**: FastAPI + SQLite + SM-2, logic rule-based (không LLM/API trả phí)
- **Frontend**: Next.js 16 (App Router) + TypeScript + Tailwind CSS v4
- **Audio**: Web Speech API (nhận diện + phát âm tiếng Trung, miễn phí)
- **Viết chữ**: HanziWriter (CDN)
- **Database**: SQLite (16 tables)

## Giấy phép

MIT
