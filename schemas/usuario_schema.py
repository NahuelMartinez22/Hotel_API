from marshmallow import Schema, fields, ValidationError, post_load , validates,validates_schema
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

class RegistroSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuario
        include_fk = True
        
    usuario = fields.String(required=True)
    categoria = fields.String(required=True)
    clave1 = fields.String(required=True)
    clave2 = fields.String(required=True)

    @validates('usuario')
    def validar_usuario(self, value):
        if len(value) < 3:
            raise ValidationError("El nombre de usuario debe tener al menos 3 caracteres.")
        if not value.isalnum():
            raise ValidationError("El nombre de usuario solo puede contener caracteres alfanumericos.")
        
        # Validar que el usuario no exista
        existing_user = Usuario.query.filter_by(usuario=value).first()
        if existing_user:
            raise ValidationError("El usuario ya existe.")
        
    @validates('clave1')
    def validar_clave1(self, value):
        if len(value) < 4:
            raise ValidationError("La clave debe tener al menos 4 caracteres.")
        
    @validates_schema
    def validar_claves_coinciden(self, data, **kwargs):
        if data['clave1'] != data['clave2']:
            raise ValidationError("Las claves no coinciden.", field_name='clave2')