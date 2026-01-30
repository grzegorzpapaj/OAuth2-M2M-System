# 🔐 User Authentication System - Guide

## Przegląd Systemu

System teraz posiada **dwupoziomową autentykację**:

1. **User Authentication** (Username + Password) - użytkownik ↔ crypto-client dashboard
2. **M2M OAuth2** (Client Credentials) - crypto-client ↔ crypto-server

## Architektura

```
┌─────────────┐
│   Browser   │
│  (Frontend) │
└──────┬──────┘
       │ POST /api/auth/login (username, password)
       │ → Session Cookie
       ↓
┌─────────────────────────┐
│   Crypto-Client (8001)  │
│   ┌──────────────────┐  │
│   │ User Database    │  │
│   │ (SQLite)         │  │
│   │ - users          │  │
│   │ - sessions       │  │
│   └──────────────────┘  │
└──────────┬──────────────┘
           │ GET /api/currencies
           │ → Uses user's client_id/secret
           │ → M2M OAuth2
           ↓
┌─────────────────────────┐
│   Crypto-Server (8000)  │
│   - OAuth2 Token        │
│   - Currency Data       │
└─────────────────────────┘
```

## 🚀 Quick Start

### 1. Instalacja Zależności

```bash
cd /home/pi/studia/OAuth2-M2M-System/crypto-client
pip install -r requirements.txt
```

### 2. Uruchomienie Serwerów

```bash
# Terminal 1 - Crypto Server
cd /home/pi/studia/OAuth2-M2M-System
./run-server.sh

# Terminal 2 - Crypto Client
./run-client.sh
```

### 3. Utworzenie Pierwszego Użytkownika

```bash
cd /home/pi/studia/OAuth2-M2M-System
python3 create_user.py
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

### 4. Logowanie w Przeglądarce

1. Otwórz: http://localhost:8001
2. Zaloguj się używając username i hasła
3. Dashboard załaduje się automatycznie z kursami kryptowalut

## 📊 Baza Danych

### Tabela `users`

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT,
    is_active BOOLEAN DEFAULT 1,
    is_admin BOOLEAN DEFAULT 0,
    client_id TEXT,
    client_secret TEXT,
    created_at TIMESTAMP,
    last_login TIMESTAMP
);
```

### Tabela `sessions`

```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    session_token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## 🔒 Endpointy API

### User Authentication

#### `POST /api/auth/login`
Logowanie użytkownika

**Request:**
```json
{
  "username": "john",
  "password": "secret123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "is_admin": false
  },
  "session_token": "ABC123...",
  "client_credentials": {
    "client_id": "test_client",
    "client_secret": "test_secret_123"
  }
}
```

**Uwaga:** Session token jest również ustawiony jako HTTP-only cookie.

#### `POST /api/auth/logout`
Wylogowanie użytkownika

**Response:**
```json
{
  "status": "success",
  "message": "Logged out successfully"
}
```

#### `GET /api/auth/me`
Pobierz dane zalogowanego użytkownika

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "is_admin": false
  },
  "client_credentials": {
    "client_id": "test_client",
    "client_secret": "test_secret_123"
  }
}
```

#### `POST /api/auth/register-user`
Rejestracja nowego użytkownika (admin)

**Request:**
```json
{
  "username": "jane",
  "password": "pass456",
  "email": "jane@example.com",
  "client_id": "jane_client",
  "client_secret": "jane_secret_456"
}
```

### Protected Endpoints (Require User Login)

#### `GET /api/currencies`
Pobierz wszystkie kursy kryptowalut

**Headers:**
- Cookie: `session_token=ABC123...`

**Response:**
```json
[
  {
    "symbol": "BTC",
    "rate": 45000.50,
    "name": "Bitcoin",
    "change_24h": 2.5,
    "updated_at": "2024-01-20T10:30:00"
  }
]
```

#### `GET /api/currencies/{symbol}`
Pobierz kurs konkretnej waluty

## 🛡️ Bezpieczeństwo

### Session Management
- **Token**: Bezpieczny 32-bajtowy token (URL-safe)
- **Expiration**: 24 godziny
- **Storage**: HTTP-only cookie (nie dostępny przez JavaScript)
- **Cleanup**: Automatyczne usuwanie wygasłych sesji przy starcie

### Password Hashing
- **Algorithm**: bcrypt
- **Library**: passlib
- **Rounds**: Default (12)

### Best Practices
1. **HTTPS**: W produkcji używaj HTTPS dla wszystkich połączeń
2. **Secure Cookies**: W produkcji ustaw `secure=True, samesite="strict"`
3. **Password Policy**: Wymuszaj silne hasła
4. **Rate Limiting**: Dodaj rate limiting dla endpointów logowania
5. **Session Timeout**: Rozważ krótsze sesje dla wrażliwych operacji

## 📝 Workflow Użytkownika

### Scenariusz 1: Nowy Użytkownik

1. **Administrator** tworzy użytkownika przez CLI:
   ```bash
   python3 create_user.py
   ```

2. **Administrator** przekazuje credentials użytkownikowi bezpiecznym kanałem

3. **Użytkownik** loguje się w przeglądarce:
   - Username: `john`
   - Password: `secret123`

4. **System** weryfikuje credentials i tworzy sesję

5. **Dashboard** ładuje się automatycznie z kursami kryptowalut

### Scenariusz 2: Istniejący Użytkownik

1. **Użytkownik** otwiera http://localhost:8001
2. **System** sprawdza czy istnieje aktywna sesja (cookie)
3. Jeśli sesja ważna → **automatyczne przekierowanie do dashboardu**
4. Jeśli brak sesji → **formularz logowania**

### Scenariusz 3: Wylogowanie

1. **Użytkownik** klika "Wyloguj"
2. **System** usuwa sesję z bazy danych
3. **System** czyści cookie
4. **Przekierowanie** do formularza logowania

## 🔧 Zarządzanie Użytkownikami

### Tworzenie Użytkownika (CLI)

```bash
python3 create_user.py
```

### Tworzenie Użytkownika (Programmatically)

```python
from crypto_client.database import db

user = db.create_user(
    username="john",
    password="secret123",
    email="john@example.com",
    client_id="test_client",
    client_secret="test_secret_123",
    is_admin=False
)
```

### Weryfikacja Użytkownika

```python
from crypto_client.database import db

user = db.verify_user("john", "secret123")
if user:
    print(f"Logged in as: {user['username']}")
```

### Zarządzanie Sesjami

```python
from crypto_client.database import db

# Utwórz sesję
token = db.create_session(user_id=1, expires_in_hours=24)

# Weryfikuj sesję
session = db.verify_session(token)

# Usuń sesję (logout)
db.delete_session(token)

# Wyczyść wygasłe sesje
db.cleanup_expired_sessions()
```

## 🐛 Troubleshooting

### Problem: "Invalid username or password"
- Sprawdź czy użytkownik istnieje w bazie danych
- Upewnij się że używasz poprawnego hasła
- Sprawdź czy konto jest aktywne (`is_active=1`)

### Problem: "Not authenticated - please login first"
- Session cookie wygasła - zaloguj się ponownie
- Przeglądarka blokuje cookies - sprawdź ustawienia
- Niepoprawny session token

### Problem: "Database locked"
- Zamknij wszystkie połączenia do bazy danych
- Usuń plik `crypto_client_users.db-journal` jeśli istnieje
- Zrestartuj aplikację

### Problem: Nie można załadować kursów
- Sprawdź czy crypto-server działa (port 8000)
- Sprawdź czy użytkownik ma przypisane `client_id` i `client_secret`
- Sprawdź logi w terminalu

## 📚 Przykłady

### Przykład: Test Całego Flow

```bash
# 1. Uruchom serwery
./run-server.sh  # Terminal 1
./run-client.sh  # Terminal 2

# 2. Utwórz użytkownika
python3 create_user.py

# 3. Zaloguj się w przeglądarce
open http://localhost:8001

# 4. Zobacz kursy w dashboard
```

### Przykład: Test API z curl

```bash
# Login
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123"}' \
  -c cookies.txt

# Get currencies (używając zapisanych cookies)
curl http://localhost:8001/api/currencies \
  -b cookies.txt

# Logout
curl -X POST http://localhost:8001/api/auth/logout \
  -b cookies.txt
```

## 🎯 Następne Kroki

1. **Dodaj więcej funkcji:**
   - Zmiana hasła
   - Reset hasła przez email
   - Profil użytkownika
   - Historia logowań

2. **Ulepsz bezpieczeństwo:**
   - 2FA (Two-Factor Authentication)
   - Rate limiting
   - CAPTCHA przy logowaniu

3. **Monitoring:**
   - Logi logowań
   - Dashboard administracyjny
   - Alerty bezpieczeństwa

4. **Deployment:**
   - Konfiguracja HTTPS
   - Reverse proxy (nginx)
   - Docker Compose dla produkcji
