from dbConfig import db
from models import Habitacion

def mostrar_habitaciones():
    habitaciones = db.session.query(Habitacion).all()
    for habitacion in habitaciones:
        print(f"ID: {habitacion.id}, Número: {habitacion.numero_habitacion}, Precio: {habitacion.precio}, Estado: {habitacion.estado}")

def filtrar_habitaciones(precio_min, precio_max, estado=None):
    query = db.session.query(Habitacion).filter(
        Habitacion.precio >= precio_min,
        Habitacion.precio <= precio_max
    )
    if estado is not None:
        query = query.filter(Habitacion.estado == estado)
    
    habitaciones = query.all()
    for habitacion in habitaciones:
        print(f"ID: {habitacion.id}, Número: {habitacion.numero_habitacion}, Precio: {habitacion.precio}, Estado: {habitacion.estado}")
        filtrar_habitaciones(1000, 5000, estado=1)  # Filtrar habitaciones disponibles con precio entre 1000 y 5000


def editar_habitacion(habitacion_id, nuevo_numero=None, nuevo_precio=None, nuevo_estado=None):
    habitacion = db.session.query(Habitacion).filter(Habitacion.id == habitacion_id).first()
    if not habitacion:
        print("Habitación no encontrada.")
        return
    
    if nuevo_numero is not None:
        habitacion.numero_habitacion = nuevo_numero
    if nuevo_precio is not None:
        habitacion.precio = nuevo_precio
    if nuevo_estado is not None:
        habitacion.estado = nuevo_estado
    
    db.session.commit()
    print(f"Habitación ID {habitacion_id} actualizada correctamente.")
editar_habitacion(1, nuevo_precio=4500, nuevo_estado=0)  # Actualizar precio y marcar como no disponible

def eliminar_habitacion(habitacion_id):
    habitacion = db.session.query(Habitacion).filter(Habitacion.id == habitacion_id).first()
    if not habitacion:
        print("Habitación no encontrada.")
        return
    
    db.session.delete(habitacion)
    db.session.commit()
    print(f"Habitación ID {habitacion_id} eliminada correctamente.")
eliminar_habitacion(3)  # Eliminar la habitación con ID 3



