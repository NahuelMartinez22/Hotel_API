from dataclasses import fields
from marshmallow import Schema, fields

class RegistroSchema(Schema):
    usuario = fields.Str(required=True)
    categoria = fields.Str(required=True)
    clave1 = fields.Str(required=True)
    clave2 = fields.Str(required=True)
    
    
    
    
    