#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Installing requirements..."
pip install -r requirements.txt

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Running migrations..."
python3 manage.py migrate --noinput

echo "Build finished successfully!"
