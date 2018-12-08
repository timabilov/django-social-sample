#!/usr/bin/env bash
set -e
python manage.py makemigrations --noinput
python manage.py migrate
python manage.py collectstatic --noinput
uwsgi --http 0.0.0.0:8000 --module socialplatform.wsgi:application --processes 2 --threads 4
