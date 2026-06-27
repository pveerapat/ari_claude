#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../.."
docker compose exec postgres pg_isready -U ari_user -d ari_local
