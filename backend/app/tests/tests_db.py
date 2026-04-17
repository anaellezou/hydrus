from app.api.kanji.models import Kanji
from app.api.vocabulary.models import Vocabulary
from app.api.grammar.models import Grammar


# kanji model 
def test_get_all_kanji(app):
    """Kanji.get_all() returns all kanji"""

    with app.app_context():
        kanji_list = Kanji.get_all_kanji()
        assert len(kanji_list) == 2


def test_get_all_kanji_filtered(app):
    """Kanji.get_all_kanji(level='N5') returns only kanji of level N5"""

    with app.app_context():
        kanji_list = Kanji.get_all_kanji(level="N5")
        assert len(kanji_list) == 1
        assert kanji_list[0].kanji == "一"


def test_get_kanji_by_id(app):
    """Kanji.get_kanji_by_id(1) returns specific kanji"""

    with app.app_context():
        kanji = Kanji.get_kanji_by_id(1)
        assert kanji is not None
        assert kanji.kanji == "一"
        assert kanji.meaning == "One"
        assert kanji.level == "N5"


def test_get_kanji_by_id_not_found(app):
    """Kanji.get_kanji_by_id(9999) returns None"""

    with app.app_context():
        kanji = Kanji.get_kanji_by_id(9999)
        assert kanji is None


# vocabulary model
def test_get_all_vocabulary(app):
    """Vocabulary.get_all() returns all vocabulary"""

    with app.app_context():
        vocab_list = Vocabulary.get_all()
        assert len(vocab_list) == 1


def test_get_vocabulary_by_id(app):
    """Vocabulary.get_vocabulary_by_id(1) returns a specific word"""

    with app.app_context():
        vocab = Vocabulary.get_vocabulary_by_id(1)
        assert vocab is not None
        assert vocab.vocab == "食べる"
        assert vocab.meaning == "to eat"


def test_get_vocabulary_by_id_not_found(app):
    """Vocabulary.get_vocabulary_by_id(9999) returns None"""

    with app.app_context():
        vocab = Vocabulary.get_vocabulary_by_id(9999)
        assert vocab is None


# Grammar Model 
def test_get_all_grammar(app):
    """Grammar.get_all() returns all grammar points"""

    with app.app_context():
        grammar_list = Grammar.get_all()
        assert len(grammar_list) == 1


def test_get_grammar_by_id(app):
    """Grammar.get_vocabulary_by_id(1) returns a specific grammar point"""

    with app.app_context():
        grammar = Grammar.get_vocabulary_by_id(1)
        assert grammar is not None
        assert grammar.romaji == "desu"
        assert grammar.meaning == "to be"


def test_get_grammar_by_id_not_found(app):
    """Grammar.get_vocabulary_by_id(9999) returns None"""

    with app.app_context():
        grammar = Grammar.get_vocabulary_by_id(9999)
        assert grammar is None
