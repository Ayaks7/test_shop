#!/bin/bash

echo "Apply migrations and creation products "
yoyo apply --database postgres://postgres@db/postgres catalog/migrations

echo "Starting server"
uvicorn catalog:app --reload --host 0.0.0.0 --port 8002
