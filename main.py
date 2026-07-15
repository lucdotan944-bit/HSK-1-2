import json
import os
import random
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from database import get_db, init_db
from sm2 import sm2
import gamify
import tts
from seed_data import get_words, get_hsk1, get_hsk2, get_sentence, get_sino_viet, get_context_note, get_dialogues, THEMES, get_theme_words, auto_categorize_theme_words, BADGES
from hsk_mapping import HSK_MAPPING
from conversations import CONVERSATIONS

app = FastAPI(title="Hán Ngữ+ - Học tiếng Trung HSK")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup():
    init_db()
    seed_words()
    seed_themes()
    seed_dialogues()
    seed_user_state()

def seed_user_state():
    conn = get_db()
    conn.execute("INSERT OR IGNORE INTO user_state (id) VALUES (1)")
    conn.commit()
    conn.close()

def seed_words():
    """Idempotent + incremental: inserts only words not already present (by
    simplified text), so re-running after the vocab set grows (e.g. HSK1-2 ->
    HSK1-9) tops up an existing DB instead of requiring a wipe, and doesn't
    touch existing rows' user_words/SM-2 progress."""
    conn = get_db()
    existing = {r["simplified"] for r in conn.execute("SELECT simplified FROM words").fetchall()}

    words = get_words()
    new_words = [w for w in words if w[0] not in existing]
    if new_words:
        conn.executemany(
            "INSERT INTO words (simplified, pinyin, meanings, hsk_level, radical) VALUES (?, ?, ?, ?, ?)",
            new_words
        )
        conn.commit()

    # Backfill sino_viet for any word missing it (new rows, or older rows seeded
    # before this word had a mapping).
    for w in conn.execute("SELECT id, simplified FROM words WHERE sino_viet IS NULL OR sino_viet = ''").fetchall():
        sv = get_sino_viet(w["simplified"])
        if sv:
            conn.execute("UPDATE words SET sino_viet=? WHERE id=?", (sv, w["id"]))
    conn.commit()

    # Auto-add to user_words for any word missing a review-state row.
    for w in conn.execute("SELECT id FROM words").fetchall():
        conn.execute(
            "INSERT OR IGNORE INTO user_words (word_id) VALUES (?)",
            (w[0],)
        )
    conn.commit()
    conn.close()
    if new_words:
        print(f"Seeded {len(new_words)} new words ({len(words)} total in vocab source)")

def seed_themes():
    """Idempotent + incremental like seed_words(): always tops up new theme
    metadata and hand-curated word links (INSERT OR IGNORE / existence
    check), then runs auto_categorize_theme_words() to keyword-tag HSK 3-9
    words that have no hand-curated list. Safe to re-run every startup."""
    conn = get_db()
    for tid, t in THEMES.items():
        conn.execute(
            "INSERT OR IGNORE INTO themes (id, name, icon, description) VALUES (?, ?, ?, ?)",
            (tid, t["name"], t["icon"], t["desc"])
        )
        for i, w_simplified in enumerate(t["words"]):
            row = conn.execute(
                "SELECT id FROM words WHERE simplified=?", (w_simplified,)
            ).fetchone()
            if row:
                already = conn.execute(
                    "SELECT 1 FROM theme_words WHERE theme_id=? AND word_id=?", (tid, row["id"])
                ).fetchone()
                if not already:
                    conn.execute(
                        "INSERT INTO theme_words (theme_id, word_id, sort_order) VALUES (?, ?, ?)",
                        (tid, row["id"], i)
                    )
    conn.commit()
    auto_categorize_theme_words(conn)
    conn.close()
    print(f"Seeded {len(THEMES)} themes")

def seed_dialogues():
    """Idempotent + incremental like seed_words()/seed_themes(): only inserts
    dialogues not already present, so adding new ones (e.g. HSK1-2 -> HSK1-9)
    tops up an existing DB instead of requiring a wipe."""
    conn = get_db()
    import re
    existing_ids = {r["id"] for r in conn.execute("SELECT id FROM dialogues").fetchall()}
    dialogues = get_dialogues()
    new_ids = [did for did in dialogues if did not in existing_ids]
    for did in new_ids:
        d = dialogues[did]
        conn.execute(
            "INSERT INTO dialogues (id, title, context, hsk_level) VALUES (?, ?, ?, ?)",
            (did, d["title"], d["context"], d.get("hsk_level", 1))
        )
        for i, line in enumerate(d["lines"]):
            speaker, cn, pinyin, vi = line
            conn.execute(
                "INSERT INTO dialogue_lines (dialogue_id, speaker, simplified, pinyin, vietnamese, sort_order) VALUES (?, ?, ?, ?, ?, ?)",
                (did, speaker, cn, pinyin, vi, i)
            )
            # Link words
            for char_word in re.findall(r'[\u4e00-\u9fff]+', cn):
                row = conn.execute("SELECT id FROM words WHERE simplified=?", (char_word,)).fetchone()
                if row:
                    conn.execute(
                        "INSERT OR IGNORE INTO dialogue_words (dialogue_id, word_id) VALUES (?, ?)",
                        (did, row["id"])
                    )
    conn.commit()
    conn.close()
    if new_ids:
        print(f"Seeded {len(new_ids)} new dialogues ({len(dialogues)} total)")

# ---- API Routes ----

@app.get("/api/gamify/state")
def get_gamify_state():
    conn = get_db()
    state = conn.execute("SELECT * FROM user_state WHERE id=1").fetchone()
    earned = conn.execute("SELECT badge_id, earned_at FROM badges_earned").fetchall()
    conn.close()
    badges = []
    for b in earned:
        meta = BADGES.get(b["badge_id"], {})
        badges.append({
            "badge_id": b["badge_id"],
            "name": meta.get("name", b["badge_id"]),
            "icon": meta.get("icon", "🏅"),
            "desc": meta.get("desc", ""),
            "earned_at": b["earned_at"],
        })
    return {
        "xp": state["xp"],
        "current_streak": state["current_streak"],
        "longest_streak": state["longest_streak"],
        "placement_level": state["placement_level"],
        "badges": badges,
    }

@app.get("/api/badges")
def list_badges():
    conn = get_db()
    earned = {r["badge_id"] for r in conn.execute("SELECT badge_id FROM badges_earned").fetchall()}
    conn.close()
    return {"badges": [
        {"badge_id": bid, "name": b["name"], "icon": b["icon"], "desc": b["desc"],
         "earned": bid in earned}
        for bid, b in BADGES.items()
    ]}

@app.get("/api/stats")
def get_stats():
    conn = get_db()

    # Total + due words per HSK level (1-9)
    level_rows = conn.execute("""
        SELECT w.hsk_level as level, COUNT(*) as total,
               SUM(CASE WHEN uw.next_review <= datetime('now') THEN 1 ELSE 0 END) as due
        FROM words w JOIN user_words uw ON uw.word_id = w.id
        GROUP BY w.hsk_level ORDER BY w.hsk_level
    """).fetchall()
    by_level = [{"level": r["level"], "total": r["total"], "due": r["due"] or 0} for r in level_rows]
    by_level_map = {r["level"]: r for r in by_level}
    hsk1 = by_level_map.get(1, {}).get("total", 0)
    hsk2 = by_level_map.get(2, {}).get("total", 0)
    due_hsk1 = by_level_map.get(1, {}).get("due", 0)
    due_hsk2 = by_level_map.get(2, {}).get("due", 0)

    # Review stats
    due = conn.execute("SELECT COUNT(*) FROM user_words WHERE next_review <= datetime('now')").fetchone()[0]
    total = conn.execute("SELECT COUNT(*) FROM user_words").fetchone()[0]
    learned = conn.execute("SELECT COUNT(*) FROM user_words WHERE repetitions >= 5").fetchone()[0]

    dlg_count = conn.execute("SELECT COUNT(*) FROM dialogues").fetchone()[0]

    conn.close()
    return {
        "hsk1": hsk1, "hsk2": hsk2,
        "due": due, "total": total, "learned": learned,
        "due_hsk1": due_hsk1, "due_hsk2": due_hsk2,
        "dialogues": dlg_count,
        "by_level": by_level,
    }

@app.get("/api/review/{hsk_level}")
def get_review_words(hsk_level: int, limit: int = 20):
    conn = get_db()
    rows = conn.execute("""
        SELECT w.id, w.simplified, w.pinyin, w.meanings, w.hsk_level, w.radical, w.sino_viet,
               uw.repetitions, uw.easiness, uw.next_review
        FROM words w
        JOIN user_words uw ON w.id = uw.word_id
        WHERE w.hsk_level <= ? AND uw.next_review <= datetime('now')
        ORDER BY uw.next_review ASC, uw.repetitions ASC
        LIMIT ?
    """, (hsk_level, limit)).fetchall()
    conn.close()
    
    words = []
    for r in rows:
        meanings = [m.strip() for m in r["meanings"].split(",")]
        d = {
            "id": r["id"],
            "simplified": r["simplified"],
            "pinyin": r["pinyin"],
            "meanings": meanings,
            "hsk_level": r["hsk_level"],
            "sino_viet": r["sino_viet"] or "",
            "repetitions": r["repetitions"],
        }
        sent = get_sentence(r["simplified"])
        if sent:
            d["sentence_cn"] = sent[0]
            d["sentence_vi"] = sent[1]
        note = get_context_note(r["simplified"])
        if note:
            d["context_note"] = note
        words.append(d)
    return {"words": words}

class ReviewSubmit(BaseModel):
    word_id: int
    quality: int  # 0-5 SM-2 quality

@app.post("/api/review")
def submit_review(data: ReviewSubmit):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM user_words WHERE word_id = ?", (data.word_id,)
    ).fetchone()
    
    if not row:
        return {"error": "Word not found"}
    
    quality = max(0, min(5, data.quality))
    reps, ef, interval = sm2(
        quality, row["repetitions"], row["easiness"], row["interval"]
    )
    
    next_review = (datetime.now() + timedelta(days=interval)).strftime("%Y-%m-%d %H:%M:%S")
    
    conn.execute("""
        UPDATE user_words 
        SET repetitions=?, easiness=?, interval=?, next_review=?,
            total_reviews=total_reviews+1,
            correct_count=correct_count+?
        WHERE word_id=?
    """, (reps, ef, interval, next_review, 1 if quality >= 3 else 0, data.word_id))
    
    # Log quiz result
    conn.execute(
        "INSERT INTO quiz_results (word_id, correct, quiz_type) VALUES (?, ?, 'review')",
        (data.word_id, 1 if quality >= 3 else 0)
    )
    gamify.touch_streak(conn)
    gamify.award_xp(conn, gamify.XP_REVIEW_CORRECT if quality >= 3 else gamify.XP_REVIEW_WRONG, 'review')
    newly_earned = gamify.check_badges(conn)
    conn.commit()
    conn.close()

    return {
        "next_review": next_review,
        "repetitions": reps,
        "easiness": round(ef, 2),
        "interval": interval,
        "newly_earned_badges": newly_earned
    }

def _generate_choices(conn, word_row, pool_hsk_level):
    """Sinh câu hỏi trắc nghiệm: nghĩa đúng + 3 nghĩa sai từ cùng pool HSK level."""
    import random
    correct = word_row["meanings"].split(",")[0].strip()
    wrong_rows = conn.execute("""
        SELECT meanings FROM words
        WHERE hsk_level <= ? AND id != ?
        ORDER BY RANDOM() LIMIT 3
    """, (pool_hsk_level, word_row["id"])).fetchall()
    choices = [correct] + [r["meanings"].split(",")[0].strip() for r in wrong_rows]
    random.shuffle(choices)
    return {
        "word_id": word_row["id"],
        "simplified": word_row["simplified"],
        "pinyin": word_row["pinyin"],
        "hsk_level": word_row["hsk_level"],
        "correct_meaning": correct,
        "choices": choices,
    }

@app.get("/api/quiz/choices/{hsk_level}")
def get_quiz_choices(hsk_level: int, count: int = 10, theme_id: str = None):
    """Câu hỏi trắc nghiệm. theme_id: lấy từ trong theme đó (distractor vẫn từ cả pool level)."""
    conn = get_db()
    if theme_id:
        rows = conn.execute("""
            SELECT w.id, w.simplified, w.pinyin, w.meanings, w.hsk_level
            FROM theme_words tw JOIN words w ON tw.word_id = w.id
            WHERE tw.theme_id = ?
            ORDER BY RANDOM() LIMIT ?
        """, (theme_id, count)).fetchall()
    else:
        rows = conn.execute("""
            SELECT id, simplified, pinyin, meanings, hsk_level
            FROM words WHERE hsk_level <= ?
            ORDER BY RANDOM() LIMIT ?
        """, (hsk_level, count)).fetchall()
    questions = [_generate_choices(conn, r, hsk_level) for r in rows]
    conn.close()
    return {"questions": questions}

class ThemeQuizResult(BaseModel):
    theme_id: str
    results: list  # [{word_id, correct}]

@app.post("/api/quiz/theme-result")
def submit_theme_quiz(data: ThemeQuizResult):
    conn = get_db()
    correct_count = 0
    for r in data.results:
        is_correct = 1 if r.get("correct") else 0
        correct_count += is_correct
        conn.execute(
            "INSERT INTO quiz_results (word_id, correct, quiz_type) VALUES (?, ?, 'theme_quiz')",
            (r["word_id"], is_correct)
        )
    gamify.touch_streak(conn)
    gamify.award_xp(conn, correct_count * gamify.XP_QUIZ_CORRECT, 'theme_quiz')
    gamify.award_xp(conn, gamify.XP_THEME_QUIZ_COMPLETE, 'theme_quiz_complete')
    newly_earned = gamify.check_badges(conn)
    conn.commit()
    conn.close()
    return {"ok": True, "correct": correct_count, "total": len(data.results),
            "newly_earned_badges": newly_earned}

@app.get("/api/themes/{theme_id}/related-dialogues")
def get_related_dialogues(theme_id: str, limit: int = 2):
    """Hội thoại chia sẻ nhiều từ vựng nhất với theme — gợi ý bước học tiếp theo."""
    conn = get_db()
    # So khớp substring trên nội dung thoại (dialogue_words seed theo cụm hanzi nên quá thưa)
    rows = conn.execute("""
        SELECT d.id, d.title, d.context, d.hsk_level,
               COUNT(DISTINCT w.id) as shared_words
        FROM dialogues d
        JOIN dialogue_lines dl ON dl.dialogue_id = d.id
        JOIN theme_words tw ON tw.theme_id = ?
        JOIN words w ON w.id = tw.word_id
        WHERE dl.simplified LIKE '%' || w.simplified || '%'
        GROUP BY d.id
        ORDER BY shared_words DESC
        LIMIT ?
    """, (theme_id, limit)).fetchall()
    conn.close()
    return {"dialogues": [dict(r) for r in rows]}

class PlacementSubmit(BaseModel):
    answers: list  # [{word_id, hsk_level, correct}]

@app.post("/api/placement/submit")
def submit_placement(data: PlacementSubmit):
    conn = get_db()
    hsk2_total = 0
    hsk2_correct = 0
    total_correct = 0
    for a in data.answers:
        is_correct = 1 if a.get("correct") else 0
        total_correct += is_correct
        if a.get("hsk_level") == 2:
            hsk2_total += 1
            hsk2_correct += is_correct
        conn.execute(
            "INSERT INTO quiz_results (word_id, correct, quiz_type) VALUES (?, ?, 'placement')",
            (a["word_id"], is_correct)
        )
    # Đúng >= 60% câu HSK2 → gợi ý bắt đầu HSK2, ngược lại HSK1
    hsk2_acc = hsk2_correct / hsk2_total if hsk2_total > 0 else 0
    recommended = 2 if hsk2_acc >= 0.6 else 1
    conn.execute("UPDATE user_state SET placement_level=? WHERE id=1", (recommended,))
    gamify.touch_streak(conn)
    gamify.award_xp(conn, gamify.XP_PLACEMENT_TEST, 'placement')
    newly_earned = gamify.check_badges(conn)
    conn.commit()
    conn.close()
    accuracy = total_correct / len(data.answers) if data.answers else 0
    return {"recommended_level": recommended, "accuracy": round(accuracy, 2),
            "newly_earned_badges": newly_earned}

@app.get("/api/quiz/{hsk_level}")
def get_quiz(hsk_level: int, count: int = 10):
    conn = get_db()
    rows = conn.execute("""
        SELECT w.id, w.simplified, w.pinyin, w.meanings, w.hsk_level
        FROM words w
        WHERE w.hsk_level <= ?
        ORDER BY RANDOM() LIMIT ?
    """, (hsk_level, count)).fetchall()
    conn.close()
    
    words = []
    for r in rows:
        words.append({
            "id": r["id"],
            "simplified": r["simplified"],
            "pinyin": r["pinyin"],
            "meanings": r["meanings"],
        })
    return {"words": words}

class QuizSubmit(BaseModel):
    word_id: int
    correct: bool
    quiz_type: str = "quiz"  # 'quiz' | 'listening'

@app.post("/api/quiz")
def submit_quiz(data: QuizSubmit):
    quiz_type = data.quiz_type if data.quiz_type in ("quiz", "listening") else "quiz"
    conn = get_db()
    conn.execute(
        "INSERT INTO quiz_results (word_id, correct, quiz_type) VALUES (?, ?, ?)",
        (data.word_id, 1 if data.correct else 0, quiz_type)
    )
    conn.commit()
    conn.close()
    return {"ok": True}

@app.get("/api/words/{hsk_level}")
def get_words_list(hsk_level: int):
    conn = get_db()
    rows = conn.execute(
        "SELECT id, simplified, pinyin, meanings, hsk_level, radical, sino_viet FROM words WHERE hsk_level=? ORDER BY id",
        (hsk_level,)
    ).fetchall()
    conn.close()
    return {"words": [
        {"id": r["id"], "simplified": r["simplified"], 
         "pinyin": r["pinyin"], "meanings": r["meanings"],
         "hsk_level": r["hsk_level"], "radical": r["radical"],
         "sino_viet": r["sino_viet"] or ""}
        for r in rows
    ]}

@app.get("/api/progress")
def get_progress():
    conn = get_db()
    stats = conn.execute("""
        SELECT 
            w.hsk_level,
            COUNT(*) as total,
            SUM(CASE WHEN uw.repetitions >= 5 THEN 1 ELSE 0 END) as mastered,
            SUM(CASE WHEN uw.repetitions >= 1 THEN 1 ELSE 0 END) as seen,
            ROUND(AVG(uw.correct_count * 1.0 / NULLIF(uw.total_reviews, 0)), 2) as accuracy
        FROM words w
        JOIN user_words uw ON w.id = uw.word_id
        GROUP BY w.hsk_level
        ORDER BY w.hsk_level
    """).fetchall()
    
    today_reviewed = conn.execute("""
        SELECT COUNT(*) FROM user_words 
        WHERE DATE(next_review) = DATE('now') AND total_reviews > 0
    """).fetchone()[0]
    
    conn.close()
    return {
        "levels": [dict(s) for s in stats],
        "today_reviewed": today_reviewed
    }

# ---- DIALOGUES ----

@app.get("/api/dialogues")
def list_dialogues(level: int = None):
    conn = get_db()
    if level:
        rows = conn.execute(
            "SELECT d.*, (SELECT COUNT(*) FROM dialogue_lines WHERE dialogue_id = d.id) as line_count FROM dialogues d WHERE d.hsk_level <= ? ORDER BY d.hsk_level, d.id",
            (level,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT d.*, (SELECT COUNT(*) FROM dialogue_lines WHERE dialogue_id = d.id) as line_count FROM dialogues d ORDER BY d.hsk_level, d.id"
        ).fetchall()
    conn.close()
    return {"dialogues": [dict(r) for r in rows]}

@app.get("/api/dialogues/{dialogue_id}")
def get_dialogue(dialogue_id: str):
    conn = get_db()
    d = conn.execute("SELECT * FROM dialogues WHERE id=?", (dialogue_id,)).fetchone()
    if not d:
        conn.close()
        return {"error": "Dialogue not found"}
    
    lines = conn.execute(
        "SELECT * FROM dialogue_lines WHERE dialogue_id=? ORDER BY sort_order",
        (dialogue_id,)
    ).fetchall()
    conn.close()
    
    return {"dialogue": dict(d), "lines": [dict(l) for l in lines]}

@app.get("/api/note/{word}")
def get_context_note_api(word: str):
    note = get_context_note(word)
    return {"word": word, "note": note}

# ---- THEMES API ----

@app.get("/api/themes")
def list_themes(level: int = None):
    conn = get_db()
    rows = conn.execute("""
        SELECT t.*,
               (SELECT COUNT(*) FROM theme_words tw JOIN words w ON tw.word_id = w.id
                WHERE tw.theme_id = t.id AND (? IS NULL OR w.hsk_level = ?)) as total_words,
               (SELECT COUNT(*) FROM theme_words tw
                JOIN words w ON tw.word_id = w.id
                JOIN user_words uw ON tw.word_id = uw.word_id
                WHERE tw.theme_id = t.id AND uw.repetitions >= 1 AND (? IS NULL OR w.hsk_level = ?)) as learned_words
        FROM themes t
        ORDER BY t.id
    """, (level, level, level, level)).fetchall()
    conn.close()
    return {"themes": [dict(r) for r in rows]}

@app.get("/api/themes/{theme_id}")
def get_theme(theme_id: str, level: int = None):
    conn = get_db()
    t = conn.execute("SELECT * FROM themes WHERE id=?", (theme_id,)).fetchone()
    if not t:
        return {"error": "Theme not found"}

    words = conn.execute("""
        SELECT w.id, w.simplified, w.pinyin, w.meanings, w.radical,
               uw.repetitions
        FROM theme_words tw
        JOIN words w ON tw.word_id = w.id
        JOIN user_words uw ON w.id = uw.word_id
        WHERE tw.theme_id = ? AND (? IS NULL OR w.hsk_level = ?)
        ORDER BY tw.sort_order
    """, (theme_id, level, level)).fetchall()
    conn.close()
    
    result = []
    for w in words:
        word_data = {"id": w["id"], "simplified": w["simplified"],
                     "pinyin": w["pinyin"],
                     "meanings": [m.strip() for m in w["meanings"].split(",")],
                     "radical": w["radical"], "learned": w["repetitions"] >= 1}
        # Get sentence
        sent = get_sentence(w["simplified"])
        if sent:
            word_data["sentence_cn"] = sent[0]
            word_data["sentence_vi"] = sent[1]
        result.append(word_data)
    
    return {"theme": dict(t), "words": result}

@app.post("/api/themes/{theme_id}/learn/{word_id}")
def learn_word_in_theme(theme_id: str, word_id: int):
    conn = get_db()
    conn.execute("""
        UPDATE user_words SET repetitions = MAX(repetitions, 1),
            total_reviews = total_reviews + 1,
            correct_count = correct_count + 1
        WHERE word_id = ?
    """, (word_id,))
    gamify.touch_streak(conn)
    gamify.award_xp(conn, gamify.XP_LESSON_WORD, 'lesson_word')
    newly_earned = gamify.check_badges(conn)
    conn.commit()
    conn.close()
    return {"ok": True, "newly_earned_badges": newly_earned}

# ---- PRONUNCIATION ----

class PronunciationLog(BaseModel):
    word_id: int = None
    target_text: str
    recognized_text: str = ""
    score: str  # 'ok' | 'warn' | 'fail'

@app.post("/api/pronunciation/log")
def log_pronunciation(data: PronunciationLog):
    conn = get_db()
    conn.execute(
        "INSERT INTO pronunciation_attempts (word_id, target_text, recognized_text, score) VALUES (?, ?, ?, ?)",
        (data.word_id, data.target_text, data.recognized_text, data.score)
    )
    conn.commit()
    conn.close()
    return {"ok": True}

# ---- WRITING PRACTICE ----

@app.get("/api/writing/characters")
def get_writing_characters(hsk_level: int = 2):
    """Danh sách ký tự đơn (tách từ ghép, dedupe) kèm trạng thái luyện viết."""
    import re
    conn = get_db()
    rows = conn.execute(
        "SELECT simplified, hsk_level FROM words WHERE hsk_level <= ? ORDER BY hsk_level, id",
        (hsk_level,)
    ).fetchall()
    practiced = {
        r["character"]: r for r in
        conn.execute("SELECT character, attempts, best_mistakes, mastered FROM writing_practice").fetchall()
    }
    conn.close()

    seen = set()
    chars = []
    for row in rows:
        for ch in re.findall(r'[一-鿿]', row["simplified"]):
            if ch in seen:
                continue
            seen.add(ch)
            p = practiced.get(ch)
            chars.append({
                "character": ch,
                "hsk_level": row["hsk_level"],
                "practiced": p is not None,
                "attempts": p["attempts"] if p else 0,
                "best_mistakes": p["best_mistakes"] if p else None,
                "mastered": bool(p["mastered"]) if p else False,
            })
    return {"characters": chars}

class WritingComplete(BaseModel):
    character: str
    mistakes: int

@app.post("/api/writing/complete")
def complete_writing(data: WritingComplete):
    conn = get_db()
    conn.execute("""
        INSERT INTO writing_practice (character, attempts, best_mistakes, mastered, last_practiced)
        VALUES (?, 1, ?, ?, datetime('now'))
        ON CONFLICT(character) DO UPDATE SET
            attempts = attempts + 1,
            best_mistakes = MIN(COALESCE(best_mistakes, 9999), excluded.best_mistakes),
            mastered = MAX(mastered, excluded.mastered),
            last_practiced = datetime('now')
    """, (data.character, data.mistakes, 1 if data.mistakes == 0 else 0))
    gamify.touch_streak(conn)
    gamify.award_xp(
        conn,
        gamify.XP_WRITING_PERFECT if data.mistakes == 0 else gamify.XP_WRITING_ATTEMPT,
        'writing'
    )
    newly_earned = gamify.check_badges(conn)
    conn.commit()
    conn.close()
    return {"ok": True, "newly_earned_badges": newly_earned}

@app.get("/api/sentence/{word}")
def get_sentence_api(word: str):
    """Get example sentence for a word."""
    sentence = get_sentence(word)
    if sentence:
        return {"word": word, "cn": sentence[0], "vi": sentence[1]}
    return {"word": word, "cn": None, "vi": None}

# ---- SKILL BREAKDOWN (rule-based, no LLM) ----

PRON_SCORE_MAP = {"ok": 1.0, "warn": 0.5, "fail": 0.0}

def _pct(numerator, denominator):
    return round(100 * numerator / denominator) if denominator else None

def _compute_skill_breakdown(conn):
    vocab_row = conn.execute("""
        SELECT COUNT(*) total, SUM(correct) correct FROM quiz_results
        WHERE quiz_type IN ('quiz', 'theme_quiz', 'review')
    """).fetchone()
    vocab_score = _pct(vocab_row["correct"] or 0, vocab_row["total"] or 0)

    grammar_row = conn.execute("""
        SELECT COUNT(*) total, SUM(qr.correct) correct FROM quiz_results qr
        JOIN context_notes cn ON cn.word_id = qr.word_id
        WHERE qr.quiz_type IN ('quiz', 'theme_quiz', 'review', 'placement')
    """).fetchone()
    grammar_score = _pct(grammar_row["correct"] or 0, grammar_row["total"] or 0)

    listening_row = conn.execute("""
        SELECT COUNT(*) total, SUM(correct) correct FROM quiz_results
        WHERE quiz_type = 'listening'
    """).fetchone()
    listening_score = _pct(listening_row["correct"] or 0, listening_row["total"] or 0)

    pron_rows = conn.execute("SELECT score FROM pronunciation_attempts").fetchall()
    if pron_rows:
        speaking_score = round(100 * sum(PRON_SCORE_MAP.get(r["score"], 0) for r in pron_rows) / len(pron_rows))
    else:
        speaking_score = None

    skills = {
        "vocab": {"label": "Từ vựng", "score": vocab_score},
        "grammar": {"label": "Ngữ pháp", "score": grammar_score},
        "listening": {"label": "Nghe", "score": listening_score},
        "speaking": {"label": "Nói", "score": speaking_score},
    }

    scored = {k: v["score"] for k, v in skills.items() if v["score"] is not None}
    # Cần ít nhất 2 kỹ năng có dữ liệu mới so sánh được yếu/mạnh có ý nghĩa
    weakest = min(scored, key=scored.get) if len(scored) >= 2 else None
    strongest = max(scored, key=scored.get) if len(scored) >= 2 else None

    return skills, weakest, strongest

def _skill_explanation_vi(skills, weakest, strongest):
    if not weakest:
        return "Bạn chưa có đủ dữ liệu ở nhiều kỹ năng để so sánh. Hãy luyện thêm ôn tập, nghe, nói để hệ thống đánh giá chính xác hơn."
    weak_label = skills[weakest]["label"]
    weak_score = skills[weakest]["score"]
    parts = [f"Kỹ năng yếu nhất hiện tại của bạn là **{weak_label}** ({weak_score}%)."]
    if strongest and strongest != weakest:
        parts.append(f"Bạn đang làm tốt nhất ở **{skills[strongest]['label']}** ({skills[strongest]['score']}%).")
    tips = {
        "vocab": "Hãy dành thêm thời gian ôn từ vựng bằng flashcard spaced repetition.",
        "grammar": "Hãy đọc lại các context note ngữ pháp khi ôn từ và chú ý ví dụ câu.",
        "listening": "Hãy luyện nghe nhiều hơn qua các đoạn hội thoại có audio.",
        "speaking": "Hãy luyện nói/đọc theo nhiều hơn và chú ý phản hồi phát âm.",
    }
    parts.append(tips.get(weakest, ""))
    return " ".join(p for p in parts if p)

@app.get("/api/skills/breakdown")
def get_skill_breakdown():
    conn = get_db()
    skills, weakest, strongest = _compute_skill_breakdown(conn)
    conn.close()
    return {
        "skills": skills,
        "weakest_skill": weakest,
        "strongest_skill": strongest,
        "explanation_vi": _skill_explanation_vi(skills, weakest, strongest),
    }

# ---- HSK 3.0 MAPPING ----

@app.get("/api/hsk-mapping")
def get_hsk_mapping():
    return {"mapping": HSK_MAPPING}

# ---- DAILY 5-MINUTE SESSION ----

@app.get("/api/daily-session")
def get_daily_session(level: int = None):
    """Lắp ráp phiên học 5 phút/ngày: ôn từ (SM-2), nghe, nói, hội thoại ngắn.
    Ưu tiên nội dung liên quan tới kỹ năng yếu nhất, nhưng luôn đủ 4 khối.
    `level`: cấp HSK người dùng đang chọn (tuỳ chọn) — giới hạn khối nghe/nói/
    hội thoại về <= cấp đó, để người mới không bị rơi vào từ/hội thoại quá
    khó. Khối ôn tập (review) vẫn không lọc theo level vì phản ánh đúng
    lịch sử SM-2 thực tế của người học, không phải cấp đang duyệt."""
    conn = get_db()
    skills, weakest, _ = _compute_skill_breakdown(conn)

    review_rows = conn.execute("""
        SELECT w.id, w.simplified, w.pinyin, w.meanings, w.hsk_level, w.sino_viet
        FROM words w JOIN user_words uw ON w.id = uw.word_id
        WHERE uw.next_review <= datetime('now')
        ORDER BY uw.next_review ASC, uw.repetitions ASC LIMIT 5
    """).fetchall()
    review_block = [dict(r) for r in review_rows]

    listen_row = conn.execute("""
        SELECT dl.dialogue_id, dl.simplified, dl.pinyin, dl.vietnamese, d.hsk_level
        FROM dialogue_lines dl JOIN dialogues d ON dl.dialogue_id = d.id
        WHERE (? IS NULL OR d.hsk_level <= ?)
        ORDER BY RANDOM() LIMIT 1
    """, (level, level)).fetchone()
    listening_block = dict(listen_row) if listen_row else None

    speak_row = conn.execute("""
        SELECT id, simplified, pinyin, meanings, hsk_level FROM words
        WHERE (? IS NULL OR hsk_level <= ?)
        ORDER BY RANDOM() LIMIT 1
    """, (level, level)).fetchone()
    speaking_block = dict(speak_row) if speak_row else None

    scenario_ids = [
        sid for sid, s in CONVERSATIONS.items() if level is None or s["hsk_level"] <= level
    ] or list(CONVERSATIONS.keys())
    import random
    conversation_id = random.choice(scenario_ids) if scenario_ids else None
    conversation_hsk_level = CONVERSATIONS[conversation_id]["hsk_level"] if conversation_id else None

    conn.close()
    return {
        "focus_skill": weakest,
        "skills": skills,
        "blocks": {
            "review": review_block,
            "listening": listening_block,
            "speaking": speaking_block,
            "conversation_scenario_id": conversation_id,
            "conversation_hsk_level": conversation_hsk_level,
        },
    }

# ---- SCRIPTED CONVERSATION PRACTICE ----

@app.get("/api/conversation/{scenario_id}")
def get_conversation(scenario_id: str):
    scenario = CONVERSATIONS.get(scenario_id)
    if not scenario:
        return JSONResponse({"error": "Scenario not found"}, status_code=404)
    return {"scenario_id": scenario_id, "title": scenario["title"],
            "hsk_level": scenario["hsk_level"], "start": scenario["start"],
            "node": scenario["nodes"][scenario["start"]]}

class ConversationRespond(BaseModel):
    node_id: str
    choice_id: str

@app.post("/api/conversation/{scenario_id}/respond")
def respond_conversation(scenario_id: str, data: ConversationRespond):
    scenario = CONVERSATIONS.get(scenario_id)
    if not scenario:
        return JSONResponse({"error": "Scenario not found"}, status_code=404)
    node = scenario["nodes"].get(data.node_id)
    if not node:
        return JSONResponse({"error": "Node not found"}, status_code=404)
    choice = next((c for c in node["choices"] if c["id"] == data.choice_id), None)
    if not choice:
        return JSONResponse({"error": "Choice not found"}, status_code=400)
    next_id = choice["next"]
    next_node = scenario["nodes"][next_id]
    is_end = len(next_node["choices"]) == 0
    if is_end:
        conn = get_db()
        gamify.touch_streak(conn)
        gamify.award_xp(conn, 20, 'conversation_complete')
        newly_earned = gamify.check_badges(conn)
        conn.commit()
        conn.close()
    else:
        newly_earned = []
    return {"node_id": next_id, "node": next_node, "is_end": is_end,
            "newly_earned_badges": newly_earned}

# ---- MOCK EXAM (thi thử) — per-level, 3 sections: nghe / đọc / ngữ pháp ----

EXAM_TIER_QUESTION_COUNT = {1: 20, 2: 20, 3: 20, 4: 30, 5: 30, 6: 30, 7: 40, 8: 40, 9: 40}
EXAM_TIER_TIME_LIMIT_MIN = {1: 15, 2: 15, 3: 15, 4: 25, 5: 25, 6: 25, 7: 35, 8: 35, 9: 35}
EXAM_PASS_THRESHOLD = 60.0


def _exam_mc_question(conn, word_row, pool_level, section):
    q = _generate_choices(conn, word_row, pool_level)
    q["section"] = section
    return q


def _exam_cloze_question(conn, level, exclude_ids):
    """Fill-in-the-blank from a real example sentence, if one exists for a word
    at/under this level. Example sentences only exist for the hand-curated
    HSK1/2 words, so this section is naturally sparse-to-empty at higher
    levels — callers pad remaining slots with reading MC questions instead."""
    rows = conn.execute(
        "SELECT id, simplified FROM words WHERE hsk_level <= ? ORDER BY RANDOM() LIMIT 60", (level,)
    ).fetchall()
    for r in rows:
        if r["id"] in exclude_ids:
            continue
        sent = get_sentence(r["simplified"])
        if sent and r["simplified"] in sent[0]:
            blanked = sent[0].replace(r["simplified"], "___", 1)
            wrong_rows = conn.execute(
                "SELECT simplified FROM words WHERE hsk_level <= ? AND id != ? ORDER BY RANDOM() LIMIT 3",
                (level, r["id"])
            ).fetchall()
            choices = [r["simplified"]] + [w["simplified"] for w in wrong_rows]
            random.shuffle(choices)
            return {
                "word_id": r["id"], "section": "grammar",
                "sentence_blanked": blanked, "sentence_vi": sent[1],
                "correct_word": r["simplified"], "choices": choices,
            }
    return None


@app.get("/api/exam/{hsk_level}/start")
def start_exam(hsk_level: int, count: int = 0):
    hsk_level = max(1, min(9, hsk_level))
    total = max(5, min(60, count)) if count else EXAM_TIER_QUESTION_COUNT[hsk_level]
    n_listen = round(total * 0.3)
    n_grammar = round(total * 0.3)
    n_read = total - n_listen - n_grammar

    conn = get_db()
    rows = conn.execute(
        "SELECT id, simplified, pinyin, meanings, hsk_level FROM words WHERE hsk_level <= ? ORDER BY RANDOM() LIMIT ?",
        (hsk_level, n_listen + n_read)
    ).fetchall()
    listen_rows, read_rows = rows[:n_listen], rows[n_listen:]

    questions = []
    used_ids = set()
    for r in listen_rows:
        questions.append(_exam_mc_question(conn, r, hsk_level, "listening"))
        used_ids.add(r["id"])
    for r in read_rows:
        questions.append(_exam_mc_question(conn, r, hsk_level, "reading"))
        used_ids.add(r["id"])

    grammar_added = 0
    for _ in range(n_grammar):
        cq = _exam_cloze_question(conn, hsk_level, used_ids)
        if not cq:
            break
        questions.append(cq)
        used_ids.add(cq["word_id"])
        grammar_added += 1

    if grammar_added < n_grammar:
        need = n_grammar - grammar_added
        pad_rows = conn.execute(
            "SELECT id, simplified, pinyin, meanings, hsk_level FROM words WHERE hsk_level <= ? ORDER BY RANDOM() LIMIT ?",
            (hsk_level, need + len(used_ids))
        ).fetchall()
        added = 0
        for r in pad_rows:
            if r["id"] in used_ids:
                continue
            questions.append(_exam_mc_question(conn, r, hsk_level, "reading"))
            used_ids.add(r["id"])
            added += 1
            if added >= need:
                break

    random.shuffle(questions)
    conn.close()
    return {
        "hsk_level": hsk_level,
        "questions": questions,
        "time_limit_seconds": EXAM_TIER_TIME_LIMIT_MIN[hsk_level] * 60,
    }


class ExamAnswer(BaseModel):
    section: str  # 'listening' | 'reading' | 'grammar'
    correct: bool


class ExamSubmit(BaseModel):
    answers: list[ExamAnswer]
    duration_seconds: int = 0


@app.post("/api/exam/{hsk_level}/submit")
def submit_exam(hsk_level: int, data: ExamSubmit):
    hsk_level = max(1, min(9, hsk_level))
    section_totals = {}
    for a in data.answers:
        s = section_totals.setdefault(a.section, {"total": 0, "correct": 0})
        s["total"] += 1
        if a.correct:
            s["correct"] += 1

    total = len(data.answers)
    correct_count = sum(1 for a in data.answers if a.correct)
    score_pct = round(100 * correct_count / total, 1) if total else 0.0
    passed = score_pct >= EXAM_PASS_THRESHOLD

    section_scores = {
        k: {"total": v["total"], "correct": v["correct"],
            "pct": round(100 * v["correct"] / v["total"], 1) if v["total"] else None}
        for k, v in section_totals.items()
    }

    conn = get_db()
    conn.execute(
        "INSERT INTO exam_sessions (hsk_level, total_questions, correct_count, section_scores, score_pct, passed, duration_seconds) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (hsk_level, total, correct_count, json.dumps(section_scores, ensure_ascii=False),
         score_pct, 1 if passed else 0, data.duration_seconds)
    )
    gamify.touch_streak(conn)
    gamify.award_xp(conn, correct_count * 5 + (50 if passed else 0), 'exam')
    newly_earned = gamify.check_badges(conn)
    conn.commit()
    conn.close()

    return {
        "score_pct": score_pct, "passed": passed, "correct_count": correct_count,
        "total_questions": total, "section_scores": section_scores,
        "newly_earned_badges": newly_earned,
    }


@app.get("/api/exam/history")
def exam_history(hsk_level: int = None, limit: int = 20):
    conn = get_db()
    if hsk_level:
        rows = conn.execute(
            "SELECT * FROM exam_sessions WHERE hsk_level=? ORDER BY created_at DESC LIMIT ?", (hsk_level, limit)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM exam_sessions ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["section_scores"] = json.loads(d["section_scores"])
        result.append(d)
    return {"sessions": result}


@app.get("/api/exam/best")
def exam_best():
    """Best score + attempt count per level — for the exam picker page."""
    conn = get_db()
    rows = conn.execute("""
        SELECT hsk_level, MAX(score_pct) as best_pct, SUM(passed) as pass_count, COUNT(*) as attempt_count
        FROM exam_sessions GROUP BY hsk_level
    """).fetchall()
    conn.close()
    return {"levels": [dict(r) for r in rows]}


# ---- TTS (server-side neural Mandarin voice, edge-tts, disk-cached) ----

@app.get("/api/tts")
async def get_tts(text: str, voice: str = tts.DEFAULT_VOICE, rate: float = 1.0):
    text = text.strip()[:500]
    if not text:
        return JSONResponse({"error": "empty text"}, status_code=400)
    try:
        path = await tts.synthesize(text, voice=voice, rate=rate)
    except Exception:
        return JSONResponse({"error": "tts_unavailable"}, status_code=503)
    return FileResponse(path, media_type="audio/mpeg", headers={"Cache-Control": "public, max-age=31536000"})


@app.get("/")
def index():
    return FileResponse("static/index.html")
