#!/bin/bash

# Kolory
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🧪 Test Frontendu Crypto Client         ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""

# Krok 1: Sprawdź czy serwisy działają
echo -e "${YELLOW}📡 Krok 1: Sprawdzam czy serwisy działają...${NC}"
echo ""

if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Crypto-server działa (port 8000)${NC}"
else
    echo -e "${RED}❌ Crypto-server nie działa!${NC}"
    echo -e "${YELLOW}   Uruchom: cd crypto-server && uvicorn main:app --reload --port 8000${NC}"
    exit 1
fi

if curl -s http://localhost:8001/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Crypto-client działa (port 8001)${NC}"
else
    echo -e "${RED}❌ Crypto-client nie działa!${NC}"
    echo -e "${YELLOW}   Uruchom: cd crypto-client && uvicorn main:app --reload --port 8001${NC}"
    exit 1
fi

echo ""

# Krok 2: Zarejestruj testowego klienta
echo -e "${YELLOW}📝 Krok 2: Rejestruję testowego klienta...${NC}"
echo ""

RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "frontend-test",
    "client_secret": "test-secret-123",
    "app_name": "Frontend Test App"
  }')

if echo "$RESPONSE" | grep -q "successfully"; then
    echo -e "${GREEN}✅ Klient zarejestrowany!${NC}"
    echo -e "${BLUE}   Client ID: frontend-test${NC}"
    echo -e "${BLUE}   Client Secret: test-secret-123${NC}"
else
    echo -e "${YELLOW}⚠️  Klient może już istnieć (to OK!)${NC}"
    echo -e "${BLUE}   Client ID: frontend-test${NC}"
    echo -e "${BLUE}   Client Secret: test-secret-123${NC}"
fi

echo ""

# Krok 3: Test logowania przez API
echo -e "${YELLOW}🔐 Krok 3: Testuję logowanie przez API...${NC}"
echo ""

LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8001/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "frontend-test",
    "client_secret": "test-secret-123"
  }')

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo -e "${GREEN}✅ Logowanie przez API działa!${NC}"
    TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    echo -e "${BLUE}   Token otrzymany (pierwsze 50 znaków): ${TOKEN:0:50}...${NC}"
else
    echo -e "${RED}❌ Logowanie nie powiodło się!${NC}"
    echo "$LOGIN_RESPONSE"
    exit 1
fi

echo ""

# Krok 4: Test pobierania kursów
echo -e "${YELLOW}💰 Krok 4: Testuję pobieranie kursów...${NC}"
echo ""

CURRENCIES_RESPONSE=$(curl -s http://localhost:8001/api/currencies \
  -H "Authorization: Bearer $TOKEN")

if echo "$CURRENCIES_RESPONSE" | grep -q "BTC"; then
    echo -e "${GREEN}✅ Pobieranie kursów działa!${NC}"
    COUNT=$(echo "$CURRENCIES_RESPONSE" | grep -o "symbol" | wc -l)
    echo -e "${BLUE}   Znaleziono $COUNT kryptowalut${NC}"
else
    echo -e "${RED}❌ Nie można pobrać kursów!${NC}"
    echo "$CURRENCIES_RESPONSE"
    exit 1
fi

echo ""

# Krok 5: Test frontendu
echo -e "${YELLOW}🌐 Krok 5: Sprawdzam frontend...${NC}"
echo ""

FRONTEND_RESPONSE=$(curl -s http://localhost:8001/)

if echo "$FRONTEND_RESPONSE" | grep -q "Crypto Client"; then
    echo -e "${GREEN}✅ Frontend działa!${NC}"
    echo -e "${BLUE}   URL: http://localhost:8001${NC}"
else
    echo -e "${RED}❌ Frontend nie odpowiada poprawnie!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ Wszystkie testy przeszły pomyślnie!  ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}🎯 Następne kroki:${NC}"
echo -e "   1. Otwórz przeglądarkę: ${YELLOW}http://localhost:8001${NC}"
echo -e "   2. Zaloguj się używając:${NC}"
echo -e "      ${GREEN}Client ID:${NC} frontend-test"
echo -e "      ${GREEN}Client Secret:${NC} test-secret-123"
echo -e "   3. Ciesz się kursami kryptowalut! 🚀"
echo ""
echo -e "${BLUE}📚 Dokumentacja:${NC}"
echo -e "   - Frontend Guide: ${YELLOW}FRONTEND_GUIDE.md${NC}"
echo -e "   - API Docs: ${YELLOW}http://localhost:8001/docs${NC}"
echo ""
