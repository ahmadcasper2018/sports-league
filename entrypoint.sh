#!/bin/sh

/usr/bin/wait-for.sh db:5432 -t 30 -- echo "PostgreSQL started"

# Migrate
python manage.py makemigrations
python manage.py migrate

exec "$@"