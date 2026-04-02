from marshmallow import Schema, fields, validate, ValidationError

class KanjiSchema(Schema):
    id = fields.Int(dump_only=True)
    character = fields.Str(required=True)
    meaning = fields.Str(required=True)
    onyomi = fields.Str(required=True, data_key="onReading")
    kunyomi = fields.Str(required=True, data_key="kunReading")
    level = fields.Str(
        load_default="N5",
        validate=validate.OneOf(["N5", "N4", "N3", "N2", "N1"]),
    )


class KanjiListSchema(Schema):
    """ wrapper for a list of kanji """
    total = fields.Int(dump_only=True)
    level = fields.Str(dump_only=True, allow_none=True)
    kanji = fields.List(fields.Nested(KanjiSchema), dump_only=True)


kanji_schema = KanjiSchema()
kanji_list_schema = KanjiListSchema()
