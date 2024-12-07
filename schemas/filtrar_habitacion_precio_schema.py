from marshmallow import Schema, fields

class HabitacionResponseSchema(Schema):
    id = fields.Int(required=True)
    numero = fields.Int(required=True)
    precio = fields.Float(required=True)

class FiltrarHabitacionesPorPrecioResponseSchema(Schema):
    habitaciones = fields.List(fields.Nested(HabitacionResponseSchema), required=True)
