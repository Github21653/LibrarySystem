#!/usr/bin/env bash

#exit on error
set -o errexit

pip install -r requirements.txt

#Convert static assest files
python manage.py collectstatic --noinput

#Apply database migrations
python manage.py migrate