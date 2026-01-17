from fastapi import FastAPI
from .database import engine, Base

from .auth import router as auth_router 
from .currency import router as currency_router

app = FastAPI()

# --- STARTUP ---
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tabele gotowe!")

app.include_router(auth_router, prefix="/api")
app.include_router(currency_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Server is running nicely!"}