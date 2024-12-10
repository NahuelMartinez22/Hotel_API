from models.models import Habitacion 
from config import ma


class HabitacionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Habitacion
        load_instance = True


