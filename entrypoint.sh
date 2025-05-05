#!/bin/bash

python manage.py collectstatic --noinput
cp -r /static_source/. /static/
python manage.py migrate
make create_admin
gunicorn mansions_of_madness.wsgi -b 0.0.0.0:8080