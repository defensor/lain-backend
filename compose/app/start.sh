#! /usr/bin/env sh
set -e

exec gunicorn -k uvicorn.workers.UvicornWorker autoapp:app -b 0.0.0.0:8080
