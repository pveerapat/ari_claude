#!/usr/bin/env bash
# Removes local database volume — destroys all local data
set -e
cd "$(dirname "$0")/../.."
docker compose down -v
docker compose up -d postgres
