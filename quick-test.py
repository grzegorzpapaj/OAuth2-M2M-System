#!/usr/bin/env python3
"""
Quick test script - sprawdza czy cały system działa
"""
import asyncio
import httpx
import time

SERVER_URL = "http://localhost:8000"
CLIENT_URL = "http://localhost:8001"

async def check_server():
    """Sprawdź czy serwer działa"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{SERVER_URL}/")
            return response.status_code == 200
    except:
        return False

async def check_client():
    """Sprawdź czy klient działa"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{CLIENT_URL}/")
            return response.status_code == 200
    except:
        return False

async def test_oauth_flow():
    """Testuj pełny flow OAuth2"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("\n" + "="*60)
        print("🔐 Test OAuth2 Client Credentials Flow")
        print("="*60)
        
        # 1. Rejestracja
        print("\n1️⃣  Rejestracja klienta...")
        try:
            reg_response = await client.post(
                f"{CLIENT_URL}/api/register"
            )
            print(f"   ✅ Status: {reg_response.status_code}")
            print(f"   📄 Odpowiedź: {reg_response.json()}")
        except Exception as e:
            print(f"   ❌ Błąd: {e}")
            return False
        
        # 2. Login (uzyskanie tokenu)
        print("\n2️⃣  Logowanie (uzyskanie tokenu)...")
        try:
            login_response = await client.post(
                f"{CLIENT_URL}/api/login"
            )
            print(f"   ✅ Status: {login_response.status_code}")
            data = login_response.json()
            print(f"   🔑 Token: {data.get('token_preview', 'N/A')}")
            print(f"   ⏰ Wygasa: {data.get('expires_at', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Błąd: {e}")
            return False
        
        # 3. Sprawdź status
        print("\n3️⃣  Sprawdzanie statusu...")
        try:
            status_response = await client.get(
                f"{CLIENT_URL}/api/status"
            )
            status = status_response.json()
            print(f"   ✅ Uwierzytelniony: {status['authenticated']}")
            print(f"   🆔 Client ID: {status['client_id']}")
        except Exception as e:
            print(f"   ❌ Błąd: {e}")
            return False
        
        # 4. Pobierz kursy walut
        print("\n4️⃣  Pobieranie kursów walut...")
        try:
            currencies_response = await client.get(
                f"{CLIENT_URL}/api/currencies"
            )
            currencies = currencies_response.json()
            print(f"   ✅ Pobrano {len(currencies)} walut:")
            for curr in currencies:
                print(f"      💰 {curr['symbol']:>5} = ${curr['rate']:>12,.2f}")
        except Exception as e:
            print(f"   ❌ Błąd: {e}")
            return False
        
        # 5. Pobierz konkretną walutę
        print("\n5️⃣  Pobieranie kursu BTC...")
        try:
            btc_response = await client.get(
                f"{CLIENT_URL}/api/currencies/BTC"
            )
            btc = btc_response.json()
            print(f"   ✅ BTC: ${btc['rate']:,.2f}")
        except Exception as e:
            print(f"   ❌ Błąd: {e}")
            return False
        
        print("\n" + "="*60)
        print("✅ Wszystkie testy przeszły pomyślnie!")
        print("="*60)
        return True

async def main():
    print("🧪 Quick System Test")
    print("="*60)
    
    # Sprawdź czy serwer działa
    print("\n🔍 Sprawdzanie serwera (localhost:8000)...")
    server_ok = await check_server()
    if server_ok:
        print("   ✅ Serwer działa")
    else:
        print("   ❌ Serwer nie odpowiada!")
        print("   💡 Uruchom serwer: ./run-server.sh")
        return
    
    # Sprawdź czy klient działa
    print("\n🔍 Sprawdzanie klienta (localhost:8001)...")
    client_ok = await check_client()
    if client_ok:
        print("   ✅ Klient działa")
    else:
        print("   ❌ Klient nie odpowiada!")
        print("   💡 Uruchom klienta: ./run-client.sh")
        return
    
    # Uruchom testy OAuth
    await test_oauth_flow()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 OAuth2 M2M System - Quick Test")
    print("="*60)
    print("\nUpewnij się że działają:")
    print("  1. PostgreSQL (docker-compose up -d)")
    print("  2. Crypto-Server (./run-server.sh)")
    print("  3. Crypto-Client (./run-client.sh)")
    print("\nRozpoczynanie testów za 2 sekundy...\n")
    
    time.sleep(2)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Test przerwany przez użytkownika")
    except Exception as e:
        print(f"\n\n❌ Nieoczekiwany błąd: {e}")
        import traceback
        traceback.print_exc()
