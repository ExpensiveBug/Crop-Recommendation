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

python3 manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.getenv('ADMIN_USERNAME')
password = os.getenv('ADMIN_PASSWORD')
if username and password:
    u, created = User.objects.get_or_create(username=username)
    u.set_password(password) 
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print(f'Superuser {username} updated/created successfully!')
"

echo "===> Build Completed!"
