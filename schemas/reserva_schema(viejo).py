from marshmallow import Schema, fields

class ReservaSchema(Schema):
    id = fields.Int()
    numero  = fields.Int()
    inicio = fields.Str()
    fin = fields.Str()
    habitacion = fields.Int()
    usuario = fields.Str() 
