# Usar una imagen base de Python
FROM python:3.13-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /hotel_API

# Copiar todos los archivos a la carpeta del contenedorpip-review --local --auto

COPY requirements.txt .

# Instalar las dependencias
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Comando para ejecutar la aplicación con Waitress
CMD ["waitress-serve", "--listen=0.0.0.0:8000", "app:app"]
