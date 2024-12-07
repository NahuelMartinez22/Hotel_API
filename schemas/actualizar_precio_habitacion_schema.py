from marshmallow import Schema, fields

class ActualizarPrecioHabitacionSchema(Schema):
    precio = fields.Float(required=True)
