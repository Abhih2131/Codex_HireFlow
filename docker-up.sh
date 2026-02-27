#!/usr/bin/env bash
set -e
docker compose up -d postgres
echo "Postgres running on localhost:5432 db=hireflow user=hireflow password=hireflow"
