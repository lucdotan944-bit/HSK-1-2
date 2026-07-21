"""SQLite database for HSK app.

Production (Render) has no persistent disk on the free tier, so a local
hsk.db file gets wiped on every deploy/restart — set TURSO_DATABASE_URL +
TURSO_AUTH_TOKEN (a free https://turso.tech database) to persist instead;
get_db() then routes through db_compat's libsql shim. Local dev with no
those env vars set keeps using a plain local sqlite3 file, unchanged.
"""
import sqlite3
import json
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'hsk.db')

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

def get_db():
    if TURSO_DATABASE_URL:
        import db_compat
        return db_compat.connect(TURSO_DATABASE_URL, TURSO_AUTH_TOKEN)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _ensure_column(conn, table, column, coldef):
    """Idempotently add a column (SQLite has no ADD COLUMN IF NOT EXISTS)."""
    cols = [r["name"] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coldef}")

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simplified TEXT NOT NULL,
            pinyin TEXT NOT NULL,
            meanings TEXT NOT NULL,
            hsk_level INTEGER NOT NULL,
            radical TEXT DEFAULT '',
            sino_viet TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS themes (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            icon TEXT DEFAULT '',
            description TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS theme_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            theme_id TEXT NOT NULL,
            word_id INTEGER NOT NULL,
            sort_order INTEGER DEFAULT 0,
            FOREIGN KEY (theme_id) REFERENCES themes(id),
            FOREIGN KEY (word_id) REFERENCES words(id)
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash TEXT,
            google_sub TEXT UNIQUE,
            display_name TEXT DEFAULT '',
            is_guest INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            expires_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS user_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL DEFAULT 1,
            word_id INTEGER NOT NULL,
            repetitions INTEGER DEFAULT 0,
            easiness REAL DEFAULT 2.5,
            interval INTEGER DEFAULT 0,
            next_review TEXT DEFAULT (datetime('now')),
            total_reviews INTEGER DEFAULT 0,
            correct_count INTEGER DEFAULT 0,
            FOREIGN KEY (word_id) REFERENCES words(id)
        );

        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL DEFAULT 1,
            word_id INTEGER NOT NULL,
            correct INTEGER NOT NULL,
            quiz_type TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (word_id) REFERENCES words(id)
        );

        CREATE TABLE IF NOT EXISTS dialogues (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            context TEXT DEFAULT '',
            hsk_level INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS dialogue_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dialogue_id TEXT NOT NULL,
            speaker TEXT NOT NULL,
            simplified TEXT NOT NULL,
            pinyin TEXT NOT NULL,
            vietnamese TEXT NOT NULL,
            sort_order INTEGER DEFAULT 0,
            FOREIGN KEY (dialogue_id) REFERENCES dialogues(id)
        );

        CREATE TABLE IF NOT EXISTS dialogue_words (
            dialogue_id TEXT NOT NULL,
            word_id INTEGER NOT NULL,
            PRIMARY KEY (dialogue_id, word_id),
            FOREIGN KEY (dialogue_id) REFERENCES dialogues(id),
            FOREIGN KEY (word_id) REFERENCES words(id)
        );

        CREATE TABLE IF NOT EXISTS context_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL,
            note_vi TEXT NOT NULL,
            note_type TEXT DEFAULT 'grammar',
            FOREIGN KEY (word_id) REFERENCES words(id)
        );
        
        CREATE TABLE IF NOT EXISTS example_sentence_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL,
            sentence_cn TEXT NOT NULL,
            sentence_pinyin TEXT NOT NULL,
            sentence_vi TEXT NOT NULL,
            FOREIGN KEY (word_id) REFERENCES words(id)
        );

        CREATE TABLE IF NOT EXISTS user_state (
            user_id INTEGER PRIMARY KEY,
            xp INTEGER DEFAULT 0,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            last_active_date TEXT DEFAULT '',
            placement_level INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS badges_earned (
            user_id INTEGER NOT NULL DEFAULT 1,
            badge_id TEXT NOT NULL,
            earned_at TEXT DEFAULT (datetime('now')),
            PRIMARY KEY (user_id, badge_id)
        );

        CREATE TABLE IF NOT EXISTS xp_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL DEFAULT 1,
            amount INTEGER NOT NULL,
            reason TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS writing_practice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL DEFAULT 1,
            character TEXT NOT NULL,
            attempts INTEGER DEFAULT 0,
            best_mistakes INTEGER DEFAULT NULL,
            last_practiced TEXT DEFAULT (datetime('now')),
            mastered INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS pronunciation_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL DEFAULT 1,
            word_id INTEGER,
            target_text TEXT NOT NULL,
            recognized_text TEXT DEFAULT '',
            score TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (word_id) REFERENCES words(id)
        );

        CREATE TABLE IF NOT EXISTS exam_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL DEFAULT 1,
            hsk_level INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            correct_count INTEGER NOT NULL,
            section_scores TEXT NOT NULL DEFAULT '{}',
            score_pct REAL NOT NULL,
            passed INTEGER NOT NULL,
            duration_seconds INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS ai_chat_usage (
            user_id INTEGER NOT NULL DEFAULT 1,
            day TEXT NOT NULL,
            count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (user_id, day)
        );

        CREATE INDEX IF NOT EXISTS idx_exam_sessions_level ON exam_sessions(hsk_level, created_at);
        CREATE INDEX IF NOT EXISTS idx_xp_log_created ON xp_log(created_at);
        CREATE INDEX IF NOT EXISTS idx_next_review ON user_words(next_review);
        CREATE INDEX IF NOT EXISTS idx_hsk_level ON words(hsk_level);
        CREATE INDEX IF NOT EXISTS idx_dialogue_level ON dialogues(hsk_level);
        CREATE INDEX IF NOT EXISTS idx_dialogue_lines ON dialogue_lines(dialogue_id, sort_order);
    """)
    conn.commit()

    _migrate_multi_user(conn)

    # user_words historically had no unique constraint, so old DBs may hold
    # duplicate SM-2 rows per word. Clean up, then enforce (user_id, word_id)
    # so submit_review's upsert has a conflict target.
    _dedupe_user_words(conn)
    conn.execute("DROP INDEX IF EXISTS idx_user_words_word_id")
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_user_words_user_word ON user_words(user_id, word_id)")
    conn.execute("DROP INDEX IF EXISTS idx_writing_char")
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_writing_user_char ON writing_practice(user_id, character)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_quiz_results_user ON quiz_results(user_id, created_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_exam_sessions_user ON exam_sessions(user_id, created_at)")
    conn.commit()
    conn.close()


def _has_column(conn, table, column):
    return column in [r["name"] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]


def _migrate_multi_user(conn):
    """Nâng DB single-user cũ lên multi-user. Idempotent — DB mới (đã tạo theo
    schema mới ở trên) không có gì để làm. Mọi dữ liệu cũ gán về user_id=1
    ("người dùng khách kế thừa" — xem seed trong main.py)."""
    # Các bảng chỉ cần thêm cột (giữ nguyên PK id autoincrement)
    for table in ("user_words", "quiz_results", "xp_log", "writing_practice",
                  "pronunciation_attempts", "exam_sessions"):
        if not _has_column(conn, table, "user_id"):
            conn.execute(f"ALTER TABLE {table} ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1")

    # user_state: PK cũ là id CHECK(id=1) — phải dựng lại theo user_id.
    if not _has_column(conn, "user_state", "user_id"):
        conn.execute("ALTER TABLE user_state RENAME TO user_state_old")
        conn.execute("""
            CREATE TABLE user_state (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                last_active_date TEXT DEFAULT '',
                placement_level INTEGER DEFAULT 0
            )
        """)
        conn.execute("""
            INSERT INTO user_state (user_id, xp, current_streak, longest_streak, last_active_date, placement_level)
            SELECT 1, xp, current_streak, longest_streak, last_active_date, placement_level
            FROM user_state_old WHERE id = 1
        """)
        conn.execute("DROP TABLE user_state_old")

    # badges_earned: PK cũ là badge_id — dựng lại theo (user_id, badge_id).
    if not _has_column(conn, "badges_earned", "user_id"):
        conn.execute("ALTER TABLE badges_earned RENAME TO badges_earned_old")
        conn.execute("""
            CREATE TABLE badges_earned (
                user_id INTEGER NOT NULL DEFAULT 1,
                badge_id TEXT NOT NULL,
                earned_at TEXT DEFAULT (datetime('now')),
                PRIMARY KEY (user_id, badge_id)
            )
        """)
        conn.execute("""
            INSERT INTO badges_earned (user_id, badge_id, earned_at)
            SELECT 1, badge_id, earned_at FROM badges_earned_old
        """)
        conn.execute("DROP TABLE badges_earned_old")

    # ai_chat_usage: PK cũ là day — dựng lại theo (user_id, day).
    if not _has_column(conn, "ai_chat_usage", "user_id"):
        conn.execute("ALTER TABLE ai_chat_usage RENAME TO ai_chat_usage_old")
        conn.execute("""
            CREATE TABLE ai_chat_usage (
                user_id INTEGER NOT NULL DEFAULT 1,
                day TEXT NOT NULL,
                count INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (user_id, day)
            )
        """)
        conn.execute("""
            INSERT INTO ai_chat_usage (user_id, day, count)
            SELECT 1, day, count FROM ai_chat_usage_old
        """)
        conn.execute("DROP TABLE ai_chat_usage_old")

    conn.commit()


def _dedupe_user_words(conn):
    dupes = conn.execute(
        "SELECT user_id, word_id FROM user_words GROUP BY user_id, word_id HAVING COUNT(*) > 1"
    ).fetchall()
    removed = 0
    for row in dupes:
        rows = conn.execute(
            "SELECT id FROM user_words WHERE user_id=? AND word_id=? ORDER BY repetitions DESC, id ASC",
            (row["user_id"], row["word_id"])
        ).fetchall()
        drop_ids = [r["id"] for r in rows[1:]]
        conn.executemany("DELETE FROM user_words WHERE id=?", [(i,) for i in drop_ids])
        removed += len(drop_ids)
    if removed:
        conn.commit()
        print(f"Deduped {removed} duplicate user_words rows")
