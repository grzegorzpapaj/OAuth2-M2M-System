#!/usr/bin/env python3
"""
Create user script - to be run inside Docker container
"""
import sys
sys.path.insert(0, '/app')

from database import db

print('=' * 60)
print('🔐 CRYPTO CLIENT - User Creation Tool (Docker)')
print('=' * 60)
print()

username = input('📝 Username: ').strip()
if not username:
    print('❌ Username cannot be empty!')
    sys.exit(1)

password = input('🔑 Password: ').strip()
if not password:
    print('❌ Password cannot be empty!')
    sys.exit(1)

email = input('📧 Email (optional): ').strip() or None

print()
print('📋 Client Credentials (optional - can be added later)')
client_id = input('   Client ID (optional): ').strip() or None
client_secret = input('   Client Secret (optional): ').strip() or None

is_admin_input = input('👑 Is admin? (y/n): ').lower()
is_admin = is_admin_input.startswith('y')

print()
print('Creating user...')

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
    print('=' * 60)
    print('✅ USER CREATED SUCCESSFULLY!')
    print('=' * 60)
    print(f'👤 Username: {user["username"]}')
    print(f'🆔 User ID: {user["id"]}')
    print(f'📧 Email: {user["email"] or "Not provided"}')
    print(f'👑 Admin: {"Yes" if user["is_admin"] else "No"}')
    if client_id:
        print(f'🔐 Client ID: {client_id}')
    print()
    print('🎉 User can now login at: http://localhost:8001')
    print('=' * 60)
    
except ValueError as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Unexpected error: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
