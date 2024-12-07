from marshmallow import Schema, fields

class LoginSchema(Schema):
    usuario = fields.Str(required=True)
    clave = fields.Str(required=True)