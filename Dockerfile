# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala git y otras dependencias necesarias
RUN apt-get update && apt-get install -y git

# Clona el repositorio de GitHub (modifica la URL del repositorio)
RUN git clone https://github.com/bussi-inceptia/intents.git

# Cambia al directorio del repositorio clonado
WORKDIR /app/intents

# Instala las dependencias del repositorio
#RUN pip install -r requirements.txt

# Copia el script a ejecutar en el contenedor
#COPY create_nlu.py /app/repo/

# Define el comando por defecto que se ejecutará cuando se inicie el contenedor
CMD ["python", "create_nlu.py"]
