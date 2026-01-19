FROM python:3.11-slim

WORKDIR /app

COPY crypto-client/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY crypto-client ./crypto-client

# Uruchom klienta
CMD ["uvicorn", "crypto-client.main:app", "--host", "0.0.0.0", "--port", "8001"]
