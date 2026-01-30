from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import os

from .database import get_db
from .models import ClientApp

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

SECRET_KEY = "secret-key-to-sign-tokens"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

ADMIN_SECRET = os.getenv("ADMIN_SECRET", "super-secret-admin-key")

class ClientCreate(BaseModel):
    client_id: str
    client_secret: str
    app_name: str

class TokenRequest(BaseModel):
    client_id: str
    client_secret: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_admin_secret(x_admin_secret: str = Header(...)):
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Nieprawidłowy klucz administratora")

@router.post("/register", dependencies=[Depends(verify_admin_secret)])
async def register_client(client_data: ClientCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ClientApp).where(ClientApp.client_id == client_data.client_id))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Taki Client ID już istnieje")

    new_client = ClientApp(
        client_id=client_data.client_id,
        client_secret=client_data.client_secret,
        app_name=client_data.app_name
    )
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return {"message": "Klient zarejestrowany", "id": new_client.id}

@router.post("/token")
async def login_for_access_token(token_data: TokenRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ClientApp).where(ClientApp.client_id == token_data.client_id))
    client = result.scalars().first()

    if not client or client.client_secret != token_data.client_secret:
        raise HTTPException(status_code=401, detail="Nieprawidłowe dane")

    access_token = create_access_token(data={"sub": client.client_id})
    return {"access_token": access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

async def get_current_client(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token jest nieważny lub wygasł",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        client_id: str = payload.get("sub")
        if client_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(ClientApp).where(ClientApp.client_id == client_id))
    client = result.scalars().first()

    if client is None:
        raise credentials_exception

    return client
