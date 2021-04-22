#!/bin/bash

host="db"
shift

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
  
>&2 echo "Postgres is up - executing command"

echo Running Migrations
python manage.py migrate

echo Running Tests
python manage.py test

echo Seeding Data
python manage.py runscript create_parking_rates

echo Running server
python manage.py runserver 0.0.0.0:8000


