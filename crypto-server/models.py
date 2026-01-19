from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from .database import Base


class ClientApp(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, index=True, nullable=False)
    # hash the passwords
    client_secret = Column(String, nullable=False)
    app_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CurrencyRate(Base):
    __tablename__ = "currency_rates_live"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)  # np. BTC, ETH
    rate = Column(Float, nullable=False)  # Aktualny kurs
    open_price = Column(Float, nullable=True) # Cena otwarcia (baza do wyliczeń)
    change_24h = Column(Float, default=0.0)   # Zmiana procentowa
    last_updated = Column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )
