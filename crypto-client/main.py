"""
Crypto Client - OAuth2 Client Credentials Grant
Komunikuje się z crypto-server używając OAuth2
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .client_service import ClientService
from .routes import router as client_router, set_client_service
import asyncio
import os

app = FastAPI(title="Crypto Client", version="1.0.0")

# Mount static files directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Globalna instancja serwisu klienta
client_service = ClientService()

# Ustaw w routes
set_client_service(client_service)

@app.on_event("startup")
async def startup():
    """Inicjalizacja klienta przy starcie"""
    print("🚀 Uruchamianie Crypto Client...")
    
    # Próba zalogowania przy starcie
    try:
        await client_service.ensure_authenticated()
        print("✅ Klient uwierzytelniony i gotowy!")
    except Exception as e:
        print(f"⚠️  Nie udało się uwierzytelnić przy starcie: {e}")
        print("💡 Użyj endpointu /register lub /login aby się uwierzytelnić")
    
    # Opcjonalnie: uruchom task pobierający kursy w tle
    asyncio.create_task(background_currency_fetcher())

@app.on_event("shutdown")
async def shutdown():
    """Czyszczenie zasobów przy wyłączeniu"""
    await client_service.close()
    print("👋 Crypto Client zatrzymany")

# Dodaj router z endpointami
app.include_router(client_router, prefix="/api")

@app.get("/")
async def root():
    """Serwuj frontend HTML"""
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/api")
async def api_root():
    """API endpoint główny"""
    return {
        "message": "Crypto Client is running",
        "authenticated": client_service.is_authenticated(),
        "server_url": client_service.server_url
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "authenticated": client_service.is_authenticated()
    }

async def background_currency_fetcher():
    """Przykładowy task w tle - pobiera kursy co 10 sekund"""
    await asyncio.sleep(5)  # Poczekaj 5 sekund na start
    
    while True:
        try:
            if client_service.is_authenticated():
                rates = await client_service.get_all_currency_rates()
                print(f"📊 Pobrano kursy: {len(rates)} walut")
                for rate in rates:
                    print(f"  {rate['symbol']}: ${rate['rate']:.2f}")
        except Exception as e:
            print(f"❌ Błąd pobierania kursów: {e}")
        
        await asyncio.sleep(10)  # Czekaj 10 sekund
