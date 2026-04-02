from flask import Blueprint, jsonify, request, abort

from .models import Kanji
from .schemas import kanji_schema, kanji_list_schema

kanji_bp = Blueprint("kanji", __name__)

VALID_LEVELS = {"N1", "N2", "N3", "N4", "N5"}


@kanji_bp.get("/")
def get_all_kanji():
    level = request.args.get("level", "").upper() or None

    if level and level not in VALID_LEVELS:
        abort(400, description=f"Invalid level, select a valid level : {', '.join(sorted(VALID_LEVELS))}")

    kanji_list = Kanji.get_all_kanji(level=level)

    result = kanji_list_schema.dump({
        "total": len(kanji_list),
        "level": level,
        "kanji": kanji_list,
    })
    return jsonify(result), 200


@kanji_bp.get("/random")
def get_random_kanji():
    level = request.args.get("level", "").upper() or None
    try:
        count = int(request.args.get("count", 1))
        if count < 1 or count > 50:
            raise ValueError
    except ValueError:
        abort(400, description="the count parameter must be between 1 et 50.")

    if level and level not in VALID_LEVELS:
        abort(400, description=f"Invalid level, levels available : {', '.join(sorted(VALID_LEVELS))}")

    kanji_list = Kanji.get_random(level=level, count=count)

    result = kanji_list_schema.dump({
        "total": len(kanji_list),
        "level": level,
        "kanji": kanji_list,
    })
    return jsonify(result), 200


@kanji_bp.get("/search")
def search_kanji():
    query = request.args.get("q", "").strip()
    if not query:
        abort(400, description="q parameter is required.")

    kanji_list = Kanji.search(query)

    result = kanji_list_schema.dump({
        "total": len(kanji_list),
        "level": None,
        "kanji": kanji_list,
    })
    return jsonify(result), 200


@kanji_bp.get("/<int:kanji_id>")
def get_kanji(kanji_id):
    kanji = Kanji.get_kanji_by_id(kanji_id)
    if kanji is None:
        abort(404, description=f"Kanji with id {kanji_id} does not exist.")

    return jsonify(kanji_schema.dump(kanji)), 200


@kanji_bp.errorhandler(400)
@kanji_bp.errorhandler(404)
def handle_error(e):
    return jsonify({"error": e.name, "message": e.description}), e.code