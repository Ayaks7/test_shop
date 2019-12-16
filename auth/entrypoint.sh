#!/bin/bash

echo "Apply migrations and creation base users"
yoyo apply --database postgres://postgres@db/postgres auth/migrations

echo "Starting auth server"
uvicorn auth:app --reload --host 0.0.0.0
