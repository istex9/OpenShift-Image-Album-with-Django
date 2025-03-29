#!/bin/bash

echo " Applying Django migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo " Starting Django app..."
exec python manage.py runserver 0.0.0.0:8080
