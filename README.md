# Hotel_API

Iniciar la API en Docker desde Visual Studio Code

Requisitos previos
Antes de comenzar, asegúrate de tener Docker y Docker Compose instalados en tu sistema.
Instalar Docker
Instalar Docker Compose

Pasos para iniciar la API desde Visual Studio Code
Abre Visual Studio Code y abre tu proyecto (si no está abierto ya).

Abre la terminal integrada de Visual Studio Code. Para hacer esto:

Ve al menú superior y selecciona Terminal > Nuevo Terminal.

Esto abrirá una terminal dentro de Visual Studio Code.

Ejecuta el siguiente comando en la terminal de Visual Studio Code para construir y levantar los contenedores:

docker-compose up --build

Este comando descargará las imágenes necesarias y construirá los contenedores para los servicios definidos en el archivo docker-compose.yml.

Espera a que el proceso termine. Cuando todo haya cargado correctamente.

Accede a la API desde HotelesClient :

con la url:
http://localhost:8000

 
