#!/usr/bin/env bash

set -e

/wait-for-it.sh $SQL_HOST:$SQL_PORT --timeout=10 --strict -- echo "postgres is up"

celery -A config worker
