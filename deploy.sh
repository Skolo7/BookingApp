#!/bin/bash

set -e

echo "Starting deployment..."

if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    exit 1
fi

echo "Building new Docker images..."
docker-compose -f docker-compose.prod.yml --env-file .env build --no-cache

echo "Performing rolling update..."
docker-compose -f docker-compose.prod.yml --env-file .env up -d --force-recreate --remove-orphans

echo "⏳ Waiting for services to be healthy..."
sleep 15

echo "Collecting static files..."
docker-compose -f docker-compose.prod.yml --env-file .env exec -T web python src/manage.py collectstatic --noinput

echo "Cleaning up old images..."
docker image prune -f

echo "completed!"
