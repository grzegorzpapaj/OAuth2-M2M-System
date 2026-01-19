FROM python:3.11-slim

WORKDIR /app

# Zainstaluj zależności systemowe (jeśli potrzebne dla asyncpg/psycopg2)
# RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY crypto-server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY crypto-server ./crypto-server

# Uruchom serwer
CMD ["uvicorn", "crypto-server.main:app", "--host", "0.0.0.0", "--port", "8000"]
