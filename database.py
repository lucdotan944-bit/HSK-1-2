"""SQLite database for HSK app"""
import sqlite3
import json
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'hsk.db')

def get_db():
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

        CREATE TABLE IF NOT EXISTS user_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            id INTEGER PRIMARY KEY CHECK (id = 1),
            xp INTEGER DEFAULT 0,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            last_active_date TEXT DEFAULT '',
            placement_level INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS badges_earned (
            badge_id TEXT PRIMARY KEY,
            earned_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS xp_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER NOT NULL,
            reason TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS writing_practice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character TEXT NOT NULL,
            attempts INTEGER DEFAULT 0,
            best_mistakes INTEGER DEFAULT NULL,
            last_practiced TEXT DEFAULT (datetime('now')),
            mastered INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS pronunciation_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER,
            target_text TEXT NOT NULL,
            recognized_text TEXT DEFAULT '',
            score TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (word_id) REFERENCES words(id)
        );

        CREATE TABLE IF NOT EXISTS exam_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hsk_level INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            correct_count INTEGER NOT NULL,
            section_scores TEXT NOT NULL DEFAULT '{}',
            score_pct REAL NOT NULL,
            passed INTEGER NOT NULL,
            duration_seconds INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE UNIQUE INDEX IF NOT EXISTS idx_writing_char ON writing_practice(character);
        CREATE INDEX IF NOT EXISTS idx_exam_sessions_level ON exam_sessions(hsk_level, created_at);
        CREATE INDEX IF NOT EXISTS idx_xp_log_created ON xp_log(created_at);
        CREATE INDEX IF NOT EXISTS idx_next_review ON user_words(next_review);
        CREATE INDEX IF NOT EXISTS idx_hsk_level ON words(hsk_level);
        CREATE INDEX IF NOT EXISTS idx_dialogue_level ON dialogues(hsk_level);
        CREATE INDEX IF NOT EXISTS idx_dialogue_lines ON dialogue_lines(dialogue_id, sort_order);
    """)
    conn.commit()

    # user_words had no unique constraint on word_id, so seed_words()'s
    # "INSERT OR IGNORE ... VALUES (word_id)" never actually had anything to
    # conflict with — it silently inserted a fresh duplicate SM-2 row per
    # word on every server restart. Clean up any dupes accumulated before
    # this fix, then add the index so it can't recur (safe: submit_review
    # always UPDATEs by word_id, touching every dupe together, so they hold
    # identical values — keeping the one with the most progress loses nothing).
    _dedupe_user_words(conn)
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_user_words_word_id ON user_words(word_id)")
    conn.commit()
    conn.close()


def _dedupe_user_words(conn):
    dupes = conn.execute(
        "SELECT word_id FROM user_words GROUP BY word_id HAVING COUNT(*) > 1"
    ).fetchall()
    removed = 0
    for row in dupes:
        rows = conn.execute(
            "SELECT id FROM user_words WHERE word_id=? ORDER BY repetitions DESC, id ASC",
            (row["word_id"],)
        ).fetchall()
        drop_ids = [r["id"] for r in rows[1:]]
        conn.executemany("DELETE FROM user_words WHERE id=?", [(i,) for i in drop_ids])
        removed += len(drop_ids)
    if removed:
        conn.commit()
        print(f"Deduped {removed} duplicate user_words rows")
