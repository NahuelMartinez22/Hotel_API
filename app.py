from config import app  
from router.usuario_router import usuario_bp
from router.habitacion_router import habitacion_bp
from router.reserva_router import reserva_bp

application = app

# Registrar Blueprints
app.register_blueprint(usuario_bp, url_prefix='/')
app.register_blueprint(habitacion_bp, url_prefix='/')
app.register_blueprint(reserva_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
