from app.extensions import get_db
 
 
class Grammar:
    def __init__(self, id, romaji, japanese, meaning, level="N5"):
        self.id = id
        self.romaji = romaji
        self.japanese = japanese
        self.meaning = meaning
        self.level = level
 
    @staticmethod
    def from_row(row):
        """Convert SQLite row to Grammar instance"""

        return Grammar(
            id=row["id"],
            romaji=row["romaji"],
            japanese=row["japanese"],
            meaning=row["meaning"],
            level=row["level"],
        )
 
    # queries
 
    @classmethod
    def get_all(cls, level=None):
        """Returns all grammar points, optionally filtered by JLPT level."""

        db = get_db()
        if level:
            rows = db.execute(
                "SELECT * FROM grammar WHERE level = ? ORDER BY id",
                (level.upper(),)
            ).fetchall()
        else:
            rows = db.execute("SELECT * FROM grammar ORDER BY id").fetchall()
        return [cls.from_row(r) for r in rows]
 
    @classmethod
    def get_by_id(cls, grammar_id):
        """Returns specific grammar point by ID, or None if not found"""

        db = get_db()
        row = db.execute(
            "SELECT * FROM grammar WHERE id = ?", (grammar_id,)
        ).fetchone()
        return cls.from_row(row) if row else None
