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



#usuario

from dbConfig import db
from models import Usuario

def mostrar_usuarios():
    usuarios = db.session.query(Usuario).all()
    for usuario in usuarios:
        print(f"ID: {usuario.id}, Usuario: {usuario.usuario}, Categoría: {usuario.categoria}")



def filtrar_usuarios(categoria=None, nombre_usuario=None):
    query = db.session.query(Usuario)
    
    if categoria:
        query = query.filter(Usuario.categoria == categoria)
    if nombre_usuario:
        query = query.filter(Usuario.usuario.like(f"%{nombre_usuario}%"))
    
    usuarios = query.all()
    for usuario in usuarios:
        print(f"ID: {usuario.id}, Usuario: {usuario.usuario}, Categoría: {usuario.categoria}")
filtrar_usuarios(categoria="Administrador")  # Filtrar por categoría
filtrar_usuarios(nombre_usuario="Juan")      # Buscar usuarios cuyo nombre contenga "Juan"


def editar_usuario(usuario_id, nuevo_usuario=None, nueva_categoria=None, nueva_clave=None):
    usuario = db.session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        print("Usuario no encontrado.")
        return
    
    if nuevo_usuario:
        usuario.usuario = nuevo_usuario
    if nueva_categoria:
        usuario.categoria = nueva_categoria
    if nueva_clave:
        from werkzeug.security import generate_password_hash
        usuario.clave = generate_password_hash(nueva_clave)
    
    db.session.commit()
    print(f"Usuario ID {usuario_id} actualizado correctamente.")

editar_usuario(1, nuevo_usuario="admin123", nueva_clave="nueva_clave_segura")  # Cambiar nombre de usuario y clave

def eliminar_usuario(usuario_id):
    usuario = db.session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        print("Usuario no encontrado.")
        return
    
    db.session.delete(usuario)
    db.session.commit()
    print(f"Usuario ID {usuario_id} eliminado correctamente.")



def mostrar_usuario_por_id(usuario_id):
    # Consultar el usuario por ID
    usuario = db.session.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    # Verificar si el usuario existe
    if not usuario:
        print(f"Usuario con ID {usuario_id} no encontrado.")
        return
    
    # Mostrar información del usuario
    print(f"ID: {usuario.id}")
    print(f"Usuario: {usuario.usuario}")
    print(f"Categoría: {usuario.categoria}")
