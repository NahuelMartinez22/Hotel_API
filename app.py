from config import app  
from routes.usuario_routes import usuario_bp
from routes.habitacion_routes import habitacion_bp
from routes.reserva_routes import reserva_bp

application = app

# Registrar Blueprints
app.register_blueprint(usuario_bp, url_prefix='/')
app.register_blueprint(habitacion_bp, url_prefix='/')
app.register_blueprint(reserva_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
