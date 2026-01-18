#!/bin/bash

# Kolory
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🚀 OAuth2 M2M System - Frontend     ║${NC}"
echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
echo ""

# Sprawdź czy crypto-server działa
echo -e "${YELLOW}📡 Sprawdzam crypto-server...${NC}"
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Crypto-server działa (port 8000)${NC}"
else
    echo -e "${YELLOW}⚠️  Crypto-server nie działa. Uruchamiam...${NC}"
    cd crypto-server
    uvicorn main:app --reload --port 8000 &
    SERVER_PID=$!
    cd ..
    sleep 2
fi

echo ""
echo -e "${YELLOW}🌐 Uruchamiam crypto-client z frontendem...${NC}"
cd crypto-client
uvicorn main:app --reload --port 8001 &
CLIENT_PID=$!
cd ..

sleep 3

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║        ✅ System gotowy!               ║${NC}"
echo -e "${GREEN}╔═══════════════════════════════════════╗${NC}"
echo ""
echo -e "${BLUE}🔐 Crypto Server:${NC} http://localhost:8000"
echo -e "${BLUE}🎨 Frontend Dashboard:${NC} http://localhost:8001"
echo -e "${BLUE}📚 API Docs (Client):${NC} http://localhost:8001/docs"
echo -e "${BLUE}📚 API Docs (Server):${NC} http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}📝 Otwórz przeglądarkę na:${NC} ${GREEN}http://localhost:8001${NC}"
echo ""
echo -e "${YELLOW}Aby zatrzymać serwery, naciśnij Ctrl+C${NC}"

# Czekaj na Ctrl+C
trap "echo -e '\n${YELLOW}Zatrzymuję serwery...${NC}'; kill $SERVER_PID $CLIENT_PID 2>/dev/null; exit" INT

wait
