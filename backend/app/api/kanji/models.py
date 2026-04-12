import sqlite3
from app.extensions import get_db

class Kanji:
    def __init__(self, id, kanji, meaning, onyomi, kunyomi, level="N5"):
        self.id = id
        self.kanji = kanji
        self.meaning = meaning
        self.onyomi = onyomi
        self.kunyomi = kunyomi
        self.level = level

    @staticmethod
    def from_row(row):
        return Kanji(
            id=row["id"],
            kanji=row["kanji"],
            meaning=row["meaning"],
            onyomi=row["onyomi"],
            kunyomi=row["kunyomi"],
            level=row["level"]
        )

    
    # queries

    @classmethod
    def get_all_kanji(cls, level=None):
        """ Return all kanji, optionally filtered by JLPT level """

        db = get_db()
        if level:
            rows = db.execute(
                "SELECT * FROM kanji WHERE level = ? ORDER BY id",
                (level.upper(),)
            ).fetchall()
        else:
            rows = db.execute("SELECT * FROM kanji ORDER BY id").fetchall()

        return [cls.from_row(row) for row in rows]


    @classmethod
    def get_kanji_by_id(cls, kanji_id):
        """ Return a specific kanji by its ID """

        db = get_db()
        row = db.execute(
            "SELECT * FROM kanji WHERE id = ?",
            (kanji_id,)
        ).fetchone()

        return cls.from_row(row) if row else None
