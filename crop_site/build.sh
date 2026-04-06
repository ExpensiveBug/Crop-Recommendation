#!/bin/bash

# Exit on error
set -e

echo "===> Installing Requirements..."
# Force install using the new flag
pip install -r requirements.txt --break-system-packages

echo "===> Collecting Static Files..."
python3 manage.py collectstatic --noinput

echo "===> Running Migrations..."
python3 manage.py migrate --noinput

echo "===> Build Completed!"
