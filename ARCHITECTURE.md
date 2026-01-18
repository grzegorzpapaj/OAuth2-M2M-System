# Architektura OAuth2 M2M System

## Diagram architektury systemu

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         OAuth2 M2M System                                 │
└──────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐      ┌─────────────────────────────────┐
│       CRYPTO-CLIENT             │      │       CRYPTO-SERVER             │
│       (Port: 8001)              │      │       (Port: 8000)              │
├─────────────────────────────────┤      ├─────────────────────────────────┤
│                                 │      │                                 │
│  ┌─────────────────────────┐   │      │  ┌─────────────────────────┐   │
│  │   FastAPI Application   │   │      │  │   FastAPI Application   │   │
│  │   - Routes              │   │      │  │   - Auth Router         │   │
│  │   - Background Tasks    │   │      │  │   - Currency Router     │   │
│  └──────────┬──────────────┘   │      │  └──────────┬──────────────┘   │
│             │                   │      │             │                   │
│  ┌──────────▼──────────────┐   │      │  ┌──────────▼──────────────┐   │
│  │   ClientService         │   │      │  │   Auth Module           │   │
│  │   - OAuth2 Logic        │◄──┼──────┼──┤   - JWT Generation      │   │
│  │   - Token Management    │   │      │  │   - Client Validation   │   │
│  │   - Auto Refresh        │   │      │  └─────────────────────────┘   │
│  └─────────────────────────┘   │      │                                 │
│                                 │      │  ┌─────────────────────────┐   │
│  ┌─────────────────────────┐   │      │  │   Currency Module       │   │
│  │   HTTP Client (httpx)   │   │      │  │   - Get All Rates       │   │
│  │   - Async Requests      │   │      │  │   - Get Single Rate     │   │
│  │   - Bearer Auth         │   │      │  │   - Protected Endpoints │   │
│  └─────────────────────────┘   │      │  └──────────┬──────────────┘   │
│                                 │      │             │                   │
└─────────────────────────────────┘      │  ┌──────────▼──────────────┐   │
                                         │  │   Database Module       │   │
                                         │  │   - SQLAlchemy          │   │
                                         │  │   - AsyncSession        │   │
                                         │  └──────────┬──────────────┘   │
                                         │             │                   │
                                         └─────────────┼───────────────────┘
                                                       │
                                         ┌─────────────▼───────────────┐
                                         │     PostgreSQL Database      │
                                         │     (Port: 5432)             │
                                         │  ┌─────────────────────────┐│
                                         │  │  Tables:                ││
                                         │  │  - clients              ││
                                         │  │  - currency_rates       ││
                                         │  └─────────────────────────┘│
                                         └─────────────────────────────┘
```

## OAuth2 Client Credentials Flow

```
┌─────────┐                                              ┌─────────┐
│ Client  │                                              │ Server  │
└────┬────┘                                              └────┬────┘
     │                                                        │
     │  1. POST /api/auth/register                           │
     │     {client_id, client_secret, app_name}              │
     │ ─────────────────────────────────────────────────────>│
     │                                                        │
     │  2. {message: "Klient zarejestrowany", id: ...}       │
     │ <─────────────────────────────────────────────────────│
     │                                                        │
     │  3. POST /api/auth/token                              │
     │     {client_id, client_secret}                        │
     │ ─────────────────────────────────────────────────────>│
     │                                                        │
     │                                          ┌──────────┐ │
     │                                          │ Validate │ │
     │                                          │ Client   │ │
     │                                          └────┬─────┘ │
     │                                               │       │
     │                                          ┌────▼─────┐ │
     │                                          │ Generate │ │
     │                                          │   JWT    │ │
     │                                          └────┬─────┘ │
     │                                               │       │
     │  4. {access_token: "eyJhbG...", type: ...}    │       │
     │ <─────────────────────────────────────────────────────│
     │                                                        │
     │  5. GET /api/currency/                                │
     │     Authorization: Bearer eyJhbG...                   │
     │ ─────────────────────────────────────────────────────>│
     │                                                        │
     │                                          ┌──────────┐ │
     │                                          │ Verify   │ │
     │                                          │   JWT    │ │
     │                                          └────┬─────┘ │
     │                                               │       │
     │                                          ┌────▼─────┐ │
     │                                          │ Get Data │ │
     │                                          │ from DB  │ │
     │                                          └────┬─────┘ │
     │                                               │       │
     │  6. [{symbol: "BTC", rate: ...}, ...]         │       │
     │ <─────────────────────────────────────────────────────│
     │                                                        │
```

## Komponenty systemu

### 1. Crypto-Server

**Odpowiedzialności:**
- Uwierzytelnianie klientów OAuth2
- Generowanie i walidacja JWT tokenów
- Dostarczanie API z kursami kryptowalut
- Ochrona endpointów przed nieautoryzowanym dostępem
- Aktualizacja kursów w tle (co 3 sekundy)

**Główne moduły:**
- `auth.py` - OAuth2 i JWT
- `currency.py` - Chronione endpointy
- `database.py` - Połączenie z PostgreSQL
- `models.py` - Modele danych
- `tasks.py` - Background jobs

### 2. Crypto-Client

**Odpowiedzialności:**
- Rejestracja w crypto-server
- Automatyczne uzyskiwanie tokenów
- Automatyczne odświeżanie wygasłych tokenów
- Komunikacja z chronionymi endpointami
- Dostarczanie własnego API dla użytkowników

**Główne moduły:**
- `client_service.py` - Logika OAuth2
- `routes.py` - Publiczne API
- `main.py` - Aplikacja FastAPI
- `config.py` - Konfiguracja

### 3. PostgreSQL Database

**Tabele:**

**clients:**
- id (PK)
- client_id (unique)
- client_secret
- app_name
- is_active
- created_at

**currency_rates:**
- id (PK)
- symbol (unique)
- rate
- last_updated

## Przepływ danych

### Rejestracja klienta
```
User -> Client API -> Client Service -> Server API -> Database
```

### Uzyskiwanie tokenu
```
User -> Client API -> Client Service -> Server Auth -> JWT Generation -> Token
```

### Pobieranie danych
```
User -> Client API -> Client Service (+ Token) -> Server Currency API -> Database -> Response
```

### Automatyczne odświeżanie
```
Client Service (check token) -> Expired? -> Get new token -> Retry request
```

## Bezpieczeństwo

1. **Credentials Storage:**
   - Client ID i Secret przechowywane w zmiennych środowiskowych
   - Hasła w bazie (w produkcji powinny być hashowane!)

2. **Token Security:**
   - JWT z czasem wygaśnięcia (120 minut)
   - Bearer token w nagłówku Authorization
   - Walidacja podpisu JWT przy każdym zapytaniu

3. **API Protection:**
   - Wszystkie endpointy currency wymagają tokenu
   - Middleware FastAPI sprawdza autoryzację
   - HTTPException dla nieautoryzowanych żądań

## Background Tasks

### Server (crypto-server/tasks.py)
- **currency_generator():**
  - Uruchamia się przy starcie serwera
  - Co 3 sekundy aktualizuje kursy walut
  - Symuluje zmienność rynku (+/- 0.5%)

### Client (crypto-client/main.py)
- **background_currency_fetcher():**
  - Uruchamia się przy starcie klienta
  - Co 10 sekund pobiera kursy z serwera
  - Automatycznie loguje się jeśli token wygasł
  - Wyświetla kursy w konsoli

## Skalowanie

### Możliwości rozbudowy:

1. **Multi-client support:**
   - Dodanie bazy danych po stronie klienta
   - Zarządzanie wieloma parami credentials
   - Load balancing

2. **Security improvements:**
   - Hashowanie client_secret (bcrypt)
   - HTTPS/TLS
   - Rate limiting
   - Token refresh mechanism

3. **Feature additions:**
   - WebSocket dla real-time updates
   - Cache (Redis)
   - Monitoring (Prometheus)
   - Logging (ELK stack)

4. **Deployment:**
   - Konteneryzacja (Docker)
   - Kubernetes orchestration
   - CI/CD pipeline
