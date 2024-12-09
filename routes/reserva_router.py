from datetime import datetime
from flask import Blueprint, jsonify, request
import jwt
from schemas.reserva_habitacion_schema import HabitacionEstadoSchema
from schemas.reserva_schema import ReservaSchema
from models.models import Reserva
import validaciones
from router.usuario_router import rutaProtegida
from dbConfig import db
from config import app



reserva_bp = Blueprint('reserva_bp', __name__)

# ------------------------ENDPOINT RESERVAS: para reservar una nueva habitacion (se necesita dos fechas disponibles)
@reserva_bp.route('/reservas', methods=['POST'])
@rutaProtegida(categoria_esperada='cliente')
def crear_reserva():
    try:
        auth_header = request.headers.get('n-auth')
        if auth_header and auth_header.startswith("bearer "):
            token = auth_header.replace("bearer ", "")
        else:
            return jsonify({"mensaje": "Token no proporcionado o inválido."}), 401
        
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        id_usuario = payload['id']


        data = request.get_json()
        inicio = data.get("inicio")
        fin = data.get("fin")
        habitacion = data.get("habitacion")

        if not validaciones.validacionFechasHospedaje(inicio, fin):
            return jsonify({"mensaje": "Fechas no válidas. Asegúrese de que la fecha de inicio no sea posterior a la fecha de fin."}), 400

        fecha_inicio = datetime.strptime(inicio, "%d/%m/%Y")
        fecha_fin = datetime.strptime(fin, "%d/%m/%Y")


        if not validaciones.disponibilidadHabitacion(habitacion, fecha_inicio, fecha_fin):
            return jsonify({"mensaje": "La habitación no está disponible en las fechas seleccionadas."}), 400


        nueva_reserva = Reserva(id_usuario=id_usuario, id_habitacion=habitacion, fecha_inicio_hospedaje=fecha_inicio, fecha_fin_hospedaje=fecha_fin)
        db.session.add(nueva_reserva)
        db.session.commit()
        print('error?2')

        return jsonify({"mensaje": "Reserva realizada con éxito."}), 201

    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 500

    
# ------------------------ENDPOINT REGRITRO: RESERVAS: Ruta para obtener las reservas ----------    
@reserva_bp.route('/reservas', methods=['GET'])
@rutaProtegida(categoria_esperada='empleado')
def reservas():
    try:
        reservas_data = validaciones.obtener_reservas()

        if reservas_data is not None:
            schema = ReservaSchema(many=True)
            result = schema.dump(reservas_data)
            return jsonify(result), 200
        else:
            return jsonify({"mensaje": "Error al obtener reservas"}), 500

    except Exception as e:
        return jsonify({"mensaje": f"Error: {e}"}), 500