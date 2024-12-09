para levantar sin docker en config.py fijate y cambia 

#este es para probar local con tus datos cambiar con lo de tu config de postgre
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1920@localhost:5432/hotel_base'