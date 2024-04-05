#!/bin/bash
echo "Creating Migrations..."
python manage.py makemigrations api
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Loading Base Data..."
python manage.py loaddata fixtures/test_data.json

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000
