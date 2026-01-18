# OAuth2 M2M System - Quick Start Guide

## 🚀 Szybkie uruchomienie (5 minut)

### Krok 1: Przygotowanie środowiska

```bash
# Przejdź do katalogu projektu
cd /home/pi/studia/OAuth2-M2M-System

# Zainstaluj zależności
pip3 install -r crypto-server/requirements.txt
pip3 install -r crypto-client/requirements.txt
```

### Krok 2: Uruchom bazę danych

```bash
# Uruchom PostgreSQL w Dockerze
docker-compose up -d

# Sprawdź czy działa
docker-compose ps
```

Powinieneś zobaczyć:
```
NAME                COMMAND                  SERVICE             STATUS
oauth2-m2m-db-1    "docker-entrypoint.s…"   db                  running
```

### Krok 3: Uruchom Crypto-Server

```bash
# Terminal 1
./run-server.sh

# LUB ręcznie:
cd crypto-server
uvicorn main:app --reload --port 8000
```

Poczekaj aż zobaczysz:
```
✅ Tabele gotowe!
🚀 Start generatora kursów!
```

Otwórz w przeglądarce: **http://localhost:8000/docs**

### Krok 4: Uruchom Crypto-Client

```bash
# Terminal 2
./run-client.sh

# LUB ręcznie:
cd crypto-client
uvicorn main:app --reload --port 8001
```

Poczekaj aż zobaczysz:
```
🚀 Uruchamianie Crypto Client...
✅ Klient uwierzytelniony i gotowy!
```

Otwórz w przeglądarce: **http://localhost:8001/docs**

### Krok 5: Testowanie

```bash
# Terminal 3 - Quick test
python3 quick-test.py

# LUB pełny test klienta
python3 crypto-client/test_client.py

# LUB interaktywne demo
python3 demo.py
```

---

## ✅ Weryfikacja

### Sprawdź czy wszystko działa:

1. **Baza danych:**
```bash
docker-compose ps
# Powinno pokazać: db - running
```

2. **Serwer:**
```bash
curl http://localhost:8000/
# Powinno zwrócić: {"message": "Server is running nicely!"}
```

3. **Klient:**
```bash
curl http://localhost:8001/
# Powinno zwrócić status klienta
```

4. **OAuth2 Flow:**
```bash
# Zarejestruj klienta
curl -X POST http://localhost:8001/api/register

# Zaloguj się
curl -X POST http://localhost:8001/api/token

# Pobierz kursy
curl http://localhost:8001/api/currencies
```

---

## 🎯 Pierwsze kroki po uruchomieniu

### Scenariusz 1: Użycie przez Swagger UI (najprostsze)

1. Otwórz http://localhost:8001/docs
2. Kliknij `POST /api/register` → Try it out → Execute
3. Kliknij `POST /api/token` → Try it out → Execute
4. Kliknij `GET /api/currencies` → Try it out → Execute
5. Zobacz kursy kryptowalut! 🎉

### Scenariusz 2: Użycie przez cURL

```bash
# 1. Rejestracja
curl -X POST http://localhost:8001/api/register

# 2. Login (uzyskaj token)
curl -X POST http://localhost:8001/api/token

# 3. Pobierz wszystkie kursy
curl http://localhost:8001/api/currencies

# 4. Pobierz konkretną walutę
curl http://localhost:8001/api/currencies/BTC
```

### Scenariusz 3: Bezpośrednia komunikacja z serwerem

```bash
# 1. Zarejestruj klienta
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"client_id": "test", "client_secret": "secret", "app_name": "Test App"}'

# 2. Uzyskaj token
TOKEN=$(curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"client_id": "test", "client_secret": "secret"}' \
  | jq -r '.access_token')

# 3. Użyj tokenu
curl http://localhost:8000/api/currency/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📊 Co zobaczysz

### Kursy kryptowalut (aktualizowane co 3 sekundy):
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

### W konsoli serwera:
```
🌱 Inicjalizacja walut startowych...
🚀 Start generatora kursów!
INFO:     127.0.0.1:xxxxx - "POST /api/auth/register HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST /api/auth/token HTTP/1.1" 200 OK
```

### W konsoli klienta:
```
🚀 Uruchamianie Crypto Client...
✅ Klient uwierzytelniony i gotowy!
📊 Pobrano kursy: 3 walut
  BTC: $45123.45
  ETH: $3201.89
  SOL: $144.56
```

---

## 🛠️ Rozwiązywanie problemów

### Problem: Baza danych nie działa
```bash
docker-compose down
docker-compose up -d
sleep 3
```

### Problem: Port zajęty (8000 lub 8001)
```bash
# Znajdź proces
lsof -i :8000
# Zabij proces
kill -9 <PID>

# LUB użyj innego portu
uvicorn main:app --port 8002
```

### Problem: Import errors
```bash
# Upewnij się że jesteś w odpowiednim katalogu
cd /home/pi/studia/OAuth2-M2M-System

# Reinstaluj zależności
pip3 install --upgrade -r crypto-server/requirements.txt
pip3 install --upgrade -r crypto-client/requirements.txt
```

### Problem: 401 Unauthorized
```bash
# Zarejestruj ponownie
curl -X POST http://localhost:8001/api/register
curl -X POST http://localhost:8001/api/token
```

### Problem: Can't connect to server
```bash
# Sprawdź czy serwer działa
curl http://localhost:8000/

# Jeśli nie - uruchom go
./run-server.sh
```

---

## 📚 Dalsze kroki

1. **Eksploruj API:**
   - http://localhost:8000/docs (Server)
   - http://localhost:8001/docs (Client)

2. **Uruchom testy:**
   ```bash
   python3 quick-test.py
   python3 crypto-client/test_client.py
   ```

3. **Wypróbuj demo:**
   ```bash
   python3 demo.py
   ```

4. **Przeczytaj dokumentację:**
   - [README.md](README.md) - Pełna dokumentacja
   - [EXAMPLES.md](EXAMPLES.md) - Przykłady użycia
   - [ARCHITECTURE.md](ARCHITECTURE.md) - Architektura systemu

5. **Zmodyfikuj kod:**
   - Dodaj nowe kryptowaluty w `crypto-server/tasks.py`
   - Zmień credentials w `crypto-client/.env`
   - Dodaj nowe endpointy

---

## 🎓 Kluczowe koncepcje

### OAuth2 Client Credentials Grant:
1. Klient ma `client_id` i `client_secret`
2. Klient wysyła credentials do `/auth/token`
3. Serwer zwraca JWT token
4. Klient używa tokenu: `Authorization: Bearer <token>`
5. Token wygasa po 120 minutach

### Automatyczne odświeżanie:
- `ClientService.ensure_authenticated()` sprawdza token
- Jeśli wygasł - automatycznie pobiera nowy
- Nie musisz się martwić o wygaśnięcie!

### Background Tasks:
- **Serwer:** Aktualizuje kursy co 3 sekundy
- **Klient:** Pobiera kursy co 10 sekund
- Działa asynchronicznie w tle

---

## 🎉 Gotowe!

Twój system OAuth2 M2M działa!

**Przydatne komendy:**
```bash
./run-server.sh          # Uruchom serwer
./run-client.sh          # Uruchom klienta
python3 quick-test.py    # Szybki test
python3 demo.py          # Interaktywne demo
docker-compose ps        # Status bazy danych
```

**Przydatne linki:**
- 📖 Server API: http://localhost:8000/docs
- 📖 Client API: http://localhost:8001/docs
- 🗄️ PostgreSQL: localhost:5432
