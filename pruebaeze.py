from dbConfig import db
from models.models import Usuario

# Prueba de conexión
try:
    usuarios = Usuario.query.all()
    print(f"Usuarios encontrados: {[usuario.usuario for usuario in usuarios]}")
except Exception as e:
    print(f"Error al conectar con la base de datos: {e}")
