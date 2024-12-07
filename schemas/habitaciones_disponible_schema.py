from marshmallow import Schema, fields

class HabitacionResponseSchema(Schema):
    id = fields.Int(required=True)
    numero = fields.Int(required=True)
    precio = fields.Str(required=True)

class HabitacionesDisponiblesResponseSchema(Schema):
    habitaciones = fields.List(fields.Nested(HabitacionResponseSchema), required=True)
