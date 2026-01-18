"""
Serwis obsługujący komunikację z crypto-server
Implementuje OAuth2 Client Credentials Grant
"""
import httpx
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from jose import jwt, JWTError


class ClientService:
    """Serwis do komunikacji z crypto-server używając OAuth2"""
    
    def __init__(
        self, 
        server_url: str = "http://localhost:8000",
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        app_name: str = "Crypto Client App",
        admin_secret: Optional[str] = None
    ):
        self.server_url = server_url
        self.client_id = client_id or "crypto-client-001"
        self.client_secret = client_secret or "super-secret-key-123"
        self.app_name = app_name
        self.admin_secret = admin_secret or os.getenv("ADMIN_SECRET", "super-secret-admin-key")
        
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        
        self.http_client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Zamknij połączenia HTTP"""
        await self.http_client.aclose()
    
    def is_authenticated(self) -> bool:
        """Sprawdź czy klient ma ważny token"""
        if not self.access_token:
            return False
        
        if self.token_expires_at and datetime.utcnow() >= self.token_expires_at:
            return False
        
        return True
    
    async def register_client(self) -> Dict:
        """
        Zarejestruj klienta w crypto-server
        Zwraca informację o rejestracji
        """
        url = f"{self.server_url}/api/auth/register"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "app_name": self.app_name
        }
        
        headers = {}
        if self.admin_secret:
            headers["X-Admin-Secret"] = self.admin_secret
        
        response = await self.http_client.post(url, json=data, headers=headers)
        
        if response.status_code == 400:
            # Klient już istnieje
            return {"message": "Klient już zarejestrowany", "existing": True}
        
        response.raise_for_status()
        return response.json()
    
    async def get_access_token(self) -> str:
        """
        Uzyskaj token dostępu od crypto-server
        Implementacja OAuth2 Client Credentials Grant
        """
        url = f"{self.server_url}/api/auth/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        response = await self.http_client.post(url, json=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data["access_token"]
        
        # Dekoduj token aby uzyskać czas wygaśnięcia
        try:
            # Nie weryfikujemy podpisu tutaj, bo to robimy tylko dla czytania exp
            payload = jwt.decode(
                self.access_token, 
                options={"verify_signature": False}
            )
            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                self.token_expires_at = datetime.fromtimestamp(exp_timestamp)
                # Odejmij 1 minutę jako bufor
                self.token_expires_at -= timedelta(minutes=1)
        except JWTError:
            # Jeśli nie możemy zdekodować, ustaw domyślny czas wygaśnięcia
            self.token_expires_at = datetime.utcnow() + timedelta(minutes=119)
        
        return self.access_token
    
    async def ensure_authenticated(self):
        """
        Upewnij się że klient jest uwierzytelniony
        Jeśli token wygasł lub nie istnieje, uzyskaj nowy
        """
        if not self.is_authenticated():
            await self.get_access_token()
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Zwróć nagłówki autoryzacji"""
        if not self.access_token:
            raise ValueError("Brak tokenu dostępu. Najpierw zaloguj się.")
        
        return {"Authorization": f"Bearer {self.access_token}"}
    
    async def get_all_currency_rates(self) -> List[Dict]:
        """
        Pobierz wszystkie kursy walut z crypto-server
        Endpoint: GET /api/currency/
        """
        await self.ensure_authenticated()
        
        url = f"{self.server_url}/api/currency/"
        headers = self._get_auth_headers()
        
        response = await self.http_client.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def get_currency_rate(self, symbol: str) -> Dict:
        """
        Pobierz kurs konkretnej waluty
        Endpoint: GET /api/currency/{symbol}
        """
        await self.ensure_authenticated()
        
        url = f"{self.server_url}/api/currency/{symbol.upper()}"
        headers = self._get_auth_headers()
        
        response = await self.http_client.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def test_connection(self) -> Dict:
        """Testuj połączenie z serwerem"""
        url = f"{self.server_url}/"
        response = await self.http_client.get(url)
        response.raise_for_status()
        return response.json()
