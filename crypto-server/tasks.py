import asyncio
import random
from sqlalchemy.future import select
from .database import AsyncSessionLocal
from .models import CurrencyRate

async def currency_generator():
    async with AsyncSessionLocal() as db:
        # 1. SEEDOWANIE: Sprawdź czy mamy jakieś waluty
        # Uwaga: przy zmianie nazwy tabeli, tabela będzie pusta na starcie
        result = await db.execute(select(CurrencyRate))
        if not result.scalars().first():
            print("🌱 Inicjalizacja walut startowych (Nowa tabela)...")
            db.add_all([
                CurrencyRate(symbol="BTC", rate=45000.0, open_price=45000.0, change_24h=0.0),
                CurrencyRate(symbol="ETH", rate=3200.0, open_price=3200.0, change_24h=0.0),
                CurrencyRate(symbol="SOL", rate=144.0, open_price=144.0, change_24h=0.0),
            ])
            await db.commit()
        
        print("🚀 Start generatora kursów (Persistent DB Mode)!")

        # 2. PĘTLA NIESKOŃCZONA (Symulacja rynku)
        while True:
            # Pobierz wszystkie waluty
            result = await db.execute(select(CurrencyRate))
            rates = result.scalars().all()

            # Zmień kurs każdej waluty
            for currency in rates:
                # Jeśli z jakiegoś powodu open_price jest null (np. stare dane), napraw to
                if currency.open_price is None:
                    currency.open_price = currency.rate

                # Zmiana ceny
                change_percent = random.uniform(-0.005, 0.005) 
                currency.rate = currency.rate * (1 + change_percent)
                
                # Oblicz i zapisz zmianę 24h w bazie
                if currency.open_price > 0:
                    currency.change_24h = ((currency.rate - currency.open_price) / currency.open_price) * 100
            
            # Zapisz wszystkie zmiany w bazie
            await db.commit()
            
            # Czekaj 3 sekundy
            await asyncio.sleep(3)