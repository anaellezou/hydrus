from flask import Blueprint, jsonify, request, abort

from .models import Grammar
from .schemas import grammar_schema, grammar_list_schema

grammar_bp = Blueprint("grammar", __name__)

VALID_LEVELS = {"N1", "N2", "N3", "N4", "N5"}


# GET /api/grammar/
# Params optionnels : ?level=N5
@grammar_bp.get("/")
def get_all_grammar():

    level = request.args.get("level", "").upper() or None

    if level and level not in VALID_LEVELS:
        abort(400, description=f"invalid level. Accepted levels : {', '.join(sorted(VALID_LEVELS))}")

    grammar_list = Grammar.get_all(level=level)

    result = grammar_list_schema.dump({
        "total": len(grammar_list),
        "level": level,
        "grammar": grammar_list,
    })
    return jsonify(result), 200


# GET /api/grammar/search
# Params requis : ?q=<query>
@grammar_bp.get("/search")
def search_grammar():

    query = request.args.get("q", "").strip()
    if not query:
        abort(400, description="'q' parameter is required")

    grammar_list = Grammar.search(query)

    result = grammar_list_schema.dump({
        "total": len(grammar_list),
        "level": None,
        "grammar": grammar_list,
    })
    return jsonify(result), 200


# GET /api/grammar/<int:grammar_id>
@grammar_bp.get("/<int:grammar_id>")
def get_grammar(grammar_id):

    grammar = Grammar.get_by_id(grammar_id)
    if grammar is None:
        abort(404, description=f"grammar point with ID {grammar_id} not found")

    return jsonify(grammar_schema.dump(grammar)), 200


# manage local blueprint errors for cleaner JSON responses
@grammar_bp.errorhandler(400)
@grammar_bp.errorhandler(404)
def handle_error(e):
    return jsonify({"error": e.name, "message": e.description}), e.code
