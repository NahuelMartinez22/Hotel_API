from marshmallow import Schema, fields

class ActivarHabitacionResponseSchema(Schema):
    mensaje = fields.Str(required=True)
