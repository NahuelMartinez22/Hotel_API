from functools import wraps
from flask import Blueprint, jsonify, request
import jwt
from marshmallow import ValidationError
from models.models import Usuario 
from schemas.usuario_schema import LoginSchema , RegistroSchema

from dbConfig import db
from config import app
from schemas.usuario_schema import LoginSchema


usuario_bp = Blueprint('usuario_bp', __name__)



#el login ya agrege validacion marshmallow como pidio el prof
# ------------------------ENDPOINT LOGIN 
@usuario_bp.route('/login', methods=['POST'])
def login():
    try:
        # esto es la  instancia del esquema para validacines
        schema = LoginSchema()
        data = request.get_json()

        # esto valida datos con el schema que hice de usuario_schema
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return jsonify({"mensaje": "Entrada no valida", "errores": err.messages}), 400

        # Si la validacion pasa, recuperamos el usuario y generamos el token
        usuario_data = Usuario.query.filter_by(usuario=validated_data['usuario']).first()
        payload = {
            "usuario": usuario_data.usuario,
            "id": usuario_data.id,
            "categoria": usuario_data.categoria
        }

        # Genera el token JWT
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token, 'categoria': usuario_data.categoria}), 200

    except Exception as e:
        print(f"Excepción en /login: {e}")
        return jsonify({'estado': 500, "mensaje": str(e)}), 500


    
# Función para verificar las rutas con el token y rol
def rutaProtegida(categoria_esperada):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = request.headers.get('n-auth')

                if token:

                    token = token.replace("bearer ", "")


                    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                    categoria = payload.get('categoria')


                    if categoria == categoria_esperada:
                        return f(*args, **kwargs)
                    else:
                        return jsonify({"status": 403, 'message': 'No tiene permiso de acceso a la información'}), 403
                else:
                    return jsonify({"status": 401, 'message': 'Debe estar autenticado previamente'}), 401
            except jwt.ExpiredSignatureError:
                return jsonify({"status": 401, 'message': 'Token expirado'}), 401
            except jwt.InvalidTokenError:
                return jsonify({"status": 401, 'message': 'Token inválido'}), 401
            except Exception as e:
                print(f"Error en la validación del token: {e}")
                return jsonify({"status": 500, 'message': 'Error interno del servidor'}), 500
        return wrapper
    return decorator



# ------------------------ENDPOINT REGRITRO: para registrar un nuevo usuario
@usuario_bp.route('/registro', methods=['POST'])
def registro():
    try:
        
        schema = RegistroSchema()
        data = request.get_json()

        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return jsonify({"mensaje": "Datos de entrada invalidos. Por favor, corrige los errores y vuelve a intentarlo", "errors": err.messages}), 400

        # trae los datos validados
        usuario = validated_data['usuario']
        categoria = validated_data['categoria']
        clave1 = validated_data['clave1']

        # Crear y guardar el nuevo usuario
        nuevo_usuario = Usuario(usuario=usuario, categoria=categoria, clave=clave1)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

    except Exception as e:
        db.session.rollback()  
        return jsonify({"mensaje": f"error interno: {str(e)}"}), 500
