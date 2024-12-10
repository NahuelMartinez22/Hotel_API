from flask import Flask
from flask_cors import CORS
from models.models import db
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)
CORS(app)

# Configuración para la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SECRET_KEY'
application = app


#comente la linea de abajo para que conecte con el postgre local, este es para el de docker
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:1920@db:5432/hotel_base')

#este es para probar local con tus datos cambiar con lo de tu config de postgre
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1920@localhost:5432/hotel_base'

# Inicialización de la base de datos con la app
db.init_app(app)


ma = Marshmallow(app)

with app.app_context():
    db.create_all()  # Esto crea todas las tablas definidas en tus modelos
