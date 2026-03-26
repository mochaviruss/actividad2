# Imagen base oficial de Python
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias primero (aprovecha cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la app
COPY app/ .

# Comando para iniciar el bot
CMD ["python", "main.py"]
