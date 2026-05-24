#!/bin/bash

# Exit on error
set -e

echo "Starting deployment..."

# Build and restart containers
docker-compose down
docker-compose build
docker-compose up -d

# Run migrations (since RUN_MIGRATIONS=true is set in docker-compose, this might be redundant 
# but good to have explicit if we change the entrypoint logic)
docker-compose exec -T web python manage.py migrate --noinput

# Collect static files
docker-compose exec -T web python manage.py collectstatic --noinput

# Success message
echo "Deployment successful!"
