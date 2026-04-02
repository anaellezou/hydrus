import sqlite3
import json
import os

DB_PATH = "app/database/kanji_database.db"

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kanji (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kanji TEXT NOT NULL,
        onyomi TEXT,
        kunyomi TEXT,
        meaning TEXT,
        level TEXT DEFAULT 'N5'
    )
    """)

    with open("app/resources/kanji_n5.json", "r", encoding="utf-8") as json_file:
        kanji_data = json.load(json_file)

    for kanji_entry in kanji_data:
        cursor.execute("""
        INSERT INTO kanji (kanji, onyomi, kunyomi, meaning, level)
        VALUES (?, ?, ?, ?, ?)
        """, (
            kanji_entry["kanji"],
            json.dumps(kanji_entry["onyomi"], ensure_ascii=False) if isinstance(kanji_entry["onyomi"], list) else kanji_entry["onyomi"],
            json.dumps(kanji_entry["kunyomi"], ensure_ascii=False) if isinstance(kanji_entry["kunyomi"], list) else kanji_entry["kunyomi"],
            json.dumps(kanji_entry["meaning"], ensure_ascii=False) if isinstance(kanji_entry["meaning"], list) else kanji_entry["meaning"],
            "N5"
        ))

    conn.commit()
    conn.close()
    print("Kanji data successfully entered in the DB")

if __name__ == "__main__":
    create_database()
