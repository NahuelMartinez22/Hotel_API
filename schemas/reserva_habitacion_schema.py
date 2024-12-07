from marshmallow import Schema, fields

class ReservaSchema(Schema):
    id = fields.Int(required=True)
    inicio = fields.Str(required=True)
    fin = fields.Str(required=True)
    usuario = fields.Str(required=True) 

class HabitacionEstadoSchema(Schema):
    id = fields.Int(required=True)
    numero = fields.Int(required=True)
    precio = fields.Str(required=True) 
    reservas = fields.List(fields.Nested(ReservaSchema), required=True)