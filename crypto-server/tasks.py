import asyncio
import random
from sqlalchemy.future import select
from .database import AsyncSessionLocal
from .models import CurrencyRate

async def currency_generator():
    async with AsyncSessionLocal() as db:
        print("🌱 Sprawdzanie i seedowanie walut...")

        initial_currencies = [
            {"symbol": "BTC", "rate": 45000.0},
            {"symbol": "ETH", "rate": 3200.0},
            {"symbol": "SOL", "rate": 144.0},
            {"symbol": "XRP", "rate": 0.55},
            {"symbol": "ADA", "rate": 0.50},
            {"symbol": "DOT", "rate": 7.20},
            {"symbol": "LINK", "rate": 14.50},
            {"symbol": "LTC", "rate": 70.00},
            {"symbol": "BCH", "rate": 250.00},
            {"symbol": "XLM", "rate": 0.12},
            {"symbol": "UNI", "rate": 6.50},
            {"symbol": "DOGE", "rate": 0.08},
            {"symbol": "AVAX", "rate": 35.00},
        ]

        new_currencies = []
        for curr_data in initial_currencies:
            result = await db.execute(select(CurrencyRate).where(CurrencyRate.symbol == curr_data["symbol"]))
            if not result.scalars().first():
                print(f"   ➕ Dodawanie nowej waluty: {curr_data['symbol']}")
                new_currencies.append(
                    CurrencyRate(
                        symbol=curr_data["symbol"],
                        rate=curr_data["rate"],
                        open_price=curr_data["rate"],
                        change_24h=0.0
                    )
                )

        if new_currencies:
            db.add_all(new_currencies)
            await db.commit()
            print(f"✅ Dodano {len(new_currencies)} nowych walut.")

        print("🚀 Start generatora kursów (Persistent DB Mode)!")

        while True:
            result = await db.execute(select(CurrencyRate))
            rates = result.scalars().all()

            for currency in rates:
                if currency.open_price is None:
                    currency.open_price = currency.rate

                change_percent = random.uniform(-0.005, 0.005)
                currency.rate = currency.rate * (1 + change_percent)

                if currency.open_price > 0:
                    currency.change_24h = ((currency.rate - currency.open_price) / currency.open_price) * 100

            await db.commit()

            await asyncio.sleep(3)
