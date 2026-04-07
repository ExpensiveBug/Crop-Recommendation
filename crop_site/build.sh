#!/bin/bash
set -e

echo "===> Installing Requirements..."

pip install -r requirements.txt --break-system-packages

echo "===> Running Migrations..."

python3 manage.py migrate --noinput

echo "===> Collecting Static Files..."

python3 manage.py collectstatic --noinput

echo "===> Build Completed!"
