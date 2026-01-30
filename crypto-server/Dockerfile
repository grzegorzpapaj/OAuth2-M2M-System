FROM python:3.11-slim

WORKDIR /app


COPY crypto-server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY crypto-server ./crypto-server

CMD ["uvicorn", "crypto-server.main:app", "--host", "0.0.0.0", "--port", "8000"]
