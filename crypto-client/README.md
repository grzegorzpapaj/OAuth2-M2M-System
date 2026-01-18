# Crypto Client

Klient OAuth2 wykorzystujący **Client Credentials Grant** do komunikacji z crypto-server.

## Funkcjonalności

- ✅ Rejestracja klienta w crypto-server
- ✅ Uzyskiwanie JWT tokenu przez OAuth2 Client Credentials
- ✅ Automatyczne odświeżanie tokenu
- ✅ Pobieranie kursów walut z zabezpieczonych endpointów
- ✅ Background task ciągle pobierający dane

## Instalacja

```bash
cd crypto-client
pip install -r requirements.txt
```

## Konfiguracja

Skopiuj `.env.example` do `.env` i dostosuj wartości:

```bash
cp .env.example .env
```

## Uruchomienie

```bash
# Z katalogu głównego projektu
uvicorn crypto-client.main:app --reload --port 8001

# Lub bezpośrednio
python -m uvicorn crypto_client.main:app --reload --port 8001
```

## Endpointy API

### Zarządzanie uwierzytelnianiem

- `POST /api/register` - Zarejestruj klienta w crypto-server
- `POST /api/login` - Zaloguj się i uzyskaj token
- `POST /api/configure` - Skonfiguruj credentials
- `GET /api/status` - Sprawdź status uwierzytelnienia

### Pobieranie danych

- `GET /api/currencies` - Pobierz wszystkie kursy walut (wymaga tokenu)
- `GET /api/currencies/{symbol}` - Pobierz kurs konkretnej waluty (wymaga tokenu)
- `GET /api/test-server` - Testuj połączenie z serwerem

### Inne

- `GET /` - Informacje o kliencie
- `GET /health` - Health check

## Przykładowe użycie

### 1. Zarejestruj klienta

```bash
curl -X POST http://localhost:8001/api/register
```

### 2. Zaloguj się (uzyskaj token)

```bash
curl -X POST http://localhost:8001/api/login
```

### 3. Pobierz kursy walut

```bash
curl http://localhost:8001/api/currencies
```

### 4. Pobierz konkretną walutę

```bash
curl http://localhost:8001/api/currencies/BTC
```

## OAuth2 Flow

1. Klient posiada `client_id` i `client_secret`
2. Klient wysyła te credentials do `POST /api/auth/token`
3. Crypto-server weryfikuje credentials i zwraca JWT token
4. Klient używa tego tokenu w nagłówku `Authorization: Bearer <token>`
5. Token automatycznie się odświeża gdy wygasa

## Struktura projektu

```
crypto-client/
├── __init__.py
├── main.py              # Główna aplikacja FastAPI
├── client_service.py    # Logika OAuth2 i komunikacji
├── routes.py            # Endpointy API
├── config.py            # Konfiguracja
├── requirements.txt     # Zależności
└── README.md           # Ten plik
```
