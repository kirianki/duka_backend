#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Wait for database to be ready
echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST ${POSTGRES_PORT:-5432}; do
  sleep 0.1
done

echo "PostgreSQL started"

# Run migrations if requested
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Running migrations..."
    python manage.py migrate --noinput

    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Execute the command passed as arguments to the script
echo "Starting server..."
exec "$@"
