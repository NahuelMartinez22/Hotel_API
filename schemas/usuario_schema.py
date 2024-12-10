from marshmallow import Schema, fields, ValidationError, post_load
from werkzeug.security import check_password_hash
from models.models import Usuario
from dbConfig import db
from config import ma

"""class LoginSchema(Schema):
    usuario = fields.String(required=True)
    clave = fields.String(required=True)"""

class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_fk = True

    # Método para cargar y validar el usuario y la contraseña
    @post_load #decorador que incializa 
    def validar_usuario(self, data, **kwargs):
        usuario = data.get('usuario')
        clave = data.get('clave')

        try:
            # Buscar el usuario en la base de datos
            usuario_encontrado = db.session.query(Usuario).filter_by(usuario=usuario).first()

            # Verificar si el usuario existe y la contraseña es correcta
            if not usuario_encontrado or not check_password_hash(usuario_encontrado.clave, clave):
                raise ValidationError("Credenciales invalidas.")

        except Exception as e:
            print(f"Error al validar usuario: {e}")
            raise ValidationError("Error en la validacion del usuario.")

        return data  # devuelve los datos si todo salio bien 
