FROM python:3.10.12

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

RUN apt-get update -y
RUN apt-get install gcc -y

# Copia los archivos de requisitos y los instala
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia el contenido de tu directorio local a /app en el contenedor
COPY . .

# Expone el puerto en el que correrá la aplicación
EXPOSE 8080

# Define el comando para correr la aplicación
#ENTRYPOINT ["uwsgi", "--ini", "uwsgi.ini"]

# Modifica el Dockerfile temporalmente:
ENTRYPOINT ["python", "app.py"]