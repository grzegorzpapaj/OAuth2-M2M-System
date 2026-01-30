"""
Crypto Client - OAuth2 Client Credentials Grant
Komunikuje się z crypto-server używając OAuth2
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .client_service import ClientService
from .routes import router as client_router, set_client_service
from .user_routes import router as user_router
from .database import db
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

# Dodaj router z endpointami
app.include_router(client_router, prefix="/api")
app.include_router(user_router, prefix="/api")  # User authentication routes

@app.on_event("startup")
async def startup():
    """Inicjalizacja klienta przy starcie"""
    print("🚀 Uruchamianie Crypto Client...")
    
    # Initialize database
    print("📊 Initializing user database...")
    db.init_db()
    db.cleanup_expired_sessions()
    
    # Próba zalogowania przy starcie
    try:
        await client_service.ensure_authenticated()
        print("✅ Klient uwierzytelniony i gotowy!")
    except Exception as e:
        print(f"⚠️  Nie udało się uwierzytelnić przy starcie: {e}")
        print("💡 Użytkownicy muszą się zalogować przez frontend")
    
    # Opcjonalnie: uruchom task pobierający kursy w tle
    asyncio.create_task(background_currency_fetcher())

@app.on_event("shutdown")
async def shutdown():
    """Czyszczenie zasobów przy wyłączeniu"""
    await client_service.close()
    print("👋 Crypto Client zatrzymany")

@app.get("/")
async def root():
    """Serwuj nowy frontend HTML z user authentication"""
    return FileResponse(os.path.join(static_dir, "dashboard.html"))

@app.get("/admin")
async def admin():
    """Serwuj admin dashboard dla M2M configuration"""
    return FileResponse(os.path.join(static_dir, "admin.html"))

@app.get("/register")
async def register_page():
    """Serwuj stronę rejestracji"""
    return FileResponse(os.path.join(static_dir, "register.html"))

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
