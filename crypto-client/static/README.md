# Crypto Client - Frontend

Prosty, nowoczesny frontend dla Crypto Client zbudowany z HTML, JavaScript i Tailwind CSS.

## 🎨 Funkcje

- ✅ **Logowanie** - Zaloguj się używając credentials od administratora
- ✅ **Dashboard** - Przegląd kursów kryptowalut
- ✅ **Responsywny design** - Działa na wszystkich urządzeniach
- ✅ **Nowoczesny UI** - Tailwind CSS z gradientami i animacjami
- ✅ **Bezpieczeństwo** - Rejestracja tylko przez administratora serwera

## 🚀 Uruchomienie

Frontend jest serwowany przez FastAPI:

```bash
cd crypto-client
uvicorn main:app --reload --port 8001
```

Otwórz przeglądarkę: **http://localhost:8001**

## 📖 Jak używać

### Proces Rejestracji (Po stronie administratora)

Administrator musi najpierw zarejestrować klienta na **crypto-server**:

```bash
# Na serwerze (port 8000)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"client_id": "my-app", "client_secret": "super-secret", "app_name": "My App"}'
```

Administrator przekazuje Ci bezpiecznym kanałem:
- **Client ID**: np. `my-app`
- **Client Secret**: np. `super-secret`

### Logowanie przez Frontend

1. Otwórz **http://localhost:8001**
2. Wprowadź **Client ID** otrzymany od administratora
3. Wprowadź **Client Secret** otrzymany od administratora
4. Kliknij **Zaloguj**
5. Po zalogowaniu automatycznie załadują się kursy kryptowalut

### Funkcje po zalogowaniu

- **Odśwież Kursy** - Pobierz najnowsze kursy kryptowalut
- **Test Połączenia** - Sprawdź połączenie z crypto-server
- **Sprawdź Status** - Zobacz informacje o swoim tokenie JWT

## 🎯 Endpointy

Frontend komunikuje się z tymi endpointami crypto-client:

- `POST /api/login` - Logowanie i uzyskanie tokenu JWT
- `GET /api/status` - Status uwierzytelnienia
- `GET /api/currencies` - Wszystkie kursy kryptowalut
- `GET /api/test-server` - Test połączenia z crypto-server

## 🔐 Model Bezpieczeństwa

```
┌─────────────┐                  ┌──────────────┐                  ┌─────────────┐
│             │  1. Rejestruje   │              │                  │             │
│ Admin       │ ────────────────>│ Crypto       │                  │ Crypto      │
│ (Serwer)    │  client_id +     │ Server       │                  │ Client      │
│             │  secret          │              │                  │             │
└─────────────┘                  └──────────────┘                  └─────────────┘
      │                                                                    ▲
      │                                                                    │
      │  2. Przekazuje bezpiecznym kanałem                                │
      │  (email/spotkanie/telefon)                                        │
      │                                                                    │
      └────────────────────────────────────────────────────────────────>  │
                          client_id + secret                               │
                                                                           │
                          3. Użytkownik loguje się                         │
                          przez frontend ─────────────────────────────────┘
```

## 💡 Technologie

- **HTML5** - Struktura
- **Tailwind CSS** - Style (CDN)
- **JavaScript** - Logika (Vanilla JS, Fetch API)
- **FastAPI** - Backend API & serwer statyczny

## 🎬 Demo Flow

1. **Administrator** rejestruje klienta na serwerze (crypto-server:8000)
2. **Administrator** przekazuje credentials użytkownikowi
3. **Użytkownik** otwiera frontend (crypto-client:8001)
4. **Użytkownik** loguje się używając otrzymanych credentials
5. **Frontend** wyświetla kursy kryptowalut z serwera
