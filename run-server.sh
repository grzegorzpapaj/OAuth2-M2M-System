#!/bin/bash

# Skrypt uruchamiający crypto-server

echo "🚀 Uruchamianie Crypto Server..."
echo ""

# Sprawdź czy jesteśmy w odpowiednim katalogu
if [ ! -d "crypto-server" ]; then
    echo "❌ Uruchom skrypt z katalogu głównego projektu!"
    exit 1
fi

# Sprawdź czy docker compose jest uruchomiony
if ! docker ps | grep -q postgres; then
    echo "🐳 Uruchamianie bazy danych PostgreSQL..."
    docker-compose down
    docker-compose up -d
    
    echo "⏳ Czekam na uruchomienie bazy danych..."
    sleep 10
fi

# Znajdź nazwę kontenera postgres
POSTGRES_CONTAINER=$(docker ps --filter "ancestor=postgres:16-alpine" --format "{{.Names}}" | head -n 1)

if [ -z "$POSTGRES_CONTAINER" ]; then
    # Spróbuj znaleźć po nazwie
    POSTGRES_CONTAINER=$(docker ps --format "{{.Names}}" | grep db | head -n 1)
fi

# Sprawdź czy baza odpowiada
if [ ! -z "$POSTGRES_CONTAINER" ]; then
    echo "📊 Sprawdzam połączenie z bazą danych ($POSTGRES_CONTAINER)..."
    for i in {1..30}; do
        if docker exec "$POSTGRES_CONTAINER" pg_isready -U crypto-server > /dev/null 2>&1; then
            echo "✅ Baza danych gotowa!"
            break
        fi
        echo "   Próba $i/30..."
        sleep 1
    done
fi

# Sprawdź czy zainstalowane są zależności
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Instalowanie zależności..."
    pip3 install -r crypto-server/requirements.txt
fi

# Dodaj katalog główny do PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Uruchom aplikację z katalogu głównego
echo "▶️  Uruchamianie serwera na porcie 8000..."
echo "📖 Dokumentacja API: http://localhost:8000/docs"
echo ""

# Uruchamiamy z katalogu głównego, podając pełną ścieżkę do modułu
# python3 -m uvicorn crypto-server/main:app --reload --port 8000 --host 0.0.0.0
python3 -m uvicorn crypto-server.main:app --reload
