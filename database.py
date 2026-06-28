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

        CREATE INDEX IF NOT EXISTS idx_next_review ON user_words(next_review);
        CREATE INDEX IF NOT EXISTS idx_hsk_level ON words(hsk_level);
        CREATE INDEX IF NOT EXISTS idx_dialogue_level ON dialogues(hsk_level);
        CREATE INDEX IF NOT EXISTS idx_dialogue_lines ON dialogue_lines(dialogue_id, sort_order);
    """)
    conn.commit()
    conn.close()
