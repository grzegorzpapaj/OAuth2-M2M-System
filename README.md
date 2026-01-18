# OAuth2 M2M System

System komunikacji Machine-to-Machine (M2M) wykorzystujący **OAuth2 Client Credentials Grant** zbudowany w FastAPI.

## 📋 Opis projektu

Projekt składa się z dwóch komponentów:

### 🔐 **Crypto-Server**
Serwer API dostarczający:
- OAuth2 uwierzytelnianie (Client Credentials Grant)
- JWT tokeny
- Chronione endpointy z kursami kryptowalut
- Background task aktualizujący kursy co 3 sekundy

### 💻 **Crypto-Client**
Klient implementujący:
- Automatyczną rejestrację w serwerze
- Uzyskiwanie i odświeżanie JWT tokenów
- Komunikację z chronionymi endpointami
- Background task pobierający dane co 10 sekund

## 🚀 Szybki start

### Wymagania
- Python 3.10+
- Docker & Docker Compose
- pip

### 1. Klonowanie i instalacja

```bash
# Przejdź do katalogu projektu
cd OAuth2-M2M-System

# Zainstaluj zależności serwera
pip3 install -r crypto-server/requirements.txt

# Zainstaluj zależności klienta
pip3 install -r crypto-client/requirements.txt
```

### 2. Uruchomienie bazy danych

```bash
docker-compose up -d
```

### 3. Uruchomienie Crypto-Server

```bash
# Opcja 1: Przez skrypt
./run-server.sh

# Opcja 2: Ręcznie
cd crypto-server
uvicorn main:app --reload --port 8000
```

Serwer dostępny na: **http://localhost:8000**  
Dokumentacja API: **http://localhost:8000/docs**

### 4. Uruchomienie Crypto-Client

```bash
# Opcja 1: Przez skrypt
./run-client.sh

# Opcja 2: Ręcznie
cd crypto-client
uvicorn main:app --reload --port 8001
```

Klient dostępny na: **http://localhost:8001**  
Dokumentacja API: **http://localhost:8001/docs**

### 5. Testowanie

```bash
python3 crypto-client/test_client.py
```

## 📁 Struktura projektu

```
OAuth2-M2M-System/
├── docker-compose.yml          # Konfiguracja PostgreSQL
├── run-server.sh              # Skrypt uruchamiający serwer
├── run-client.sh              # Skrypt uruchamiający klienta
├── EXAMPLES.md                # Przykłady użycia
│
├── crypto-server/             # Serwer OAuth2
│   ├── __init__.py
│   ├── main.py               # Główna aplikacja FastAPI
│   ├── auth.py               # Logika OAuth2 i JWT
│   ├── currency.py           # Endpointy kursów walut
│   ├── database.py           # Konfiguracja bazy danych
│   ├── models.py             # Modele SQLAlchemy
│   └── tasks.py              # Background tasks
│
└── crypto-client/            # Klient OAuth2
    ├── __init__.py
    ├── main.py              # Główna aplikacja FastAPI
    ├── client_service.py    # Logika OAuth2 i komunikacji
    ├── routes.py            # Endpointy API klienta
    ├── config.py            # Konfiguracja
    ├── test_client.py       # Skrypt testowy
    ├── requirements.txt     # Zależności
    └── README.md           # Dokumentacja klienta
```

## 🔑 OAuth2 Flow

```
┌─────────────┐                           ┌─────────────┐
│             │  1. POST /auth/register   │             │
│             │ ────────────────────────> │             │
│             │  {client_id, secret}      │             │
│             │                           │             │
│             │  2. POST /auth/token      │             │
│   Client    │ ────────────────────────> │   Server    │
│             │  {client_id, secret}      │             │
│             │ <──────────────────────── │             │
│             │  {access_token, ...}      │             │
│             │                           │             │
│             │  3. GET /currency/        │             │
│             │ ────────────────────────> │             │
│             │  Authorization: Bearer    │             │
│             │ <──────────────────────── │             │
│             │  [{rates}]                │             │
└─────────────┘                           └─────────────┘
```

## 📚 API Endpoints

### Crypto-Server

#### Uwierzytelnianie
- `POST /api/auth/register` - Rejestracja klienta
- `POST /api/auth/token` - Uzyskanie JWT tokenu

#### Kursy walut (wymagają tokenu)
- `GET /api/currency/` - Wszystkie kursy
- `GET /api/currency/{symbol}` - Konkretna waluta

### Crypto-Client

#### Zarządzanie
- `POST /api/register` - Zarejestruj w serwerze
- `POST /api/login` - Zaloguj i uzyskaj token
- `POST /api/configure` - Skonfiguruj credentials
- `GET /api/status` - Status uwierzytelnienia

#### Dane
- `GET /api/currencies` - Wszystkie kursy
- `GET /api/currencies/{symbol}` - Konkretna waluta
- `GET /api/test-server` - Test połączenia

## 💡 Przykłady użycia

### cURL - Pełny flow

```bash
# 1. Zarejestruj klienta
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"client_id": "test", "client_secret": "secret", "app_name": "Test"}'

# 2. Uzyskaj token
TOKEN=$(curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"client_id": "test", "client_secret": "secret"}' \
  | jq -r '.access_token')

# 3. Pobierz kursy
curl http://localhost:8000/api/currency/ \
  -H "Authorization: Bearer $TOKEN"
```

### Python

```python
from crypto_client.client_service import ClientService
import asyncio

async def main():
    client = ClientService()
    await client.register_client()
    await client.get_access_token()
    
    rates = await client.get_all_currency_rates()
    for rate in rates:
        print(f"{rate['symbol']}: ${rate['rate']}")
    
    await client.close()

asyncio.run(main())
```

Więcej przykładów w [EXAMPLES.md](EXAMPLES.md)

## 🛠️ Konfiguracja

### Crypto-Server
```python
# crypto-server/database.py
DATABASE_URL = "postgresql+asyncpg://crypto-server:postgres@localhost:5432/crypto-server-db"

# crypto-server/auth.py
SECRET_KEY = "secret-key-to-sign-tokens"
ACCESS_TOKEN_EXPIRE_MINUTES = 120
```

### Crypto-Client
```python
# crypto-client/.env
SERVER_URL=http://localhost:8000
CLIENT_ID=crypto-client-001
CLIENT_SECRET=super-secret-key-123
CLIENT_PORT=8001
```

## 🔧 Technologie

- **FastAPI** - Framework webowy
- **SQLAlchemy** - ORM
- **PostgreSQL** - Baza danych
- **python-jose** - JWT tokeny
- **httpx** - Klient HTTP
- **Pydantic** - Walidacja danych
- **Docker** - Konteneryzacja bazy danych

## 📖 Dokumentacja

- Crypto-Server: http://localhost:8000/docs
- Crypto-Client: http://localhost:8001/docs
- [Przykłady użycia](EXAMPLES.md)
- [Dokumentacja klienta](crypto-client/README.md)

## 🐛 Troubleshooting

### Baza danych nie działa
```bash
docker-compose down
docker-compose up -d
docker-compose ps
```

### Błąd 401 Unauthorized
- Sprawdź credentials (client_id, client_secret)
- Token wygasa po 120 minutach
- Użyj `/api/login` aby uzyskać nowy token

### Port zajęty
```bash
# Zmień port
uvicorn main:app --port 8002
```

## 📝 Licencja

Projekt edukacyjny - Bezpieczeństwo Usług Sieciowych

## 👤 Autor

Projekt OAuth2 M2M System

---

**⚡ Szybkie linki:**
- 📖 [Pełne przykłady](EXAMPLES.md)
- 🔧 [Konfiguracja klienta](crypto-client/README.md)
- 📚 [Swagger UI Server](http://localhost:8000/docs)
- 📚 [Swagger UI Client](http://localhost:8001/docs)
