from marshmallow import Schema, fields

"""class HabitacionSchema(Schema):
    id = fields.Int(required=True)
    numero_habitacion = fields.Int(required=True, attribute="numero")
    precio = fields.Float(required=True)
    estado = fields.Int(required=True)
    """
    

class HabitacionSchema(Schema):
    id = fields.Int(required=True)
    numero_habitacion = fields.Int(required=True, attribute="numero")
    precio = fields.Float(required=True)
    estado = fields.String(required=True)  

    
    def make_state(self, obj):
        return "activa" if obj.estado == 1 else "desactivada"
    
    # Aquí usamos la función 'make_state' al serializar
    def dump(self, obj, many=False):
        result = super().dump(obj, many=many)
        if many:
            for item in result:
                item['estado'] = self.make_state(item)
        else:
            result['estado'] = self.make_state(result)
        return result

