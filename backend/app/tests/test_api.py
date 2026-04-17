import json

# Health check 
def test_health(client):
    """GET /api/health returns 200 and status ok"""

    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


# Tests kanji 
def test_get_all_kanji(client):
    """GET /api/kanji/ returns all kanji"""

    res = client.get("/api/kanji/")
    assert res.status_code == 200
    data = res.get_json()
    assert "kanji" in data
    assert "total" in data
    assert data["total"] == 2


def test_get_kanji_filtered_by_level(client):
    """GET /api/kanji/?level=N5 returns only kanji of level N5"""
    res = client.get("/api/kanji/?level=N5")
    assert res.status_code == 200
    data = res.get_json()
    assert data["total"] == 1
    assert data["kanji"][0]["kanji"] == "一"


def test_get_kanji_invalid_level(client):
    """GET /api/kanji/?level=N9 retutns 400 for invalid level"""

    res = client.get("/api/kanji/?level=N9")
    assert res.status_code == 400
    data = res.get_json()
    assert "error" in data


def test_get_kanji_by_id(client):
    """GET /api/kanji/1 returns specific kanji"""

    res = client.get("/api/kanji/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["kanji"] == "一"
    assert data["meaning"] == "One"


def test_get_kanji_not_found(client):
    """GET /api/kanji/9999 returns 404"""
    res = client.get("/api/kanji/9999")
    assert res.status_code == 404
    data = res.get_json()
    assert "error" in data


# Test vocabulary 
def test_get_all_vocabulary(client):
    """GET /api/vocabulary/ returns all vocabulary"""

    res = client.get("/api/vocabulary/")
    assert res.status_code == 200
    data = res.get_json()
    assert "vocabulary" in data
    assert data["total"] == 1


def test_get_vocabulary_by_id(client):
    """GET /api/vocabulary/1 returns a specific word"""

    res = client.get("/api/vocabulary/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["vocab"] == "食べる"
    assert data["meaning"] == "to eat"


def test_get_vocabulary_not_found(client):
    """GET /api/vocabulary/9999 returns 404"""

    res = client.get("/api/vocabulary/9999")
    assert res.status_code == 404


# Tests grammar 
def test_get_all_grammar(client):
    """GET /api/grammar/ returns all grammar points"""

    res = client.get("/api/grammar/")
    assert res.status_code == 200
    data = res.get_json()
    assert "grammar" in data
    assert data["total"] == 1


def test_get_grammar_by_id(client):
    """GET /api/grammar/1 returns a specific grammar point"""

    res = client.get("/api/grammar/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["romaji"] == "desu"
    assert data["meaning"] == "to be"


def test_get_grammar_not_found(client):
    """GET /api/grammar/9999 returns 404"""

    res = client.get("/api/grammar/9999")
    assert res.status_code == 404
