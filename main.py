import os
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from database import get_db, init_db
from sm2 import sm2
from seed_data import get_words, get_hsk1, get_hsk2, get_sentence, get_sino_viet, get_context_note, get_dialogues, THEMES, get_theme_words

app = FastAPI(title="Hán Ngữ+ - Học tiếng Trung HSK")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup():
    init_db()
    seed_words()
    seed_themes()
    seed_dialogues()

def seed_words():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
    if count > 0:
        conn.close()
        return
    
    words = get_words()
    conn.executemany(
        "INSERT INTO words (simplified, pinyin, meanings, hsk_level, radical) VALUES (?, ?, ?, ?, ?)",
        words
    )
    conn.commit()
    
    # Update sino_viet for all words
    for w in conn.execute("SELECT id, simplified FROM words").fetchall():
        sv = get_sino_viet(w["simplified"])
        if sv:
            conn.execute("UPDATE words SET sino_viet=? WHERE id=?", (sv, w["id"]))
    conn.commit()
    
    # Auto-add to user_words for all words
    word_ids = conn.execute("SELECT id FROM words").fetchall()
    for w in word_ids:
        conn.execute(
            "INSERT OR IGNORE INTO user_words (word_id) VALUES (?)",
            (w[0],)
        )
    conn.commit()
    conn.close()
    print(f"Seeded {len(words)} words")

def seed_themes():
    conn = get_db()
    existing = conn.execute("SELECT COUNT(*) FROM themes").fetchone()[0]
    if existing > 0:
        conn.close()
        return
    # Seed themes
    for tid, t in THEMES.items():
        conn.execute(
            "INSERT OR IGNORE INTO themes (id, name, icon, description) VALUES (?, ?, ?, ?)",
            (tid, t["name"], t["icon"], t["desc"])
        )
        # Link words
        for i, w_simplified in enumerate(t["words"]):
            row = conn.execute(
                "SELECT id FROM words WHERE simplified=?", (w_simplified,)
            ).fetchone()
            if row:
                conn.execute(
                    "INSERT OR IGNORE INTO theme_words (theme_id, word_id, sort_order) VALUES (?, ?, ?)",
                    (tid, row["id"], i)
                )
    conn.commit()
    conn.close()
    print(f"Seeded {len(THEMES)} themes")

def seed_dialogues():
    conn = get_db()
    existing = conn.execute("SELECT COUNT(*) FROM dialogues").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    import re
    dialogues = get_dialogues()
    for did, d in dialogues.items():
        conn.execute(
            "INSERT OR IGNORE INTO dialogues (id, title, context, hsk_level) VALUES (?, ?, ?, ?)",
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
    print(f"Seeded {len(dialogues)} dialogues")

# ---- API Routes ----

@app.get("/api/stats")
def get_stats():
    conn = get_db()
    # Total words per HSK level
    hsk1 = conn.execute("SELECT COUNT(*) FROM words WHERE hsk_level=1").fetchone()[0]
    hsk2 = conn.execute("SELECT COUNT(*) FROM words WHERE hsk_level=2").fetchone()[0]
    
    # Review stats
    due = conn.execute("SELECT COUNT(*) FROM user_words WHERE next_review <= datetime('now')").fetchone()[0]
    total = conn.execute("SELECT COUNT(*) FROM user_words").fetchone()[0]
    learned = conn.execute("SELECT COUNT(*) FROM user_words WHERE repetitions >= 5").fetchone()[0]
    
    # Due by level
    due_hsk1 = conn.execute("""
        SELECT COUNT(*) FROM user_words uw 
        JOIN words w ON uw.word_id = w.id 
        WHERE w.hsk_level=1 AND uw.next_review <= datetime('now')
    """).fetchone()[0]
    due_hsk2 = conn.execute("""
        SELECT COUNT(*) FROM user_words uw 
        JOIN words w ON uw.word_id = w.id 
        WHERE w.hsk_level=2 AND uw.next_review <= datetime('now')
    """).fetchone()[0]
    
    dlg_count = conn.execute("SELECT COUNT(*) FROM dialogues").fetchone()[0]
    
    conn.close()
    return {
        "hsk1": hsk1, "hsk2": hsk2,
        "due": due, "total": total, "learned": learned,
        "due_hsk1": due_hsk1, "due_hsk2": due_hsk2,
        "dialogues": dlg_count
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
    conn.commit()
    conn.close()
    
    return {
        "next_review": next_review,
        "repetitions": reps,
        "easiness": round(ef, 2),
        "interval": interval
    }

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

@app.post("/api/quiz")
def submit_quiz(data: QuizSubmit):
    conn = get_db()
    conn.execute(
        "INSERT INTO quiz_results (word_id, correct, quiz_type) VALUES (?, ?, 'quiz')",
        (data.word_id, 1 if data.correct else 0)
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
def list_themes():
    conn = get_db()
    rows = conn.execute("""
        SELECT t.*,
               (SELECT COUNT(*) FROM theme_words WHERE theme_id = t.id) as total_words,
               (SELECT COUNT(*) FROM theme_words tw 
                JOIN user_words uw ON tw.word_id = uw.word_id 
                WHERE tw.theme_id = t.id AND uw.repetitions >= 1) as learned_words
        FROM themes t
        ORDER BY t.id
    """).fetchall()
    conn.close()
    return {"themes": [dict(r) for r in rows]}

@app.get("/api/themes/{theme_id}")
def get_theme(theme_id: str):
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
        WHERE tw.theme_id = ?
        ORDER BY tw.sort_order
    """, (theme_id,)).fetchall()
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
    conn.commit()
    conn.close()
    return {"ok": True}

@app.get("/api/sentence/{word}")
def get_sentence_api(word: str):
    """Get example sentence for a word."""
    sentence = get_sentence(word)
    if sentence:
        return {"word": word, "cn": sentence[0], "vi": sentence[1]}
    return {"word": word, "cn": None, "vi": None}

@app.get("/")
def index():
    return FileResponse("static/index.html")
