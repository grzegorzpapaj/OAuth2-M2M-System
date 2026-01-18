#!/usr/bin/env python3
"""
Skrypt testowy dla crypto-client
Demonstracja OAuth2 Client Credentials Grant
"""
import asyncio
import sys
sys.path.insert(0, '/home/pi/studia/OAuth2-M2M-System')

from crypto_client.client_service import ClientService


async def main():
    print("=" * 60)
    print("🔐 OAuth2 Client Credentials Grant - Test")
    print("=" * 60)
    
    # Utworzenie klienta
    client = ClientService(
        server_url="http://localhost:8000",
        client_id="crypto-client-001",
        client_secret="super-secret-key-123",
        app_name="Test Client App"
    )
    
    try:
        # 1. Test połączenia z serwerem
        print("\n📡 1. Testowanie połączenia z serwerem...")
        server_info = await client.test_connection()
        print(f"   ✅ Serwer odpowiada: {server_info}")
        
        # 2. Rejestracja klienta
        print("\n📝 2. Rejestracja klienta...")
        reg_result = await client.register_client()
        print(f"   ✅ Rejestracja: {reg_result}")
        
        # 3. Uzyskanie tokenu
        print("\n🔑 3. Uzyskiwanie tokenu JWT...")
        token = await client.get_access_token()
        print(f"   ✅ Token uzyskany: {token[:30]}...")
        print(f"   ⏱️  Ważny do: {client.token_expires_at}")
        print(f"   🔐 Uwierzytelniony: {client.is_authenticated()}")
        
        # 4. Pobieranie wszystkich kursów walut
        print("\n💰 4. Pobieranie wszystkich kursów walut...")
        rates = await client.get_all_currency_rates()
        print(f"   ✅ Pobrano {len(rates)} walut:")
        for rate in rates:
            print(f"      {rate['symbol']:>5} = ${rate['rate']:>10,.2f}")
        
        # 5. Pobieranie konkretnej waluty
        print("\n📊 5. Pobieranie kursu BTC...")
        btc_rate = await client.get_currency_rate("BTC")
        print(f"   ✅ BTC: ${btc_rate['rate']:,.2f}")
        
        # 6. Test wygaśnięcia tokenu
        print("\n⏳ 6. Symulacja wygaśnięcia tokenu...")
        client.access_token = None  # Symuluj brak tokenu
        print("   🔄 Token usunięty, ponowne uwierzytelnianie...")
        
        await client.ensure_authenticated()
        print(f"   ✅ Automatycznie uzyskano nowy token!")
        
        # 7. Pobieranie po wygaśnięciu
        print("\n🔄 7. Pobieranie danych po odświeżeniu tokenu...")
        eth_rate = await client.get_currency_rate("ETH")
        print(f"   ✅ ETH: ${eth_rate['rate']:,.2f}")
        
        print("\n" + "=" * 60)
        print("✅ Wszystkie testy zakończone pomyślnie!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await client.close()
        print("\n👋 Połączenie zamknięte")


if __name__ == "__main__":
    print("\n🚀 Uruchamianie testów OAuth2 Client...")
    print("⚠️  Upewnij się, że crypto-server działa na localhost:8000\n")
    
    asyncio.run(main())
