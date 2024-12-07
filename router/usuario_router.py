from functools import wraps
from flask import Blueprint, jsonify, request
import jwt
from marshmallow import ValidationError
from models import Usuario  # Import your models
from schemas.login_schema import LoginSchema
from schemas.registro_schema import RegistroSchema
import validaciones
from dbConfig import db
from config import app


usuario_bp = Blueprint('usuario_bp', __name__)

# ------------------------ENDPOINT LOGIN 
@usuario_bp.route('/login', methods=['POST'])
def login():
    try:
        schema = LoginSchema()
        data = request.get_json()
        
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return jsonify({"message": "Invalid input", "errors": err.messages}), 400

        usuario = validated_data['usuario']
        clave = validated_data['clave']

        usuario_data = validaciones.validarUsuario(usuario, clave)

        if usuario_data:
            payload = {"usuario": usuario, "id": usuario_data.id, "categoria": usuario_data.categoria}
            
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({'token': token, 'categoria': usuario_data.categoria}), 200
        else:
            return jsonify({'status': 401, "message": 'Credenciales inválidas.'}), 401
    except Exception as e:
        return jsonify({'status': 500, "message": str(e)}), 500
    
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
            return jsonify({"message": "Invalid input", "errors": err.messages}), 400

        usuario = validated_data['usuario']
        categoria = validated_data['categoria']
        clave1 = validated_data['clave1']
        clave2 = validated_data['clave2']

        if clave1 != clave2:
            return jsonify({"mensaje": "Las claves no coinciden"}), 400
        
        existing_user = Usuario.query.filter_by(usuario=usuario).first()
        if existing_user:
            return jsonify({"mensaje": "El usuario ya existe"}), 400


        nuevo_usuario = Usuario(usuario=usuario, categoria=categoria, clave=clave1)

        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 500