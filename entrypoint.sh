#!/bin/bash

set -e

echo "🔍 DATABASE_HOST=$DATABASE_HOST"
echo "🔍 DATABASE_PORT=$DATABASE_PORT"

echo "🔁 Waiting for PostgreSQL at $DATABASE_HOST:$DATABASE_PORT..."

RETRIES=20
until nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  echo "⏳ PostgreSQL not available yet – sleeping..."
  RETRIES=$((RETRIES-1))
  if [ $RETRIES -le 0 ]; then
    echo "❌ Could not connect to PostgreSQL – exiting."
    exit 1
  fi
  sleep 2
done

echo "✅ PostgreSQL is available."

echo "📦 Running migrations..."
python manage.py migrate --noinput

echo "👤 Ensuring superuser exists..."
python manage.py shell << END
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if username and email and password:
    if not User.objects.filter(username=username).exists():
        print("🧑‍🚀 Creating superuser...")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print("✅ Superuser already exists.")
else:
    print("⚠️ Missing superuser environment variables; skipping creation.")
END

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn..."
exec gunicorn portfolio_cum_blog.wsgi:application --bind 0.0.0.0:8080
