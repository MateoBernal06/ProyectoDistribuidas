
FROM python:3.9-slim

WORKDIR /app

# Dependencias del sistema
RUN pip install --no-cache-dir Flask==2.3.3 Werkzeug==2.3.7

COPY . .

# Crear directorio para la base de datos
RUN mkdir -p /app/data

# Exponer el puerto
EXPOSE 5000

# Variables de entorno
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
