from models import Usuario, Habitacion, Reserva
from dbConfig import db
from datetime import datetime
from werkzeug.security import check_password_hash

def validacionFechasHospedaje(fechaInicio, fechaFin):
    if fechaFin < fechaInicio:
        return False
    return True

def disponibilidadHabitacion(idHabitacion, fechaInicio, fechaFin):
    try:
        reservas = db.session.query(Reserva).filter(
            Reserva.id_habitacion == idHabitacion,
            db.or_(Reserva.fecha_inicio_hospedaje.between(fechaInicio, fechaFin),
                   Reserva.fecha_fin_hospedaje.between(fechaInicio, fechaFin))
        ).all()
        
        return len(reservas) == 0

    except Exception as e:
        print(f"Error al verificar disponibilidad: {e}")
        return False

def validarUsuario(usuario, clave):
    try:

        usuario_encontrado = db.session.query(Usuario).filter_by(usuario=usuario).first()

        if usuario_encontrado and check_password_hash(usuario_encontrado.clave, clave):
            return usuario_encontrado

        print("Credenciales inválidas")
        return None
    except Exception as e:
        print(f"Error al validar usuario: {e}")
        return None


def validarExistenciaHabitacion(numero_habitacion):
    try:
        habitacion = db.session.query(Habitacion).filter_by(numero_habitacion=numero_habitacion).first()
        return habitacion is None

    except Exception as e:
        print(f"Error al validar existencia de la habitacion: {e}")
        return False


def habitacion_existe(idHabitacion):
    try:
        habitacion = db.session.query(Habitacion).filter_by(id=idHabitacion).first()
        return habitacion is not None
    except Exception as e:
        print(f"Error al verificar existencia de habitacion: {e}")
        return False

def habitacion_por_id(numero_habitacion):
    try:
        reservas = db.session.query(Reserva).filter(
            Reserva.id_habitacion == numero_habitacion
        ).all()
        
        return reservas

    except Exception as e:
        print(f"Error al validar reservas de la habitacion: {e}")
        return False

def usuario_por_id(id_usuario):
    usuario = db.session.query(Usuario).filter_by(id=id_usuario).first()
    if usuario:
        return usuario.usuario 
    return "Desconocido"


def validar_fecha_formato(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def obtener_reservas():
    try:
        reservas = db.session.query(Reserva, Habitacion).join(
            Habitacion, Reserva.id_habitacion == Habitacion.id  
        ).order_by(Habitacion.numero_habitacion, Reserva.fecha_inicio_hospedaje).all()

        resultado = []
        for reserva, habitacion in reservas:
            resultado.append({
                "id": reserva.id,
                "numero": habitacion.numero_habitacion,  
                "inicio": reserva.fecha_inicio_hospedaje.strftime('%Y-%m-%d'),
                "fin": reserva.fecha_fin_hospedaje.strftime('%Y-%m-%d') 
            })

        return resultado

    except Exception as e:
        print(f"Error al obtener reservas: {e}")
        return None

def validar_existencia_habitacion(numero_habitacion):
    habitacion_existente = db.session.query(Habitacion).filter_by(numero_habitacion=numero_habitacion).first()
    return habitacion_existente is not None

def validar_precio(precio):
    return precio > 0
