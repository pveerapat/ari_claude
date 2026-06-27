#!/usr/bin/env bash
set -e
echo "=== Root health ==="
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""
echo "=== API v1 health ==="
curl -s http://localhost:8000/api/v1/health | python3 -m json.tool
