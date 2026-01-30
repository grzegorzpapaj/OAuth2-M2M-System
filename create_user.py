#!/usr/bin/env python3
"""
CLI tool to create users for crypto-client dashboard
Usage: python create_user.py
"""
import sys
import os

# Add crypto-client directory to path
crypto_client_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crypto-client')
sys.path.insert(0, crypto_client_path)

from database import db

def create_user():
    """Interactive user creation"""
    print("=" * 60)
    print("🔐 CRYPTO CLIENT - User Creation Tool")
    print("=" * 60)
    print()
    
    # Get user details
    username = input("📝 Username: ").strip()
    if not username:
        print("❌ Username cannot be empty!")
        return
    
    password = input("🔑 Password: ").strip()
    if not password:
        print("❌ Password cannot be empty!")
        return
    
    email = input("📧 Email (optional): ").strip() or None
    
    print()
    print("📋 Client Credentials (optional - can be added later)")
    client_id = input("   Client ID (optional): ").strip() or None
    client_secret = input("   Client Secret (optional): ").strip() or None
    
    is_admin = input("👑 Is admin? (y/n): ").lower().startswith('y')
    
    print()
    print("Creating user...")
    
    try:
        user = db.create_user(
            username=username,
            password=password,
            email=email,
            client_id=client_id,
            client_secret=client_secret,
            is_admin=is_admin
        )
        
        print()
        print("=" * 60)
        print("✅ USER CREATED SUCCESSFULLY!")
        print("=" * 60)
        print(f"👤 Username: {user['username']}")
        print(f"🆔 User ID: {user['id']}")
        print(f"📧 Email: {user['email'] or 'Not provided'}")
        print(f"👑 Admin: {'Yes' if user['is_admin'] else 'No'}")
        if client_id:
            print(f"🔐 Client ID: {client_id}")
        print()
        print("🎉 User can now login at: http://localhost:8001")
        print("=" * 60)
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        return

if __name__ == "__main__":
    try:
        create_user()
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
