"""
Konfiguracja dla crypto-client
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Ustawienia aplikacji"""
    
    # Adres crypto-server
    SERVER_URL: str = "http://localhost:8000"
    
    # Credentials OAuth2
    CLIENT_ID: str = "crypto-client-001"
    CLIENT_SECRET: str = "super-secret-key-123"
    APP_NAME: str = "Crypto Client App"
    
    # Port na którym działa client
    CLIENT_PORT: int = 8001
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
