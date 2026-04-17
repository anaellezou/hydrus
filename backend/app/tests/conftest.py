import pytest
import sqlite3
from app import create_app


# config
class TestConfig:
    TESTING = True
    DATABASE = ":memory:"
    SECRET_KEY = "test"


# setup DB in memory with test data
def init_test_db(db):
    """Create tables and insert test data into the DB"""

    db.executescript("""
        CREATE TABLE IF NOT EXISTS kanji (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            kanji    TEXT NOT NULL,
            onyomi   TEXT,
            kunyomi  TEXT,
            meaning  TEXT,
            level    TEXT DEFAULT 'N5'
        );
        CREATE TABLE IF NOT EXISTS vocabulary (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            vocab    TEXT NOT NULL,
            romaji   TEXT,
            hiragana TEXT,
            type     TEXT,
            meaning  TEXT,
            level    TEXT DEFAULT 'N5'
        );
        CREATE TABLE IF NOT EXISTS grammar (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            romaji   TEXT NOT NULL,
            japanese TEXT,
            meaning  TEXT,
            level    TEXT DEFAULT 'N5'
        );

        INSERT INTO kanji (kanji, onyomi, kunyomi, meaning, level)
        VALUES ('一', 'いちichi', 'ひとhito', 'One', 'N5');

        INSERT INTO kanji (kanji, onyomi, kunyomi, meaning, level)
        VALUES ('二', 'にni', 'ふたfuta', 'Two', 'N4');

        INSERT INTO vocabulary (vocab, romaji, hiragana, type, meaning, level)
        VALUES ('食べる', 'taberu', 'たべる', 'Verb', 'to eat', 'N5');

        INSERT INTO grammar (romaji, japanese, meaning, level)
        VALUES ('desu', 'です', 'to be', 'N5');
    """)
    db.commit()


# Fixtures 
@pytest.fixture
def app(monkeypatch):
    """Create an instance of the app with a test config and patch get_db to use the DB"""

    app = create_app(TestConfig)

    # DB in memory for testing
    test_db = sqlite3.connect(":memory:", check_same_thread=False)
    test_db.row_factory = sqlite3.Row
    init_test_db(test_db)

    get_db = lambda: test_db

    # Patch get_db in every model module to use the test DB connection
    import app.api.kanji.models as kanji_models
    import app.api.vocabulary.models as vocab_models
    import app.api.grammar.models as grammar_models

    monkeypatch.setattr(kanji_models, "get_db", get_db)
    monkeypatch.setattr(vocab_models, "get_db", get_db)
    monkeypatch.setattr(grammar_models, "get_db", get_db)

    yield app

    test_db.close()


@pytest.fixture
def client(app):
    """Client HTTP for testing the app's routes"""

    return app.test_client()
