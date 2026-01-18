#!/bin/bash

# Skrypt uruchamiający crypto-client

echo "🚀 Uruchamianie Crypto Client..."
echo ""

# Sprawdź czy jesteśmy w odpowiednim katalogu
if [ ! -d "crypto-client" ]; then
    echo "❌ Uruchom skrypt z katalogu głównego projektu!"
    exit 1
fi

# Sprawdź czy zainstalowane są zależności
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Instalowanie zależności..."
    pip3 install -r crypto-client/requirements.txt
fi

# Dodaj katalog główny do PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Uruchom aplikację z katalogu głównego
echo "▶️  Uruchamianie serwera na porcie 8001..."
echo "📖 Dokumentacja API: http://localhost:8001/docs"
echo ""

# Uruchamiamy z katalogu głównego, podając pełną ścieżkę do modułu
python3 -m uvicorn crypto-client.main:app --reload --port 8001 --host 0.0.0.0