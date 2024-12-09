from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import models

class ReservaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Reserva
        load_instance = True
