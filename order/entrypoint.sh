#!/bin/bash


echo "Apply migrations for orders"
python manage.py migrate

echo "Starting server"
python manage.py runserver 0.0.0.0:8001