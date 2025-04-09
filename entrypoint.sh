#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
    sleep 1
done
echo "PostgreSQL is up!"

# Check if migrations have been applied by looking for a flag file
FLAG_FILE="/app/.migrations_applied"

if [ ! -f "$FLAG_FILE" ]; then
    echo "Applying database migrations..."
    poetry run python manage.py migrate

    # Load initial data only if it hasn't been loaded
    echo "Loading initial data..."
    poetry run python manage.py runscript import_data

    # Create flag file to mark initialization complete
    touch "$FLAG_FILE"
    echo "Initial data loaded successfully"
else
    echo "Migrations already applied, skipping initialization"
fi

# Start the server
echo "Starting Django server..."
exec poetry run python manage.py runserver 0.0.0.0:8000
