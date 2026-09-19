#!/usr/bin/env bash
set -e

echo "=== STARTING DJANGO APPLICATION ==="

# Navigate to backend directory if at project root
if [ -d "backend" ]; then
    echo "Found backend directory, changing directory..."
    cd backend
fi

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Applying database migrations..."
python manage.py migrate --no-input

PORT="${PORT:-8000}"
echo "Starting Gunicorn on 0.0.0.0:$PORT..."
exec gunicorn config.wsgi:application --bind "0.0.0.0:$PORT" --workers 2 --timeout 120