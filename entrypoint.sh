#! /bin/bash

python manage.py makemigrations --noinput

python manage.py migrate --noinput

python manage.py collectstatic --noinput
export DJANGO_SETTINGS_MODULE=config.settings

exec gunicorn config.wsgi:application -b 0.0.0.0 --reload
