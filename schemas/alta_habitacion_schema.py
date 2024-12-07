from marshmallow import Schema, fields

class AltaHabitacionSchema(Schema):
    numero = fields.Int(required=True)
    precio = fields.Float(required=True)