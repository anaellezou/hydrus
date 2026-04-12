from marshmallow import Schema, fields, validate


class ReadingSchema(Schema):
    romaji   = fields.Str(dump_only=True)
    hiragana = fields.Str(dump_only=True)


class VocabularySchema(Schema):
    id       = fields.Int(dump_only=True)
    vocab    = fields.Str(required=True)
    reading  = fields.Method("get_reading", dump_only=True)
    type     = fields.Str(dump_only=True)
    meaning  = fields.Str(required=True)
    level    = fields.Str(
        load_default="N5",
        validate=validate.OneOf(["N5", "N4", "N3", "N2", "N1"]),
    )

    def get_reading(self, obj):
        """group romaji and hiragana into a single 'reading' field in the output"""

        return {
            "romaji":   obj.romaji,
            "hiragana": obj.hiragana,
        }


class VocabularyListSchema(Schema):
    """wrapper for a list of vocabulary, with metadata like total count and level filter"""

    total      = fields.Int(dump_only=True)
    level      = fields.Str(dump_only=True, allow_none=True)
    vocabulary = fields.List(fields.Nested(VocabularySchema), dump_only=True)


# reusable schemas
vocabulary_schema      = VocabularySchema()
vocabulary_list_schema = VocabularyListSchema()
