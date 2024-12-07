from marshmallow import Schema, fields

class DesactivarHabitacionResponseSchema(Schema):
    mensaje = fields.Str(required=True)
