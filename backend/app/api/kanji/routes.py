from flask import Blueprint, jsonify, request, abort

from .models import Kanji
from .schemas import kanji_schema, kanji_list_schema

kanji_bp = Blueprint("kanji", __name__)

VALID_LEVELS = {"N1", "N2", "N3", "N4", "N5"}


@kanji_bp.get("/")
def get_all_kanji():
    """ Get all kanji, optionally filtered by JLPT level. """

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


@kanji_bp.get("/<int:kanji_id>")
def get_kanji(kanji_id):
    """ Get a specific kanji by its ID. """

    kanji = Kanji.get_kanji_by_id(kanji_id)
    if kanji is None:
        abort(404, description=f"Kanji with id {kanji_id} does not exist.")

    return jsonify(kanji_schema.dump(kanji)), 200


@kanji_bp.errorhandler(400)
@kanji_bp.errorhandler(404)
def handle_error(e):
    return jsonify({"error": e.name, "message": e.description}), e.code