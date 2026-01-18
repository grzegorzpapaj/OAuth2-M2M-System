# 🔄 Architektura Endpointów - Podsumowanie

## Flow Logowania

```
┌─────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│                 │         │                  │         │                  │
│   Frontend      │ POST    │  Crypto-Client   │ POST    │  Crypto-Server   │
│   (Browser)     │────────>│  (Port 8001)     │────────>│  (Port 8000)     │
│                 │         │                  │         │                  │
└─────────────────┘         └──────────────────┘         └──────────────────┘
                                                          
   /api/token                  /api/auth/token
   + client_id                 + client_id
   + client_secret             + client_secret
                                                          
   <────────────               <────────────
   { access_token }            { access_token }
```

## Endpointy

### Frontend → Crypto-Client (port 8001)

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/api/token` | POST | Logowanie (client_id + secret) → zwraca JWT |
| `/api/status` | GET | Status uwierzytelnienia |
| `/api/currencies` | GET | Wszystkie kursy (wymaga Bearer token) |
| `/api/test-server` | GET | Test połączenia (wymaga Bearer token) |

### Crypto-Client → Crypto-Server (port 8000)

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/api/auth/register` | POST | Rejestracja klienta (admin) |
| `/api/auth/token` | POST | Uzyskanie JWT tokenu |
| `/api/currency/` | GET | Wszystkie kursy (wymaga Bearer token) |
| `/api/currency/{symbol}` | GET | Konkretna waluta (wymaga Bearer token) |

## Konfiguracja

### client_service.py (POPRAWNIE SKONFIGUROWANE ✅)
```python
url = f"{self.server_url}/api/auth/token"  # Port 8000
# server_url = "http://localhost:8000"
```

### routes.py (POPRAWNIE SKONFIGUROWANE ✅)
```python
@router.post("/token")  # Endpoint dla frontendu
async def get_token(request: TokenRequest):
    # Wywołuje client_service.get_access_token()
    # który uderza w http://localhost:8000/api/auth/token
```

### index.html (POPRAWNIE SKONFIGUROWANE ✅)
```javascript
const response = await fetch('/api/token', {  // Port 8001
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        client_id: clientId,
        client_secret: clientSecret
    })
});
```

## Testowanie

### 1. Zarejestruj klienta na serwerze (port 8000)
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "test-app",
    "client_secret": "test-secret",
    "app_name": "Test App"
  }'
```

### 2. Zaloguj się przez crypto-client (port 8001)
```bash
curl -X POST http://localhost:8001/api/token \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "test-app",
    "client_secret": "test-secret"
  }'
```

### 3. Lub zaloguj się przez frontend
- Otwórz: http://localhost:8001
- Wpisz: client_id = test-app
- Wpisz: client_secret = test-secret
- Kliknij: Zaloguj

---

**Status**: ✅ Wszystko poprawnie skonfigurowane!
