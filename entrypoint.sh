#!/bin/bash


mkdir -p /opt/app-root/src/media/photos


echo " Applying Django migrations ...."
python manage.py migrate --noinput

echo " Starting Django app..."
exec python manage.py runserver 0.0.0.0:8080
