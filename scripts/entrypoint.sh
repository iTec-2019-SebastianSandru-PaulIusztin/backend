#!/usr/bin/env bash

DB_HOST=${SERVICING_DB_HOST:-localhost}
DB_PORT=${SERVICING_DB_PORT:-5432}

echo "$DB_HOST:$DB_PORT"

bash "$(dirname "${BASH_SOURCE[0]}")"/wait-for-it.sh "$DB_HOST:$DB_PORT" "--" "echo" "Database connection is available" && \
python manage.py runserver 0.0.0.0:80
python manage.py migrate
