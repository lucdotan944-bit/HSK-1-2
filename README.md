# Hán Ngữ+ — HSK 1-2 Learning App

Ứng dụng học tiếng Trung HSK 1-2 cho người Việt.

## Tính năng

- 📚 **268 từ vựng** HSK1 (154) + HSK2 (114) — pinyin, Hán-Việt, nghĩa tiếng Việt
- 🃏 **Flashcard** với spaced repetition (SM-2 algorithm)
- 💬 **9 hội thoại** giao tiếp thực tế — gọi món, hỏi đường, mua sắm, khám bệnh...
- 📝 **22 context notes** — giải thích ngữ pháp bằng tiếng Việt
- 🎯 **Quiz** — chọn nghĩa đúng, kiểm tra kiến thức
- 📊 **Theo dõi tiến độ** — thống kê từ đã học, cần ôn
- 🎨 **10 chủ đề** — gia đình, màu sắc, thời gian, đồ ăn...
- 🔊 **Audio** — phát âm chuẩn qua Web Speech API
- 🔄 **Học theo chủ đề** — chọn theme, học từ theo nhóm
- 📦 **Lesson trọn gói** — học từ → mini-quiz → gợi ý hội thoại liên quan
- ✍️ **Luyện viết chữ Hán** — animation thứ tự nét + tự viết có chấm lỗi (HanziWriter)
- 🎯 **Test xếp trình độ** — 15 câu (~5 phút) gợi ý điểm bắt đầu HSK1/HSK2
- 🔥 **Gamification** — XP, streak ngày học liên tiếp, 10 huy hiệu
- 🎤 **Chấm phát âm** — nói vào mic, so khớp với từ đích (Chrome/Edge)

## Cài đặt & Chạy

```bash
# 1. Clone repo
git clone https://github.com/lucdotan944-bit/HSK-1-2.git
cd HSK-1-2

# 2. Cài dependencies
pip install -r requirements.txt

# 3. Chạy server
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000

# 4. Mở trình duyệt
# http://localhost:8000/
```

## Cấu trúc thư mục

```
├── main.py              # FastAPI server + API endpoints
├── database.py          # SQLite schema (16 tables)
├── seed_data.py         # 268 từ + 9 hội thoại + 22 context notes
├── sm2.py               # SM-2 spaced repetition algorithm
├── gamify.py            # XP, streak, huy hiệu
├── requirements.txt     # Python dependencies
├── .gitignore
└── static/
    ├── index.html       # Frontend SPA
    ├── app.js           # Logic frontend
    ├── style.css        # Responsive CSS
    └── img/             # Theme icons (SVG)
```

## API Endpoints

| Endpoint | Mô tả |
|----------|-------|
| `GET /` | Trang chủ |
| `GET /api/stats` | Thống kê (từ, hội thoại, tiến độ) |
| `GET /api/words/{level}` | Danh sách từ theo HSK level |
| `GET /api/review/{level}` | Từ cần ôn tập theo SM-2 |
| `POST /api/review/{word_id}` | Ghi nhận kết quả ôn tập |
| `GET /api/dialogues` | Danh sách hội thoại |
| `GET /api/dialogues/{id}` | Chi tiết hội thoại (có pinyin) |
| `GET /api/note/{word}` | Context note ngữ pháp |
| `GET /api/themes` | Danh sách chủ đề |
| `GET /api/progress` | Tiến độ học tập |
| `POST /api/quiz` | Gửi kết quả quiz |
| `GET /api/gamify/state` | XP, streak, huy hiệu đã đạt |
| `GET /api/badges` | Danh mục huy hiệu |
| `GET /api/quiz/choices/{level}` | Câu hỏi trắc nghiệm (hỗ trợ `theme_id`, `count`) |
| `POST /api/quiz/theme-result` | Kết quả mini-quiz theo chủ đề |
| `GET /api/themes/{id}/related-dialogues` | Hội thoại chung từ vựng với chủ đề |
| `POST /api/placement/submit` | Nộp bài test xếp trình độ |
| `GET /api/writing/characters` | Ký tự luyện viết + trạng thái |
| `POST /api/writing/complete` | Ghi nhận kết quả luyện viết |
| `POST /api/pronunciation/log` | Log kết quả chấm phát âm |

## Công nghệ

- **Backend**: FastAPI + SQLite + SM-2
- **Frontend**: Vanilla JS + HTML5 + CSS3
- **Audio**: Web Speech API (phát âm tiếng Trung)
- **Database**: SQLite (16 tables)

## Giấy phép

MIT
