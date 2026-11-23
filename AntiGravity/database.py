import sqlite3
import json
from datetime import datetime

DB_NAME = "smart_notes.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            semester TEXT NOT NULL,
            topic_name TEXT NOT NULL,
            raw_text TEXT NOT NULL,
            summary TEXT,
            key_definitions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Flashcards table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            FOREIGN KEY (note_id) REFERENCES notes (id)
        )
    """)

    # Vector embeddings schema (reserved for 100% stage)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id INTEGER NOT NULL,
            vector_data BLOB NOT NULL,
            FOREIGN KEY (note_id) REFERENCES notes (id)
        )
    """)

    conn.commit()
    conn.close()

def save_note(subject, semester, topic_name, raw_text, summary, key_definitions, flashcards=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notes (subject, semester, topic_name, raw_text, summary, key_definitions)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (subject, semester, topic_name, raw_text, summary, json.dumps(key_definitions) if key_definitions else "[]"))
    
    note_id = cursor.lastrowid

    if flashcards:
        for card in flashcards:
            cursor.execute("""
                INSERT INTO flashcards (note_id, question, answer)
                VALUES (?, ?, ?)
            """, (note_id, card.get("question", ""), card.get("answer", "")))

    conn.commit()
    conn.close()
    return note_id

def get_all_notes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, subject, semester, topic_name, created_at, summary FROM notes ORDER BY id DESC")
    rows = cursor.fetchall()
    notes = [dict(row) for row in rows]
    conn.close()
    return notes

def get_note_by_id(note_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    note_row = cursor.fetchone()
    if not note_row:
        conn.close()
        return None
    
    note = dict(note_row)
    cursor.execute("SELECT question, answer FROM flashcards WHERE note_id = ?", (note_id,))
    note["flashcards"] = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return note

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
