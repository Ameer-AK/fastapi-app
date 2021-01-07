#!/usr/bin/env bash

cd src

echo "MIGRATING DATABASE..."

alembic upgrade head

echo "SEEDING DATABASE..."

python seed/seeddb.py

echo "STARING UVICORN SERVER..."

uvicorn main:app --host 0.0.0.0 --reload
