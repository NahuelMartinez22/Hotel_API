from marshmallow import Schema, fields

class HabitacionResponseSchema(Schema):
    numero = fields.Int(required=True)
    estado = fields.Str(required=True)

class BuscarHabitacionesPorFechaResponseSchema(Schema):
    cantidad = fields.Int(required=True)
    habitaciones = fields.List(fields.Nested(HabitacionResponseSchema), required=True)
