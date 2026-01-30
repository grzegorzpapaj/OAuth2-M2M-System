from fastapi import FastAPI
import asyncio
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import engine, Base

from .auth import router as auth_router
from .currency import router as currency_router
from .tasks import currency_generator

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tabele gotowe!")

    asyncio.create_task(currency_generator())

app.include_router(auth_router, prefix="/api")
app.include_router(currency_router, prefix="/api")

app.mount("/static", StaticFiles(directory="crypto-server/static"), name="static")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "crypto-server"}

@app.get("/")
async def root():
    return FileResponse("crypto-server/static/index.html")
