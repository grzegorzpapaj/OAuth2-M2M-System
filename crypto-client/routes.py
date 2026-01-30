"""
Endpointy FastAPI dla crypto-client
"""
from fastapi import APIRouter, HTTPException, Cookie, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(tags=["Client Operations"])


class ClientCredentials(BaseModel):
    """Model do ustawienia credentials"""
    client_id: str
    client_secret: str
    app_name: Optional[str] = "Crypto Client App"
    admin_secret: Optional[str] = None


class TokenRequest(BaseModel):
    """Model do żądania tokenu"""
    client_id: str
    client_secret: str


class CurrencyRateResponse(BaseModel):
    """Model odpowiedzi z kursem waluty"""
    symbol: str
    rate: float
    name: str
    change_24h: float
    updated_at: datetime


# Będzie zaimportowany w main.py
_client_service = None


def set_client_service(service):
    """Ustaw globalny client service"""
    global _client_service
    _client_service = service


# Dependency for user authentication
async def get_current_user(session_token: Optional[str] = Cookie(None)):
    """Dependency to verify user session"""
    from .database import db
    
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated - please login first")
    
    user = db.verify_session(session_token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session - please login again")
    
    return user


@router.post("/register")
async def register():
    """
    Zarejestruj klienta w crypto-server
    """
    try:
        result = await _client_service.register_client()
        return {
            "status": "success",
            "data": result,
            "client_id": _client_service.client_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/token")
async def get_token(request: TokenRequest):
    """
    Uzyskaj access token od crypto-server (OAuth2 token endpoint)
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Próba uzyskania tokenu dla client_id: {request.client_id}")
        
        # Zaktualizuj credentials w globalnym client service
        _client_service.client_id = request.client_id
        _client_service.client_secret = request.client_secret
        
        # Uzyskaj token od crypto-server
        token = await _client_service.get_access_token()
        
        logger.info(f"Token uzyskany pomyślnie, długość: {len(token)}")
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 7200
        }
    except Exception as e:
        logger.error(f"Błąd podczas uzyskiwania tokenu: {type(e).__name__}: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=401, detail=f"Błąd uwierzytelniania: {str(e)}")


@router.post("/configure")
async def configure_credentials(credentials: ClientCredentials):
    """
    Skonfiguruj credentials klienta (client_id, client_secret)
    """
    _client_service.client_id = credentials.client_id
    _client_service.client_secret = credentials.client_secret
    _client_service.app_name = credentials.app_name
    if credentials.admin_secret:
        _client_service.admin_secret = credentials.admin_secret
    
    # Reset tokenu
    _client_service.access_token = None
    _client_service.token_expires_at = None
    
    return {
        "status": "success",
        "message": "Credentials zaktualizowane",
        "client_id": _client_service.client_id
    }


@router.get("/status")
async def get_status():
    """
    Sprawdź status uwierzytelnienia klienta
    """
    return {
        "authenticated": _client_service.is_authenticated(),
        "client_id": _client_service.client_id,
        "server_url": _client_service.server_url,
        "token_expires_at": _client_service.token_expires_at.isoformat() if _client_service.token_expires_at else None,
        "has_token": _client_service.access_token is not None
    }


@router.get("/currencies", response_model=List[CurrencyRateResponse])
async def get_all_currencies(user: dict = Depends(get_current_user)):
    """
    Pobierz wszystkie kursy walut z crypto-server
    Wymaga uwierzytelnienia użytkownika
    """
    try:
        # Use user's client credentials for M2M OAuth2
        if user.get("client_id") and user.get("client_secret"):
            _client_service.client_id = user["client_id"]
            _client_service.client_secret = user["client_secret"]
        
        rates = await _client_service.get_all_currency_rates()
        return rates
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Błąd pobierania kursów: {str(e)}"
        )


@router.get("/currencies/{symbol}", response_model=CurrencyRateResponse)
async def get_currency(symbol: str, user: dict = Depends(get_current_user)):
    """
    Pobierz kurs konkretnej waluty z crypto-server
    Wymaga uwierzytelnienia użytkownika
    """
    try:
        # Use user's client credentials for M2M OAuth2
        if user.get("client_id") and user.get("client_secret"):
            _client_service.client_id = user["client_id"]
            _client_service.client_secret = user["client_secret"]
        
        rate = await _client_service.get_currency_rate(symbol)
        return rate
    except Exception as e:
        if "404" in str(e):
            raise HTTPException(status_code=404, detail=f"Waluta {symbol} nie została znaleziona")
        raise HTTPException(
            status_code=500, 
            detail=f"Błąd pobierania kursu: {str(e)}"
        )


@router.get("/test-server")
async def test_server_connection():
    """
    Testuj połączenie z crypto-server (nie wymaga uwierzytelnienia)
    """
    try:
        result = await _client_service.test_connection()
        return {
            "status": "success",
            "server_response": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Nie można połączyć się z serwerem: {str(e)}"
        )
