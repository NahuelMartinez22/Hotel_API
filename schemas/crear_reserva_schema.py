from marshmallow import Schema, fields

class CrearReservaSchema(Schema):
    inicio = fields.Date(required=True)
    fin = fields.Date(required=True)
    habitacion = fields.Int(required=True) 
