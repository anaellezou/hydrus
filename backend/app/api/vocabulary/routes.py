from flask import Blueprint, jsonify, request, abort

from .models import Vocabulary
from .schemas import vocabulary_schema, vocabulary_list_schema

vocabulary_bp = Blueprint("vocabulary", __name__)

VALID_LEVELS = {"N1", "N2", "N3", "N4", "N5"}


# GET /api/vocabulary/
# Params optionnels : ?level=N5
@vocabulary_bp.get("/")
def get_all_vocabulary():
    level = request.args.get("level", "").upper() or None

    if level and level not in VALID_LEVELS:
        abort(400, description=f"invalid level. Accepted levels : {', '.join(sorted(VALID_LEVELS))}")

    vocab_list = Vocabulary.get_all(level=level)

    result = vocabulary_list_schema.dump({
        "total": len(vocab_list),
        "level": level,
        "vocabulary": vocab_list,
    })
    return jsonify(result), 200


# GET /api/vocabulary/<int:vocab_id>
@vocabulary_bp.get("/<int:vocab_id>")
def get_vocabulary(vocab_id):
    vocab = Vocabulary.get_by_id(vocab_id)
    if vocab is None:
        abort(404, description=f"word with ID {vocab_id} not found")

    return jsonify(vocabulary_schema.dump(vocab)), 200


# handle 400 and 404 errors with a JSON response instead of HTML
@vocabulary_bp.errorhandler(400)
@vocabulary_bp.errorhandler(404)
def handle_error(e):
    return jsonify({"error": e.name, "message": e.description}), e.code
