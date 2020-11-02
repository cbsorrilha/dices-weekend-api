from marshmallow import Schema, fields


class DiceSchema(Schema):
    diceType = fields.Integer()
    value = fields.Integer()


class ResultSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    mode = fields.Str()
    modifier = fields.Integer()
    created = fields.DateTime()
    result = fields.Integer()
    dices = fields.List(fields.Nested(DiceSchema))
