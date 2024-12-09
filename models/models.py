from dbConfig import db
from werkzeug.security import generate_password_hash


# Modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), unique=True)
    categoria = db.Column(db.String(100))  
    clave = db.Column(db.String(200))  
    
    def __init__(self, usuario, categoria, clave):
        self.usuario = usuario
        self.categoria = categoria  
        self.clave = generate_password_hash(clave)

# Modelo de Habitacion
class Habitacion(db.Model):
    __tablename__ = 'habitacion'
    id = db.Column(db.Integer, primary_key=True)
    numero_habitacion = db.Column(db.Integer, nullable=False, unique=True)
    precio = db.Column(db.Float, nullable=False)
    estado = db.Column(db.Integer, nullable=False, default=1)
    
    def __init__(self, numero_habitacion, precio):
        self.numero_habitacion = numero_habitacion
        self.precio = precio

# Modelo de Reserva
class Reserva(db.Model):
    __tablename__ = 'reserva'
    id = db.Column(db.Integer, primary_key=True)
    id_habitacion = db.Column(db.Integer, db.ForeignKey('habitacion.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_inicio_hospedaje = db.Column(db.Date, nullable=False)
    fecha_fin_hospedaje = db.Column(db.Date, nullable=False)

    habitacion = db.relationship('Habitacion', backref='reservas')
    usuario = db.relationship('Usuario', backref='reservas')

    def __init__(self, id_habitacion, id_usuario, fecha_inicio_hospedaje, fecha_fin_hospedaje):
        self.id_habitacion = id_habitacion
        self.id_usuario = id_usuario
        self.fecha_inicio_hospedaje = fecha_inicio_hospedaje
        self.fecha_fin_hospedaje = fecha_fin_hospedaje
