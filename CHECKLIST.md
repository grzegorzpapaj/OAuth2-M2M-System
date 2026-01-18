# ✅ Checklist - Weryfikacja systemu OAuth2 M2M

## 📋 Lista kontrolna uruchomienia

### 1. Wymagania wstępne
- [ ] Python 3.10+ zainstalowany (`python3 --version`)
- [ ] Docker zainstalowany (`docker --version`)
- [ ] Docker Compose zainstalowany (`docker-compose --version`)
- [ ] pip zainstalowany (`pip3 --version`)
- [ ] Porty 8000, 8001, 5432 dostępne

### 2. Instalacja zależności
- [ ] Zainstalowano zależności serwera (`pip3 install -r crypto-server/requirements.txt`)
- [ ] Zainstalowano zależności klienta (`pip3 install -r crypto-client/requirements.txt`)
- [ ] Brak błędów podczas instalacji

### 3. Baza danych
- [ ] PostgreSQL uruchomiony (`docker-compose up -d`)
- [ ] Kontener działa (`docker-compose ps` pokazuje status "running")
- [ ] Port 5432 dostępny (`netstat -tuln | grep 5432`)

### 4. Crypto-Server
- [ ] Serwer uruchomiony (`./run-server.sh` lub ręcznie)
- [ ] Komunikat "Tabele gotowe!" wyświetlony
- [ ] Komunikat "Start generatora kursów!" wyświetlony
- [ ] Swagger UI dostępny (http://localhost:8000/docs)
- [ ] Endpoint `/` odpowiada (`curl http://localhost:8000/`)
- [ ] Waluty inicjalizowane (BTC, ETH, SOL)

### 5. Crypto-Client
- [ ] Klient uruchomiony (`./run-client.sh` lub ręcznie)
- [ ] Komunikat "Uruchamianie Crypto Client..." wyświetlony
- [ ] Swagger UI dostępny (http://localhost:8001/docs)
- [ ] Endpoint `/` odpowiada (`curl http://localhost:8001/`)
- [ ] Background task pobiera kursy co 10 sekund

### 6. OAuth2 Flow
- [ ] Rejestracja klienta działa (`POST /api/register`)
- [ ] Logowanie działa (`POST /api/token`)
- [ ] Token JWT zwracany poprawnie
- [ ] Token zawiera pole `exp` (expiration)
- [ ] Status pokazuje `authenticated: true`

### 7. Endpointy chronione
- [ ] `/api/currencies` zwraca listę walut
- [ ] `/api/currencies/BTC` zwraca kurs BTC
- [ ] `/api/currencies/ETH` zwraca kurs ETH
- [ ] `/api/currencies/SOL` zwraca kurs SOL
- [ ] Próba dostępu bez tokenu zwraca 401

### 8. Automatyczne funkcje
- [ ] Token automatycznie się odświeża po wygaśnięciu
- [ ] Kursy aktualizują się co 3 sekundy (widać zmiany)
- [ ] Background task klienta pobiera dane co 10 sekund
- [ ] Logi pokazują aktywność systemu

### 9. Testy
- [ ] `python3 quick-test.py` przechodzi pomyślnie
- [ ] `python3 crypto-client/test_client.py` przechodzi pomyślnie
- [ ] `python3 demo.py` działa poprawnie
- [ ] Wszystkie dema działają bez błędów

### 10. Dokumentacja
- [ ] README.md czytelny i kompletny
- [ ] QUICKSTART.md pomocny dla nowych użytkowników
- [ ] EXAMPLES.md zawiera działające przykłady
- [ ] ARCHITECTURE.md wyjaśnia strukturę
- [ ] Komentarze w kodzie są zrozumiałe

---

## 🔍 Testy funkcjonalności

### Test 1: Podstawowy OAuth2 Flow
```bash
# Powinno działać bez błędów
curl -X POST http://localhost:8001/api/register
curl -X POST http://localhost:8001/api/token
curl http://localhost:8001/api/currencies
```
- [ ] ✅ Działa

### Test 2: Bezpośredni dostęp do serwera
```bash
# Zarejestruj klienta bezpośrednio
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"client_id": "test123", "client_secret": "secret123", "app_name": "Test"}'

# Uzyskaj token
curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"client_id": "test123", "client_secret": "secret123"}'
```
- [ ] ✅ Działa

### Test 3: Użycie tokenu
```bash
# Ustaw token (skopiuj z poprzedniego wyniku)
TOKEN="<wklej_token_tutaj>"

# Pobierz dane
curl http://localhost:8000/api/currency/ \
  -H "Authorization: Bearer $TOKEN"
```
- [ ] ✅ Działa

### Test 4: Nieprawidłowe credentials
```bash
# Powinno zwrócić 401
curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"client_id": "fake", "client_secret": "wrong"}'
```
- [ ] ✅ Zwraca błąd 401

### Test 5: Brak tokenu
```bash
# Powinno zwrócić 401
curl http://localhost:8000/api/currency/
```
- [ ] ✅ Zwraca błąd 401

### Test 6: Nieprawidłowy token
```bash
# Powinno zwrócić 401
curl http://localhost:8000/api/currency/ \
  -H "Authorization: Bearer fake-token"
```
- [ ] ✅ Zwraca błąd 401

### Test 7: Aktualizacja kursów
```bash
# Pobierz kurs dwa razy z przerwą 5 sekund
curl http://localhost:8001/api/currencies/BTC
sleep 5
curl http://localhost:8001/api/currencies/BTC
# Kursy powinny się różnić (zmiana +/- 0.5%)
```
- [ ] ✅ Kursy się zmieniają

---

## 🐛 Troubleshooting Checklist

### Problem: Serwer nie startuje
- [ ] Sprawdzono czy port 8000 jest wolny (`lsof -i :8000`)
- [ ] Sprawdzono czy baza danych działa (`docker-compose ps`)
- [ ] Sprawdzono logi błędów w konsoli
- [ ] Zainstalowano wszystkie zależności
- [ ] Sprawdzono połączenie z bazą (`DATABASE_URL` poprawny)

### Problem: Klient nie łączy się z serwerem
- [ ] Serwer działa (`curl http://localhost:8000/`)
- [ ] `SERVER_URL` w konfiguracji klienta jest poprawny
- [ ] Brak firewall blokującego połączenie
- [ ] Port 8000 jest dostępny z localhost

### Problem: 401 Unauthorized
- [ ] Klient zarejestrowany (`POST /api/register`)
- [ ] Klient zalogowany (`POST /api/token`)
- [ ] Token nie wygasł (ważny 120 minut)
- [ ] Credentials są poprawne
- [ ] Token przekazywany w nagłówku `Authorization: Bearer`

### Problem: Database connection error
- [ ] Docker działa (`docker ps`)
- [ ] PostgreSQL kontener uruchomiony
- [ ] Port 5432 dostępny
- [ ] Credentials bazy są poprawne w `database.py`
- [ ] Poczekano 3-5 sekund po `docker-compose up`

### Problem: Import errors
- [ ] Uruchamianie z właściwego katalogu
- [ ] Python path ustawiony poprawnie
- [ ] Wszystkie pliki `__init__.py` istnieją
- [ ] Używany Python 3.10+

---

## ✨ Feature Checklist

### Zaimplementowane funkcjonalności:

#### OAuth2 Server (crypto-server)
- [x] Rejestracja klientów
- [x] Generowanie JWT tokenów
- [x] Walidacja credentials
- [x] Walidacja JWT przy każdym żądaniu
- [x] Chronione endpointy
- [x] Background task aktualizacji kursów
- [x] Baza danych PostgreSQL
- [x] SQLAlchemy ORM
- [x] FastAPI + async
- [x] Swagger UI dokumentacja

#### OAuth2 Client (crypto-client)
- [x] Automatyczna rejestracja
- [x] Uzyskiwanie tokenów
- [x] Automatyczne odświeżanie tokenów
- [x] Komunikacja z chronionymi endpointami
- [x] Background task pobierania danych
- [x] Własne API dla użytkowników
- [x] Obsługa błędów
- [x] Konfiguracja przez .env
- [x] Swagger UI dokumentacja

#### Bezpieczeństwo
- [x] Client credentials grant flow
- [x] JWT z czasem wygaśnięcia
- [x] Bearer token authentication
- [x] Walidacja podpisu JWT
- [x] HTTPException dla błędów auth
- [ ] ⚠️ Hashowanie client_secret (TODO: bcrypt)
- [ ] ⚠️ HTTPS/TLS (TODO: produkcja)
- [ ] ⚠️ Rate limiting (TODO: produkcja)

#### Dokumentacja
- [x] README.md
- [x] QUICKSTART.md
- [x] EXAMPLES.md
- [x] ARCHITECTURE.md
- [x] Inline comments w kodzie
- [x] Docstrings w funkcjach
- [x] Type hints

#### Testy i demo
- [x] quick-test.py
- [x] test_client.py
- [x] demo.py (interaktywne)
- [x] Przykłady cURL
- [x] Przykłady Python

#### DevOps
- [x] Docker Compose dla bazy
- [x] Shell scripts (run-server.sh, run-client.sh)
- [x] requirements.txt dla obu części
- [x] .env.example
- [x] .gitignore
- [ ] ⚠️ Dockerfile (TODO)
- [ ] ⚠️ CI/CD (TODO)

---

## 📊 Metryki jakości

### Kod
- [ ] Kod działa bez błędów
- [ ] Brak warnings w konsoli
- [ ] Async/await używane poprawnie
- [ ] Error handling zaimplementowany
- [ ] Type hints w większości funkcji
- [ ] Docstrings w publicznych funkcjach

### Performance
- [ ] Token cache działa (nie pobiera za każdym razem)
- [ ] Połączenia HTTP async
- [ ] Database queries async
- [ ] Background tasks nie blokują

### Dokumentacja
- [ ] Każdy plik ma jasny cel
- [ ] README wyjaśnia jak uruchomić
- [ ] Przykłady są działające
- [ ] Komentarze wyjaśniają "dlaczego", nie "co"

### User Experience
- [ ] Proste uruchomienie (3 komendy)
- [ ] Jasne komunikaty błędów
- [ ] Swagger UI działający
- [ ] Logi informatywne
- [ ] Auto-refresh przezroczysty dla użytkownika

---

## 🎓 Sprawdź czy rozumiesz

- [ ] Potrafię wyjaśnić OAuth2 Client Credentials Grant
- [ ] Rozumiem jak działają JWT tokeny
- [ ] Wiem kiedy token wygasa i jak się odświeża
- [ ] Rozumiem różnicę między client a server
- [ ] Potrafię dodać nowy endpoint
- [ ] Potrafię dodać nową kryptowalutę
- [ ] Rozumiem background tasks w FastAPI
- [ ] Potrafię debugować błędy 401

---

## 🚀 Gotowość do prezentacji

- [ ] System uruchamia się bez błędów
- [ ] Wszystkie testy przechodzą
- [ ] Demo działa płynnie
- [ ] Dokumentacja jest kompletna
- [ ] Potrafię wyjaśnić architekturę
- [ ] Potrafię pokazać OAuth2 flow
- [ ] Potrafię obsłużyć pytania
- [ ] Kod jest czysty i zrozumiały

---

## ✅ Finalna weryfikacja

Po zaznaczeniu wszystkich powyższych, uruchom:

```bash
# Test kompletny
python3 quick-test.py

# Jeśli wszystko ✅ - gotowe do użycia! 🎉
```

**Status projektu:** ⬜ W trakcie | ✅ Gotowy

**Data weryfikacji:** _______________

**Weryfikował:** _______________
