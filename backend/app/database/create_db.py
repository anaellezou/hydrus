import sqlite3
import json
import os

DB_PATH = "jlpt.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# create tables
def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kanji (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        kanji    TEXT NOT NULL,
        onyomi   TEXT,
        kunyomi  TEXT,
        meaning  TEXT,
        level    TEXT DEFAULT 'N5'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocabulary (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        vocab    TEXT NOT NULL,
        romaji   TEXT,
        hiragana TEXT,
        type     TEXT,
        meaning  TEXT,
        level    TEXT DEFAULT 'N5'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grammar (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        romaji   TEXT NOT NULL,
        japanese TEXT,
        meaning  TEXT,
        level    TEXT DEFAULT 'N5'
    )
    """)

# insert data from JSON files

def to_str(value):
    """ convert line to json string if it's a list, otherwise return the value as is """
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    return value

def add_n5_kanji(cursor):
    with open("app/resources/kanji_n5.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for entry in data:
        cursor.execute("""
        INSERT INTO kanji (kanji, onyomi, kunyomi, meaning, level)
        VALUES (?, ?, ?, ?, ?)
        """, (
            entry["kanji"],
            to_str(entry.get("onyomi")),
            to_str(entry.get("kunyomi")),
            to_str(entry.get("meaning")),
            entry.get("level", "N5"),
        ))
    print(f"✓ {len(data)} kanji added")

def add_n5_vocabulary(cursor):
    with open("app/resources/vocab_n5.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for entry in data:
        cursor.execute("""
        INSERT INTO vocabulary (vocab, romaji, hiragana, type, meaning, level)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entry["vocab"],
            entry.get("reading", {}).get("romaji"),
            entry.get("reading", {}).get("hiragana"),
            entry.get("type"),
            to_str(entry.get("meaning")),
            entry.get("level", "N5"),
        ))
    print(f"✓ {len(data)} words added")

def add_n5_grammar(cursor):
    with open("app/resources/grammar_n5.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for entry in data:
        cursor.execute("""
        INSERT INTO grammar (romaji, japanese, meaning, level)
        VALUES (?, ?, ?, ?)
        """, (
            entry["romaji"],
            entry.get("japanese"),
            entry.get("meaning"),
            entry.get("level", "N5"),
        ))
    print(f"✓ {len(data)} grammar points added")


# create database and populate it

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Ancienne DB supprimée")

    conn = get_connection()
    cursor = conn.cursor()

    create_tables(cursor)
    add_n5_kanji(cursor)
    add_n5_vocabulary(cursor)
    add_n5_grammar(cursor)

    conn.commit()
    conn.close()
    print(f"\n✓ database '{DB_PATH}' successfully created")

if __name__ == "__main__":
    create_database()
