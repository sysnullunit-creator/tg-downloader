#!/usr/bin/env bash
set -e

# Continuous Deployment script for Raspberry Pi / VPS host
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "==> [CD] Pulling latest changes from origin/main..."
git fetch origin main
git reset --hard origin/main

echo "==> [CD] Ensuring secure permissions for .env..."
if [ -f .env ]; then
    chmod 600 .env
fi

echo "==> [CD] Building and restarting Docker containers..."
docker compose build --pull
docker compose up -d --remove-orphans

echo "==> [CD] Cleaning up dangling images..."
docker image prune -f

echo "==> [CD] Deployment completed successfully!"
docker compose ps

