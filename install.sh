#!/bin/bash

# Instalator zależności dla OAuth2 M2M System
# Uruchom ten skrypt aby zainstalować wszystkie wymagane pakiety

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║                    🔧 OAuth2 M2M System - Instalator                         ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Sprawdź Python
echo "🐍 Sprawdzanie wersji Python..."
python3 --version || {
    echo "❌ Python 3 nie jest zainstalowany!"
    exit 1
}

# Sprawdź pip
echo "📦 Sprawdzanie pip..."
pip3 --version || {
    echo "❌ pip3 nie jest zainstalowany!"
    exit 1
}

# Sprawdź Docker
echo "🐳 Sprawdzanie Docker..."
docker --version || {
    echo "⚠️  Docker nie jest zainstalowany - będzie potrzebny do bazy danych!"
}

# Sprawdź Docker Compose
echo "🐳 Sprawdzanie Docker Compose..."
docker-compose --version || {
    echo "⚠️  Docker Compose nie jest zainstalowany!"
}

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Instalacja zależności serwera
echo "📥 Instalowanie zależności crypto-server..."
pip3 install -r crypto-server/requirements.txt || {
    echo "❌ Błąd podczas instalacji zależności serwera!"
    exit 1
}
echo "✅ Zależności serwera zainstalowane"
echo ""

# Instalacja zależności klienta
echo "📥 Instalowanie zależności crypto-client..."
pip3 install -r crypto-client/requirements.txt || {
    echo "❌ Błąd podczas instalacji zależności klienta!"
    exit 1
}
echo "✅ Zależności klienta zainstalowane"
echo ""

# Kopiuj .env.example do .env jeśli nie istnieje
if [ ! -f crypto-client/.env ]; then
    echo "📝 Tworzenie pliku .env dla klienta..."
    cp crypto-client/.env.example crypto-client/.env
    echo "✅ Plik .env utworzony"
else
    echo "ℹ️  Plik .env już istnieje"
fi
echo ""

# Sprawdź czy Docker działa
echo "🐳 Sprawdzanie czy Docker działa..."
if docker ps &>/dev/null; then
    echo "✅ Docker działa"
    
    # Sprawdź czy baza już uruchomiona
    if docker-compose ps | grep -q "Up"; then
        echo "ℹ️  Baza danych już działa"
    else
        echo "🚀 Uruchamianie bazy danych..."
        docker-compose up -d
        echo "⏳ Czekanie 3 sekundy na inicjalizację bazy..."
        sleep 3
        echo "✅ Baza danych uruchomiona"
    fi
else
    echo "⚠️  Docker nie działa - uruchom go przed startem serwera"
fi

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""
echo "✅ Instalacja zakończona pomyślnie!"
echo ""
echo "📋 Następne kroki:"
echo ""
echo "  1. Uruchom serwer:"
echo "     ./run-server.sh"
echo "     (lub: cd crypto-server && uvicorn main:app --reload --port 8000)"
echo ""
echo "  2. W nowym terminalu, uruchom klienta:"
echo "     ./run-client.sh"
echo "     (lub: cd crypto-client && uvicorn main:app --reload --port 8001)"
echo ""
echo "  3. Uruchom testy:"
echo "     python3 quick-test.py"
echo ""
echo "  4. Otwórz w przeglądarce:"
echo "     Server:  http://localhost:8000/docs"
echo "     Client:  http://localhost:8001/docs"
echo ""
echo "📚 Dokumentacja:"
echo "  • README.md       - Pełna dokumentacja"
echo "  • QUICKSTART.md   - Przewodnik szybkiego startu"
echo "  • EXAMPLES.md     - Przykłady użycia"
echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
