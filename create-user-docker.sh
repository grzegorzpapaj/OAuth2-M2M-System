#!/bin/bash
# Create a user in the crypto-client Docker container

echo "🔐 Creating user in crypto-client container..."
echo ""

docker-compose exec -T client python3 /app/crypto-client/_create_user_docker.py
