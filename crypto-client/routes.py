"""
Endpointy FastAPI dla crypto-client
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

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


# Będzie zaimportowany w main.py
_client_service = None


def set_client_service(service):
    """Ustaw globalny client service"""
    global _client_service
    _client_service = service


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
    try:
        # Zaktualizuj credentials w globalnym client service
        _client_service.client_id = request.client_id
        _client_service.client_secret = request.client_secret
        
        # Uzyskaj token od crypto-server
        token = await _client_service.get_access_token()
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 7200
        }
    except Exception as e:
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
async def get_all_currencies():
    """
    Pobierz wszystkie kursy walut z crypto-server
    Wymaga uwierzytelnienia
    """
    try:
        rates = await _client_service.get_all_currency_rates()
        return rates
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Błąd pobierania kursów: {str(e)}"
        )


@router.get("/currencies/{symbol}", response_model=CurrencyRateResponse)
async def get_currency(symbol: str):
    """
    Pobierz kurs konkretnej waluty z crypto-server
    Wymaga uwierzytelnienia
    """
    try:
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
