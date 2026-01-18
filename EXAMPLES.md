# OAuth2 M2M System - Przykłady użycia

## Szybki start

### 1. Uruchom crypto-server
```bash
./run-server.sh
```
Serwer będzie dostępny na: http://localhost:8000

### 2. Uruchom crypto-client
```bash
./run-client.sh
```
Klient będzie dostępny na: http://localhost:8001

### 3. Uruchom testy
```bash
python3 crypto-client/test_client.py
```

---

## Przykłady API

### Crypto-Client API

#### 1. Sprawdź status klienta
```bash
curl http://localhost:8001/api/status
```

#### 2. Zarejestruj klienta w serwerze
```bash
curl -X POST http://localhost:8001/api/register
```

#### 3. Zaloguj się (uzyskaj token)
```bash
curl -X POST http://localhost:8001/api/login
```

#### 4. Pobierz wszystkie kursy walut
```bash
curl http://localhost:8001/api/currencies
```

Przykładowa odpowiedź:
```json
[
  {
    "symbol": "BTC",
    "rate": 45123.45
  },
  {
    "symbol": "ETH",
    "rate": 3201.89
  },
  {
    "symbol": "SOL",
    "rate": 144.56
  }
]
```

#### 5. Pobierz konkretną walutę
```bash
curl http://localhost:8001/api/currencies/BTC
```

#### 6. Skonfiguruj własne credentials
```bash
curl -X POST http://localhost:8001/api/configure \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "moj-klient",
    "client_secret": "moje-tajne-haslo",
    "app_name": "Moja Aplikacja"
  }'
```

---

## Bezpośrednia komunikacja z Crypto-Server

### 1. Zarejestruj klienta bezpośrednio
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "direct-client",
    "client_secret": "secret123",
    "app_name": "Direct App"
  }'
```

### 2. Uzyskaj token (OAuth2 Client Credentials Grant)
```bash
curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "direct-client",
    "client_secret": "secret123"
  }'
```

Przykładowa odpowiedź:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Użyj tokenu do pobrania danych
```bash
TOKEN="twój_token_tutaj"

curl http://localhost:8000/api/currency/ \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Pobierz konkretną walutę
```bash
curl http://localhost:8000/api/currency/BTC \
  -H "Authorization: Bearer $TOKEN"
```

---

## Python - Programatyczne użycie

### Prosty przykład z httpx
```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        # 1. Rejestracja
        reg_response = await client.post(
            "http://localhost:8000/api/auth/register",
            json={
                "client_id": "python-client",
                "client_secret": "python-secret",
                "app_name": "Python App"
            }
        )
        print(reg_response.json())
        
        # 2. Uzyskanie tokenu
        token_response = await client.post(
            "http://localhost:8000/api/auth/token",
            json={
                "client_id": "python-client",
                "client_secret": "python-secret"
            }
        )
        token_data = token_response.json()
        token = token_data["access_token"]
        print(f"Token: {token[:30]}...")
        
        # 3. Pobieranie danych
        headers = {"Authorization": f"Bearer {token}"}
        rates_response = await client.get(
            "http://localhost:8000/api/currency/",
            headers=headers
        )
        rates = rates_response.json()
        
        for rate in rates:
            print(f"{rate['symbol']}: ${rate['rate']}")

asyncio.run(main())
```

### Użycie ClientService
```python
from crypto_client.client_service import ClientService
import asyncio

async def main():
    client = ClientService(
        server_url="http://localhost:8000",
        client_id="moj-klient",
        client_secret="moj-sekret"
    )
    
    # Rejestracja i logowanie
    await client.register_client()
    await client.get_access_token()
    
    # Pobieranie danych
    rates = await client.get_all_currency_rates()
    for rate in rates:
        print(f"{rate['symbol']}: ${rate['rate']}")
    
    # Konkretna waluta
    btc = await client.get_currency_rate("BTC")
    print(f"BTC: ${btc['rate']}")
    
    await client.close()

asyncio.run(main())
```

---

## JavaScript / Node.js przykład

```javascript
const axios = require('axios');

async function main() {
  const SERVER_URL = 'http://localhost:8000';
  const CLIENT_ID = 'js-client';
  const CLIENT_SECRET = 'js-secret';
  
  try {
    // 1. Rejestracja
    await axios.post(`${SERVER_URL}/api/auth/register`, {
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      app_name: 'JavaScript App'
    });
    
    // 2. Uzyskanie tokenu
    const tokenResponse = await axios.post(`${SERVER_URL}/api/auth/token`, {
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET
    });
    
    const token = tokenResponse.data.access_token;
    console.log('Token uzyskany:', token.substring(0, 30) + '...');
    
    // 3. Pobieranie danych z tokenem
    const ratesResponse = await axios.get(`${SERVER_URL}/api/currency/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    console.log('Kursy walut:');
    ratesResponse.data.forEach(rate => {
      console.log(`${rate.symbol}: $${rate.rate}`);
    });
    
  } catch (error) {
    console.error('Błąd:', error.response?.data || error.message);
  }
}

main();
```

---

## Testy

### Sprawdź czy wszystko działa
```bash
# Terminal 1: Uruchom serwer
./run-server.sh

# Terminal 2: Uruchom klienta
./run-client.sh

# Terminal 3: Uruchom testy
python3 crypto-client/test_client.py
```

### Testowanie ręczne przez Swagger UI

1. **Crypto-Server**: http://localhost:8000/docs
2. **Crypto-Client**: http://localhost:8001/docs

---

## Troubleshooting

### Błąd połączenia z bazą danych
```bash
docker-compose up -d
docker-compose ps  # Sprawdź czy baza działa
```

### Błąd 401 Unauthorized
- Sprawdź czy używasz prawidłowych credentials
- Sprawdź czy token nie wygasł (ważny przez 120 minut)
- Zarejestruj klienta ponownie

### Błąd importu w Python
```bash
# Zainstaluj zależności
pip3 install -r crypto-server/requirements.txt
pip3 install -r crypto-client/requirements.txt
```

### Port już zajęty
```bash
# Zmień port w pliku .env lub przy uruchomieniu
uvicorn crypto_client.main:app --port 8002
```
