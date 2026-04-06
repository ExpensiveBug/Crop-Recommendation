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
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, 'admin@example.com', password)
        print(f'Superuser {username} created successfully!')
    else:
        print(f'Superuser {username} already exists.')
else:
    print('Admin credentials not found in environment variables.')
"

echo "===> Build Completed!"
