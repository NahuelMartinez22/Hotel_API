from models.models import Habitacion 
from config import ma
from marshmallow import Schema, fields, ValidationError, validates


class HabitacionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Habitacion
        load_instance = True


class AltaHabitacionSchema(Schema):
    numero = fields.Integer(required=True)  
    precio = fields.Float(required=True)

    @validates('numero')
    def validar_numero_habitacion(self, value):
        if value <= 0:
            raise ValidationError("El número de habitación debe ser un entero positivo.")
        if Habitacion.query.filter_by(numero_habitacion=value).first():
            raise ValidationError("Ya existe una habitación con ese número.")

    @validates('precio')
    def validar_precio(self, value):
        if value <= 0:
            raise ValidationError("El precio debe ser un número positivo.")