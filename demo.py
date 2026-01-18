#!/usr/bin/env python3
"""
Demo script - pokazuje różne scenariusze użycia systemu
"""
import asyncio
import sys
sys.path.insert(0, '/home/pi/studia/OAuth2-M2M-System')

from crypto_client.client_service import ClientService


async def demo_basic_usage():
    """Podstawowe użycie - rejestracja, login, pobieranie danych"""
    print("\n" + "="*70)
    print("📚 DEMO 1: Podstawowe użycie")
    print("="*70)
    
    client = ClientService(
        server_url="http://localhost:8000",
        client_id="demo-client-basic",
        client_secret="demo-secret-123"
    )
    
    try:
        # Rejestracja i logowanie
        await client.register_client()
        await client.get_access_token()
        print(f"✅ Zalogowano jako: {client.client_id}")
        
        # Pobierz wszystkie kursy
        rates = await client.get_all_currency_rates()
        print(f"\n💰 Kursy {len(rates)} kryptowalut:")
        for rate in rates:
            print(f"   {rate['symbol']:>5}: ${rate['rate']:>12,.2f}")
            
    finally:
        await client.close()


async def demo_auto_refresh():
    """Demonstracja automatycznego odświeżania tokenu"""
    print("\n" + "="*70)
    print("🔄 DEMO 2: Automatyczne odświeżanie tokenu")
    print("="*70)
    
    client = ClientService(
        server_url="http://localhost:8000",
        client_id="demo-client-refresh",
        client_secret="refresh-secret-456"
    )
    
    try:
        await client.register_client()
        await client.get_access_token()
        print("✅ Token uzyskany")
        
        # Pobierz dane
        btc1 = await client.get_currency_rate("BTC")
        print(f"📊 BTC (przed): ${btc1['rate']:,.2f}")
        
        # Symuluj wygaśnięcie tokenu
        print("\n⚠️  Symulacja wygaśnięcia tokenu...")
        client.access_token = None
        
        # ensure_authenticated automatycznie odświeży token
        btc2 = await client.get_currency_rate("BTC")
        print(f"📊 BTC (po auto-refresh): ${btc2['rate']:,.2f}")
        print("✅ Token automatycznie odświeżony!")
        
    finally:
        await client.close()


async def demo_error_handling():
    """Demonstracja obsługi błędów"""
    print("\n" + "="*70)
    print("🛡️  DEMO 3: Obsługa błędów")
    print("="*70)
    
    client = ClientService(
        server_url="http://localhost:8000",
        client_id="demo-client-errors",
        client_secret="error-secret-789"
    )
    
    try:
        await client.register_client()
        await client.get_access_token()
        
        # Test 1: Nieistniejąca waluta
        print("\n1️⃣  Próba pobrania nieistniejącej waluty...")
        try:
            await client.get_currency_rate("NIEISTNIEJE")
        except Exception as e:
            print(f"   ❌ Złapano błąd: {e}")
        
        # Test 2: Nieprawidłowy token
        print("\n2️⃣  Próba użycia nieprawidłowego tokenu...")
        old_token = client.access_token
        client.access_token = "nieprawidlowy-token"
        try:
            await client.get_all_currency_rates()
        except Exception as e:
            print(f"   ❌ Złapano błąd: {type(e).__name__}")
            client.access_token = old_token
        
        print("\n✅ Obsługa błędów działa poprawnie!")
        
    finally:
        await client.close()


async def demo_multiple_clients():
    """Demonstracja wielu klientów równocześnie"""
    print("\n" + "="*70)
    print("👥 DEMO 4: Wiele klientów równocześnie")
    print("="*70)
    
    # Utwórz 3 klientów
    clients = [
        ClientService(
            server_url="http://localhost:8000",
            client_id=f"multi-client-{i}",
            client_secret=f"secret-{i}",
            app_name=f"App {i}"
        )
        for i in range(1, 4)
    ]
    
    try:
        # Zarejestruj wszystkich
        print("\n📝 Rejestracja klientów...")
        for i, client in enumerate(clients, 1):
            await client.register_client()
            await client.get_access_token()
            print(f"   ✅ Klient {i} zarejestrowany")
        
        # Pobierz dane równocześnie
        print("\n📊 Pobieranie danych równocześnie...")
        tasks = [client.get_currency_rate("ETH") for client in clients]
        results = await asyncio.gather(*tasks)
        
        for i, result in enumerate(results, 1):
            print(f"   Klient {i}: ETH = ${result['rate']:,.2f}")
        
        print("\n✅ Wszyscy klienci działają poprawnie!")
        
    finally:
        for client in clients:
            await client.close()


async def demo_continuous_monitoring():
    """Demonstracja ciągłego monitorowania (10 sekund)"""
    print("\n" + "="*70)
    print("📡 DEMO 5: Ciągłe monitorowanie kursów (10 sekund)")
    print("="*70)
    
    client = ClientService(
        server_url="http://localhost:8000",
        client_id="demo-client-monitor",
        client_secret="monitor-secret"
    )
    
    try:
        await client.register_client()
        await client.get_access_token()
        
        print("\n⏱️  Monitorowanie rozpoczęte... (Ctrl+C aby przerwać)")
        
        for i in range(10):
            rates = await client.get_all_currency_rates()
            print(f"\n[{i+1}/10] Kursy:")
            for rate in rates:
                print(f"   {rate['symbol']:>5}: ${rate['rate']:>12,.2f}")
            
            if i < 9:  # Nie czekaj po ostatnim
                await asyncio.sleep(1)
        
        print("\n✅ Monitorowanie zakończone!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Monitorowanie przerwane przez użytkownika")
    finally:
        await client.close()


async def main():
    """Uruchom wszystkie dema"""
    print("\n" + "="*70)
    print("🎬 OAuth2 M2M System - Interactive Demo")
    print("="*70)
    print("\nTen skrypt demonstruje różne scenariusze użycia systemu.")
    print("Upewnij się, że serwer i klient działają!\n")
    
    demos = [
        ("Podstawowe użycie", demo_basic_usage),
        ("Auto-refresh tokenu", demo_auto_refresh),
        ("Obsługa błędów", demo_error_handling),
        ("Wiele klientów", demo_multiple_clients),
        ("Ciągłe monitorowanie", demo_continuous_monitoring),
    ]
    
    print("Dostępne dema:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print("  0. Wszystkie")
    print("  q. Wyjście")
    
    choice = input("\nWybierz demo (0-5, q): ").strip()
    
    if choice == 'q':
        print("👋 Do zobaczenia!")
        return
    
    try:
        if choice == '0':
            # Uruchom wszystkie
            for name, demo_func in demos:
                await demo_func()
                await asyncio.sleep(2)
        else:
            idx = int(choice) - 1
            if 0 <= idx < len(demos):
                await demos[idx][1]()
            else:
                print("❌ Nieprawidłowy wybór!")
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo przerwane")
    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Do zobaczenia!")
