# 🐳 Docker Deployment Guide

## Przegląd

System używa Docker Compose do uruchomienia wszystkich komponentów:
- **PostgreSQL** (port 5432) - Baza danych dla crypto-server
- **Crypto-Server** (port 8000) - OAuth2 server + API kryptowalut
- **Crypto-Client** (port 8001) - Dashboard użytkownika z autentykacją

## 🚀 Quick Start

### 1. Uruchomienie Systemu

```bash
cd /home/pi/studia/OAuth2-M2M-System
docker-compose up -d
```

To uruchomi wszystkie kontenery w tle.

### 2. Sprawdzenie Statusu

```bash
docker-compose ps
```

Oczekiwany output:
```
NAME                IMAGE                      STATUS
crypto-server       oauth2-m2m-system-server   Up
crypto-client       oauth2-m2m-system-client   Up
oauth2-m2m-system-db-1   postgres:16-alpine    Up (healthy)
```

### 3. Utworzenie Pierwszego Użytkownika

```bash
./create-user-docker.sh
```

Przykład:
```
📝 Username: john
🔑 Password: secret123
📧 Email (optional): john@example.com
   Client ID (optional): test_client
   Client Secret (optional): test_secret_123
👑 Is admin? (y/n): n
```

### 4. Dostęp do Dashboardu

Otwórz przeglądarkę: **http://localhost:8001**

Zaloguj się używając utworzonego username i hasła.

## 📊 Struktura Kontenerów

```
┌─────────────────────────┐
│   PostgreSQL (db)       │
│   Port: 5432            │
│   Volume: postgres_data │
└──────────┬──────────────┘
           │
┌──────────▼──────────────┐
│   Crypto-Server         │
│   Port: 8000            │
│   Container: server     │
└──────────┬──────────────┘
           │
┌──────────▼──────────────┐
│   Crypto-Client         │
│   Port: 8001            │
│   Container: client     │
│   Volume: client_data   │
│   (SQLite users DB)     │
└─────────────────────────┘
```

## 🔧 Zarządzanie Kontenerami

### Uruchomienie
```bash
docker-compose up -d
```

### Zatrzymanie
```bash
docker-compose down
```

### Restart
```bash
docker-compose restart
```

### Restart pojedynczego serwisu
```bash
docker-compose restart client
docker-compose restart server
```

### Zobacz logi
```bash
# Wszystkie serwisy
docker-compose logs -f

# Tylko client
docker-compose logs -f client

# Tylko server
docker-compose logs -f server

# Ostatnie 100 linii
docker-compose logs --tail=100 client
```

### Rebuild po zmianach w kodzie
```bash
docker-compose up -d --build
```

## 🛠️ Debugowanie

### Wejdź do kontenera Client
```bash
docker-compose exec client bash
```

### Wejdź do kontenera Server
```bash
docker-compose exec server bash
```

### Sprawdź bazę danych PostgreSQL
```bash
docker-compose exec db psql -U crypto-server -d crypto-server-db
```

### Zobacz wszystkie zmienne środowiskowe
```bash
docker-compose exec client env
```

### Sprawdź bazę danych użytkowników (SQLite)
```bash
docker-compose exec client sqlite3 /app/data/crypto_client_users.db "SELECT * FROM users;"
```

## 📦 Wolumeny (Persystencja Danych)

### PostgreSQL Data
```bash
docker volume inspect oauth2-m2m-system_postgres_data
```

### Client User Database (SQLite)
```bash
docker volume inspect oauth2-m2m-system_client_data
```

### Lista wszystkich wolumenów
```bash
docker volume ls
```

### Usunięcie wolumenów (UWAGA: usuwa dane!)
```bash
docker-compose down -v
```

## 🔐 Zarządzanie Użytkownikami

### Tworzenie użytkownika (Interaktywnie)
```bash
./create-user-docker.sh
```

### Tworzenie użytkownika (Skrypt)
```bash
docker-compose exec client python3 -c "
from crypto_client.database import db
user = db.create_user(
    username='alice',
    password='pass123',
    email='alice@example.com',
    client_id='alice_client',
    client_secret='alice_secret_456'
)
print(f'Created user: {user[\"username\"]}')
"
```

### Lista użytkowników
```bash
docker-compose exec client sqlite3 /app/data/crypto_client_users.db \
  "SELECT id, username, email, is_admin, created_at FROM users;"
```

### Usunięcie użytkownika
```bash
docker-compose exec client sqlite3 /app/data/crypto_client_users.db \
  "DELETE FROM users WHERE username='john';"
```

## 🧪 Testowanie API

### Test Health Endpoint
```bash
curl http://localhost:8001/health
```

### Test Login
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123"}' \
  -c cookies.txt
```

### Test Currencies (po zalogowaniu)
```bash
curl http://localhost:8001/api/currencies -b cookies.txt
```

## 🔄 Aktualizacja Kodu

### Gdy zmienisz kod Pythona
```bash
# Przebuduj i zrestartuj
docker-compose up -d --build

# Lub tylko restart (szybsze jeśli kod jest zmontowany jako volume)
docker-compose restart client
```

### Gdy zmienisz requirements.txt
```bash
# Musi być rebuild
docker-compose build client
docker-compose up -d client
```

### Gdy zmienisz static files (HTML/CSS/JS)
```bash
# Wystarczy restart (pliki są zmontowane jako volume)
docker-compose restart client
```

## 🚨 Troubleshooting

### Problem: Kontenery nie startują
```bash
# Zobacz logi
docker-compose logs

# Sprawdź status
docker-compose ps
```

### Problem: Port już zajęty (8000 lub 8001)
```bash
# Znajdź proces na porcie
sudo lsof -i :8001

# Zabij proces
sudo kill -9 <PID>

# Lub zmień port w docker-compose.yml
```

### Problem: Database connection error
```bash
# Sprawdź czy PostgreSQL działa
docker-compose ps db

# Sprawdź logi PostgreSQL
docker-compose logs db

# Restart bazy
docker-compose restart db
```

### Problem: "Database locked" (SQLite)
```bash
# Zrestartuj client
docker-compose restart client

# Lub usuń lock file
docker-compose exec client rm -f /app/data/crypto_client_users.db-journal
```

### Problem: Brak użytkowników po restarcie
```bash
# Sprawdź czy wolumen istnieje
docker volume inspect oauth2-m2m-system_client_data

# Lista użytkowników
docker-compose exec client sqlite3 /app/data/crypto_client_users.db \
  "SELECT * FROM users;"
```

### Czysty restart (usuwa wszystkie dane!)
```bash
docker-compose down -v
docker-compose up -d
./create-user-docker.sh
```

## 🎯 Production Deployment

### Zmienne środowiskowe dla produkcji

Utwórz plik `.env`:
```env
# Database
POSTGRES_PASSWORD=strong-password-here
POSTGRES_DB=crypto-server-db

# Server
ADMIN_SECRET=super-secret-admin-key-change-this
CRYPTO_SERVER_URL=https://api.yourdomain.com

# Security
SESSION_SECRET=another-random-secret
```

### Docker Compose dla produkcji
```yaml
version: "3.8"

services:
  # ... same as development ...
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - client
      - server
```

### Nginx jako reverse proxy
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://client:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://server:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📚 Przydatne Komendy

```bash
# Start wszystkiego
docker-compose up -d

# Stop wszystkiego
docker-compose down

# Zobacz co działa
docker-compose ps

# Logi w czasie rzeczywistym
docker-compose logs -f

# Rebuild + restart
docker-compose up -d --build

# Wejdź do kontenera
docker-compose exec client bash

# Utwórz użytkownika
./create-user-docker.sh

# Test API
curl http://localhost:8001/health

# Usuń wszystko (włącznie z danymi!)
docker-compose down -v
```

## 🔗 Linki

- **Dashboard**: http://localhost:8001
- **Server API Docs**: http://localhost:8000/docs
- **Client API Docs**: http://localhost:8001/docs
- **PostgreSQL**: localhost:5432

## 💡 Tips

1. **Development**: Użyj `docker-compose logs -f` aby widzieć logi na żywo
2. **Hot Reload**: Kod jest zmontowany jako volume, więc zmiany są widoczne po restarcie
3. **Backup**: Regularnie backupuj wolumeny Docker
4. **Security**: W produkcji zmień wszystkie hasła i sekrety!
5. **Monitoring**: Dodaj health checks do wszystkich serwisów
