FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api/
COPY database/ ./database/

EXPOSE 5002

# Comando para ejecutar la API
CMD ["python", "api/autor.py"]