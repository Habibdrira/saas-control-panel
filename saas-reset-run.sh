#!/bin/bash
set -e

echo "==============================="
echo "  SaaS Platform Reset & Run"
echo "==============================="

echo "[1/6] Stopping docker-compose..."
docker compose down || true

echo "[2/6] Removing all containers..."
docker ps -aq | xargs -r docker rm -f

echo "[3/6] Removing all images..."
docker images -aq | xargs -r docker rmi -f

echo "[4/6] Cleaning volumes & networks..."
docker system prune -a -f --volumes

echo "[5/6] Building user-app image..."
cd user-app
docker build -t user-app .
cd ..

echo "[6/6] Starting SaaS platform..."
docker compose up --build

echo "==============================="
echo "  SaaS Platform is running 🚀"
echo "==============================="
