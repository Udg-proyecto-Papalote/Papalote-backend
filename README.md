# Backend del proyecto modular

## Pasos para el uso del backend

1. Clonar el repositorio
2. Instalar virtualenv con el comando `pip install virtualenv`
3. Crear un entorno virtual con el comando `virtualenv venv`
4. Activar el entorno virtual con el comando `./venv/Scripts/activate.bat`
5. Instalar las dependencias con el comando `pip install -r requirements.txt`
6. Ve al archivo `config.py` y reemplaza los valores de las variables `MONGODB_USERNAME` y `MONGODB_PASSWORD` por los valores de tus credenciales de MongoDB
7. Ejecuta el archivo `app.py` con el comando `python ./src/app.py`

## Base de datos en VSCode

1. Instalar la extensión `MongoDB for VSCode`
2. Conectar la base de datos con el botón `Connect with Connection String`
3. Introducir la cadena de conexión de MongoDB Atlas
4. Te vas a la tab de la extensión y verás la conexión con tu base de datos
