#!/bin/bash

echo "===> Starting Build Process"

# Install requirements
echo "===> Installing Requirements..."
pip install -r requirements.txt || { echo "Pip install failed"; exit 1; }

# Collect Static
echo "===> Collecting Static Files..."
python3 manage.py collectstatic --noinput || { echo "Collectstatic failed"; exit 1; }

# Migrations
echo "===> Running Migrations..."
python3 manage.py migrate --noinput || { echo "Migrations failed"; exit 1; }

echo "===> Build Finished Successfully!"
