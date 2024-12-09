from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import models


class HabitacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Habitacion
        load_instance = True

