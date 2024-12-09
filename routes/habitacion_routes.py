from datetime import datetime
from flask import Blueprint, jsonify, request
import jwt
from marshmallow import ValidationError
from models.models import Habitacion , Reserva
from schemas.activar_mensaje_habitacion_schema import ActivarHabitacionResponseSchema
from schemas.actualizar_precio_habitacion_schema import ActualizarPrecioHabitacionSchema
from schemas.alta_habitacion_schema import AltaHabitacionSchema
from schemas.deshabilitar_habitacion_shcema import DesactivarHabitacionResponseSchema
from schemas.habitacion_por_fecha_schema import BuscarHabitacionesPorFechaResponseSchema
from schemas.habitacion_schema import HabitacionSchema
from schemas.reserva_habitacion_schema import HabitacionEstadoSchema
import validaciones
from routes.usuario_routes import rutaProtegida
from dbConfig import db
from config import app

habitacion_bp = Blueprint('habitacion_bp', __name__)

habitacion_schema = HabitacionSchema()


# ------------------------ENDPOINT HABITACIONES: Ruta para dar de alta habitacion ----------    

@habitacion_bp.route('/habitaciones', methods=['POST'])
@rutaProtegida(categoria_esperada='empleado')
def alta_habitacion():
    try:
        schema = AltaHabitacionSchema()
        data = request.get_json()
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return jsonify({"mensaje": "Datos no válidos", "errors": err.messages}), 400

        numero = validated_data['numero']
        precio = validated_data['precio']

        if validaciones.validar_existencia_habitacion(numero):
            return jsonify({"mensaje": "Error: Ya existe una habitacion con ese número."}), 400

        if not validaciones.validar_precio(precio):
            return jsonify({"mensaje": "Error: El precio debe ser un número positivo."}), 400

        nueva_habitacion = Habitacion(numero_habitacion=numero, precio=precio)
        db.session.add(nueva_habitacion)
        db.session.commit()

        return jsonify({"mensaje": "habitacion registrada exitosamente."}), 201

    except Exception as e:
        return jsonify({"mensaje": f"Error al registrar la habitacion: {str(e)}"}), 500
    
    
# ------------------------ENDPOINT HABITACIONES: Ruta para editar una habitacion ----------    
@habitacion_bp.route('/habitaciones/<int:id>/precio', methods=['PUT'])
@rutaProtegida(categoria_esperada='empleado')
def actualizar_precio_habitacion(id):
    try:

        data = request.get_json()

        schema = ActualizarPrecioHabitacionSchema()
        errors = schema.validate(data)
        if errors:
            return jsonify({"mensaje": "Errores en los datos", "errores": errors}), 400

        nuevo_precio = data['precio']

        habitacion = db.session.query(Habitacion).filter_by(id=id).first()

        if not habitacion:
            return jsonify({"mensaje": "Error: La habitacion no existe."}), 404

        habitacion.precio = nuevo_precio
        db.session.commit()

        return jsonify({"mensaje": "Precio de la habitacion actualizado exitosamente."}), 200

    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 500
    
    
# ------------------------ENDPOINT HABITACIONES: Ruta obtener habitacion ----------    
@habitacion_bp.route('/habitaciones', methods=['GET'])
@rutaProtegida(categoria_esperada='empleado')
def obtener_habitaciones():
    try:
        habitaciones = db.session.query(Habitacion).all()

        
        habitaciones_respuesta = [
            {
                "id": habitacion.id,
                "numero": habitacion.numero_habitacion,
                "precio": habitacion.precio,
                "activa": True if habitacion.estado == 1 else False  
            }
            for habitacion in habitaciones
        ]

        cantidad_habitaciones = len(habitaciones_respuesta)

        return jsonify({
            "habitaciones": habitaciones_respuesta,
            "cantidad": cantidad_habitaciones
        })

    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 500


    
# ------------------------ENDPOINT HABITACIONES: Ruta obtener estado habitacion ---------- 

@habitacion_bp.route('/habitaciones/<int:id>', methods=['GET'])
@rutaProtegida(categoria_esperada='empleado')
def obtener_estado_habitaciones(id):
    try:
        habitacion = db.session.query(Habitacion).filter_by(id=id).first()

        if not habitacion:
            return jsonify({"mensaje": "La habitacion no existe."}), 404

        reservas_por_id = validaciones.habitacion_por_id(id)
        
        auth_header = request.headers.get('n-auth')
        if auth_header and auth_header.startswith("bearer "):
            token = auth_header.replace("bearer ", "")
        else:
            return jsonify({"mensaje": "Token no proporcionado o inválido."}), 401
        
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        id_usuario = payload['id']
        
        nombres_usuario = validaciones.usuario_por_id(id_usuario)

        habitaciones_respuesta = {
            "id": habitacion.id,
            "numero": habitacion.numero_habitacion,
            "precio": str(habitacion.precio), 
            "reservas": [
                {
                    "id": reserva.id,
                    "inicio": reserva.fecha_inicio_hospedaje.strftime("%Y-%m-%d"),
                    "fin": reserva.fecha_fin_hospedaje.strftime("%Y-%m-%d"),
                    # "usuario": nombres_usuario.get(reserva.id_usuario, "Desconocido"),
                    "usuario": validaciones.usuario_por_id(reserva.id_usuario)
                }
                for reserva in reservas_por_id
            ]
        }

        schema = HabitacionEstadoSchema()
        habitacion_serializada = schema.dump(habitaciones_respuesta)

        return jsonify(habitacion_serializada), 200

    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 500
    
# ------------------------ENDPOINT HABITACIONES: Para habilitar una habitacion
@habitacion_bp.route('/habitaciones/<int:id>', methods=['POST'])
@rutaProtegida(categoria_esperada='empleado')
def activar_habitacion(id):
    try:
        habitacion = db.session.query(Habitacion).filter_by(id=id).first()

        if not habitacion:
            error_schema = ActivarHabitacionResponseSchema()
            return jsonify(error_schema.dump({"mensaje": "Habitacion no encontrada"})), 404

        habitacion.estado = 1

        db.session.commit()

        success_schema = ActivarHabitacionResponseSchema()
        return jsonify(success_schema.dump({"mensaje": "Habitacion activada exitosamente"})), 200

    except Exception as e:
        error_schema = ActivarHabitacionResponseSchema()
        return jsonify(error_schema.dump({"mensaje": f"Error: {str(e)}"})), 500
    
# ------------------------ENDPOINT HABITACIONES: Para desabilitar una habitacion
@habitacion_bp.route('/habitaciones/<int:id>', methods=['DELETE'])
@rutaProtegida(categoria_esperada='empleado')
def desactivar_habitacion(id):
    try:
        habitacion = db.session.query(Habitacion).filter_by(id=id).first()

        if not habitacion:
            error_schema = DesactivarHabitacionResponseSchema()
            return jsonify(error_schema.dump({"mensaje": "Habitacion no encontrada"})), 404

        habitacion.estado = 0

        db.session.commit()

        success_schema = DesactivarHabitacionResponseSchema()
        return jsonify(success_schema.dump({"mensaje": "Habitacion desactivada exitosamente"})), 200

    except Exception as e:
        error_schema = DesactivarHabitacionResponseSchema()
        return jsonify(error_schema.dump({"mensaje": f"Error: {str(e)}"})), 500
    

# ------------------------ENDPOINT HABITACIONES: Ruta resumen diario----------   
@habitacion_bp.route('/habitaciones/diario', methods=['GET'])
@rutaProtegida(categoria_esperada='empleado')
def buscar_habitaciones_por_fecha():
    try:

        fecha_str = request.args.get('fecha')
        if not fecha_str:
            return jsonify({"mensaje": "El parámetro 'fecha' es obligatorio."}), 400

        try:
            fecha_consulta = datetime.strptime(fecha_str, "%d/%m/%Y").date()
        except ValueError:
            return jsonify({"mensaje": "El formato de la fecha debe ser DD/MM/YYYY."}), 400

        habitaciones = Habitacion.query.all()

        habitaciones_respuesta = []
        for habitacion in habitaciones:
            
            reserva = Reserva.query.filter(
                Reserva.id_habitacion == habitacion.id,
                Reserva.fecha_inicio_hospedaje <= fecha_consulta,
                Reserva.fecha_fin_hospedaje >= fecha_consulta
            ).first()

            estado = "ocupada" if reserva else "libre"

            habitaciones_respuesta.append({
                "numero": habitacion.numero_habitacion,
                "estado": estado
            })

        respuesta = {
            "cantidad": len(habitaciones_respuesta),
            "habitaciones": habitaciones_respuesta
        }


        response_schema = BuscarHabitacionesPorFechaResponseSchema()
        return jsonify(response_schema.dump(respuesta)), 200

    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 500


# ------------------------ENDPOINT HABITACIONES: Ruta filtrar por precio ----------  
@habitacion_bp.route('/habitaciones/filtrar', methods=['GET'])
@rutaProtegida(categoria_esperada='cliente')
def filtrar_habitaciones_por_precio():
    try:

        precio_str = request.args.get('precio')
        if not precio_str:
            return jsonify({"mensaje": "El parámetro 'precio' es obligatorio."}), 400


        try:
            precio = float(precio_str)
        except ValueError:
            return jsonify({"mensaje": "El precio debe ser un número decimal."}), 400


        habitaciones = Habitacion.query.filter(Habitacion.precio <= precio).all()


        habitaciones_respuesta = [
            {
                "id": habitacion.id,
                "numero": habitacion.numero_habitacion,
                "precio": str(habitacion.precio)
            }
            for habitacion in habitaciones
        ]

        return jsonify(habitaciones_respuesta), 200

    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 500
    

# ------------------------ENDPOINT HABITACIONES: Ruta filtrar por fechas  ----------  
@habitacion_bp.route('/habitaciones/disponibles', methods=['GET'])
@rutaProtegida(categoria_esperada='cliente')
def habitaciones_disponibles():
    try:
        inicio_str = request.args.get('inicio')
        fin_str = request.args.get('fin')

        if not inicio_str or not fin_str:
            return jsonify({"mensaje": "Los parámetros 'inicio' y 'fin' son obligatorios."}), 400

        try:
            inicio = datetime.strptime(inicio_str, "%d/%m/%Y")
            fin = datetime.strptime(fin_str, "%d/%m/%Y")
        except ValueError:
            return jsonify({"mensaje": "El formato de fecha debe ser dd/mm/yyyy."}), 400

        habitaciones_disponibles = db.session.query(Habitacion).filter(
            ~Habitacion.id.in_(
                db.session.query(Reserva.id_habitacion).filter(
                    (Reserva.fecha_inicio_hospedaje <= fin) & 
                    (Reserva.fecha_fin_hospedaje >= inicio)
                )
            )
        ).all()

        habitaciones_respuesta = [
            {
                "id": habitacion.id,
                "numero": habitacion.numero_habitacion,
                "precio": str(habitacion.precio)
            }
            for habitacion in habitaciones_disponibles
        ]

        return jsonify(habitaciones_respuesta), 200

    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 500
