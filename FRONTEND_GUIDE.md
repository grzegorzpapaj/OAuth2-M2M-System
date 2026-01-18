# 🌐 Frontend - Przewodnik Użytkownika

Kompletny przewodnik po frontendzie Crypto Client.

## 🚀 Szybki Start

### 1. Uruchom całą aplikację

```bash
# Opcja 1: Uruchom wszystko jednym poleceniem
./run-frontend.sh

# Opcja 2: Ręcznie
# Terminal 1 - Crypto Server
cd crypto-server
uvicorn main:app --reload --port 8000

# Terminal 2 - Crypto Client
cd crypto-client
uvicorn main:app --reload --port 8001
```

### 2. Otwórz frontend
Przejdź do: **http://localhost:8001**

## 🔐 Proces Rejestracji i Logowania

### Krok 1: Administrator rejestruje klienta

Administrator musi najpierw zarejestrować klienta na **crypto-server** (port 8000):

```bash
# Przez terminal
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "my-frontend-app",
    "client_secret": "super-secure-password-123",
    "app_name": "My Crypto App"
  }'
```

**Lub przez Swagger UI**: http://localhost:8000/docs

Odpowiedź:
```json
{
  "client_id": "my-frontend-app",
  "app_name": "My Crypto App",
  "message": "Client registered successfully"
}
```

### Krok 2: Administrator przekazuje credentials

Administrator przekazuje użytkownikowi **BEZPIECZNYM kanałem**:
- 📧 **Email szyfrowany**
- 📞 **Telefon**
- 🤝 **Spotkanie osobiste**
- 🔒 **System zarządzania hasłami**

**Przekazane dane:**
- `client_id`: `my-frontend-app`
- `client_secret`: `super-secure-password-123`

### Krok 3: Użytkownik loguje się przez frontend

1. Otwórz **http://localhost:8001**
2. Wprowadź otrzymany **Client ID**
3. Wprowadź otrzymany **Client Secret**
4. Kliknij **Zaloguj**

Po zalogowaniu:
- ✅ Status zmienia się na "Zalogowany"
- ✅ Automatycznie ładują się kursy kryptowalut
- ✅ Odblokowują się wszystkie funkcje

## 🎯 Funkcje Frontendu

### Po zalogowaniu masz dostęp do:

#### 1. **Odśwież Kursy** 🔄
- Pobiera najnowsze kursy wszystkich kryptowalut
- Wyświetla: symbol, nazwę, cenę, zmianę 24h
- Automatycznie aktualizuje się po zalogowaniu

#### 2. **Test Połączenia** ✅
- Sprawdza połączenie z crypto-server
- Weryfikuje czy token JWT jest ważny
- Pokazuje status komunikacji

#### 3. **Sprawdź Status** 📊
- Wyświetla informacje o zalogowanym kliencie
- Pokazuje client_id
- Informuje czy jesteś uwierzytelniony

#### 4. **Wyloguj** 🚪
- Czyści lokalny token
- Wraca do ekranu logowania
- Czyści formularz

## 📱 Interfejs Użytkownika

### Ekran Logowania
```
┌─────────────────────────────────────┐
│  ℹ️  Uwaga                           │
│  Administrator musi zarejestrować   │
│  klienta i przekazać credentials    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  🔐 Logowanie                        │
│                                     │
│  Client ID: [________________]      │
│  Client Secret: [____________]      │
│                                     │
│  [      Zaloguj      ]              │
└─────────────────────────────────────┘
```

### Dashboard (po zalogowaniu)
```
┌─────────────────────────────────────────────────┐
│  👋 Witaj!                          [Wyloguj]  │
│  Jesteś zalogowany jako: my-app                │
└─────────────────────────────────────────────────┘

┌──────────┐  ┌──────────┐  ┌──────────┐
│ Odśwież  │  │   Test   │  │ Sprawdź  │
│  Kursy   │  │Połączenia│  │  Status  │
└──────────┘  └──────────┘  └──────────┘

┌─────────┐  ┌─────────┐  ┌─────────┐
│  BTC    │  │  ETH    │  │  DOGE   │
│ $45000  │  │ $3200   │  │ $0.08   │
│ ↗ +2.5% │  │ ↗ +1.8% │  │ ↘ -0.5% │
└─────────┘  └─────────┘  └─────────┘
```

## 🎨 Wygląd i Feel

### Design System
- **Kolory**: Gradient od slate-900 przez blue-900
- **Karty**: Glass morphism z backdrop blur
- **Przyciski**: Gradient z hover effects
- **Animacje**: Smooth transitions
- **Responsive**: Desktop & Mobile

### Statusy Wizualne
- 🔴 **Czerwony** - Niezalogowany
- 🟢 **Zielony** - Zalogowany (pulsujący)
- 🔵 **Niebieski** - Informacje
- 🟡 **Żółty** - Ostrzeżenia
- ⚪ **Biały/Szary** - Neutralny

## 🔧 Techniczne Detale

### Endpointy Używane przez Frontend

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/api/token` | POST | Logowanie (client_id + secret) |
| `/api/status` | GET | Status uwierzytelnienia |
| `/api/currencies` | GET | Wszystkie kursy walut |
| `/api/test-server` | GET | Test połączenia |

### Przechowywanie Danych
- **Token JWT**: W pamięci JavaScript (zmienna `accessToken`)
- **Client ID**: W pamięci JavaScript (zmienna `currentClientId`)
- **Brak localStorage/cookies** - zwiększone bezpieczeństwo

### Zarządzanie Tokenem
- Token jest **tylko w pamięci** - nie przetrwa odświeżenia strony
- Po odświeżeniu strony - **wymaga ponownego logowania**
- Token wygasa po **120 minutach** (konfigurowalny na serwerze)

## ❓ FAQ

### Q: Czy mogę zarejestrować się sam przez frontend?
**A:** Nie. Rejestracja odbywa się TYLKO przez administratora na crypto-server. To celowa decyzja bezpieczeństwa w modelu OAuth2 Client Credentials.

### Q: Dlaczego po odświeżeniu strony muszę logować się ponownie?
**A:** Token JWT jest przechowywany tylko w pamięci JavaScript dla bezpieczeństwa. Nie używamy localStorage/cookies.

### Q: Jak długo ważny jest token?
**A:** Domyślnie 120 minut (2 godziny). Po tym czasie musisz się zalogować ponownie.

### Q: Czy mogę zmienić hasło (client_secret)?
**A:** Tak, ale tylko administrator może to zrobić przez aktualizację w bazie danych serwera.

### Q: Czy frontend działa offline?
**A:** Nie. Frontend wymaga połączenia z crypto-client (port 8001), który z kolei łączy się z crypto-server (port 8000).

### Q: Czy mogę używać frontendu na telefonie?
**A:** Tak! Frontend jest w pełni responsywny i działa na urządzeniach mobilnych.

## 🐛 Rozwiązywanie Problemów

### Problem: "Błąd połączenia"
**Rozwiązanie:**
```bash
# Sprawdź czy serwisy działają
curl http://localhost:8000/  # crypto-server
curl http://localhost:8001/  # crypto-client

# Uruchom ponownie
./run-frontend.sh
```

### Problem: "Błąd logowania: Invalid credentials"
**Rozwiązanie:**
- Sprawdź czy client_id i client_secret są poprawne
- Sprawdź czy klient jest zarejestrowany na serwerze
- Sprawdź logi serwera: `docker-compose logs -f`

### Problem: "401 Unauthorized" przy pobieraniu kursów
**Rozwiązanie:**
- Token wygasł - zaloguj się ponownie
- Sprawdź status: kliknij "Sprawdź Status"

### Problem: "CORS Error"
**Rozwiązanie:**
- FastAPI już obsługuje CORS
- Sprawdź czy używasz `http://localhost:8001` a nie `http://127.0.0.1:8001`

## 🎬 Przykładowy Workflow

```bash
# 1. Administrator uruchamia system
./run-frontend.sh

# 2. Administrator rejestruje klienta
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"client_id": "alice-app", "client_secret": "alice123", "app_name": "Alice App"}'

# 3. Administrator przekazuje Alice:
# - client_id: alice-app
# - client_secret: alice123

# 4. Alice otwiera przeglądarkę
# http://localhost:8001

# 5. Alice loguje się
# - Wpisuje: alice-app
# - Wpisuje: alice123
# - Klika: Zaloguj

# 6. Alice widzi dashboard z kursami kryptowalut! 🎉
```

## 📚 Dalsze Kroki

- 📖 Zobacz [README.md](README.md) - główna dokumentacja
- 🔧 Zobacz [crypto-client/README.md](crypto-client/README.md) - dokumentacja API
- 💡 Zobacz [EXAMPLES.md](EXAMPLES.md) - przykłady użycia
- 🎨 Zobacz [crypto-client/static/README.md](crypto-client/static/README.md) - dokumentacja techniczna frontendu

---

**Miłego korzystania z Crypto Client Frontend! 🚀**
