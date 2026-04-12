from marshmallow import Schema, fields, validate
 
 
class GrammarSchema(Schema):
    id       = fields.Int(dump_only=True)
    romaji   = fields.Str(required=True)
    japanese = fields.Str(required=True)
    meaning  = fields.Str(required=True)
    level    = fields.Str(
        load_default="N5",
        validate=validate.OneOf(["N5", "N4", "N3", "N2", "N1"]),
    )
 
 
class GrammarListSchema(Schema):
    """wrapper for list of grammar points, with metadata"""

    total   = fields.Int(dump_only=True)
    level   = fields.Str(dump_only=True, allow_none=True)
    grammar = fields.List(fields.Nested(GrammarSchema), dump_only=True)
 
 
# reusable schema instances
grammar_schema      = GrammarSchema()
grammar_list_schema = GrammarListSchema()
 