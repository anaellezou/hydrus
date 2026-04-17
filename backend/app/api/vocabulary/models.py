from app.extensions import get_db


class Vocabulary:
    def __init__(self, id, vocab, romaji, hiragana, type, meaning, level="N5"):
        self.id = id
        self.vocab = vocab
        self.romaji = romaji
        self.hiragana = hiragana
        self.type = type
        self.meaning = meaning
        self.level = level

    @staticmethod
    def from_row(row):
        """convert SQLite row in Vocabulary instance"""

        return Vocabulary(
            id=row["id"],
            vocab=row["vocab"],
            romaji=row["romaji"],
            hiragana=row["hiragana"],
            type=row["type"],
            meaning=row["meaning"],
            level=row["level"],
        )

    # queries

    @classmethod
    def get_all(cls, level=None):
        """ return all vocabulary, filtered by JLPT level if specified """

        db = get_db()
        if level:
            rows = db.execute(
                "SELECT * FROM vocabulary WHERE level = ? ORDER BY id",
                (level.upper(),)
            ).fetchall()
        else:
            rows = db.execute("SELECT * FROM vocabulary ORDER BY id").fetchall()
        return [cls.from_row(r) for r in rows]

    @classmethod
    def get_vocabulary_by_id(cls, vocab_id):
        """return a specific word by its ID, or None if it doesnt exist"""

        db = get_db()
        row = db.execute(
            "SELECT * FROM vocabulary WHERE id = ?", (vocab_id,)
        ).fetchone()
        return cls.from_row(row) if row else None
