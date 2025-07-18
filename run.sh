#!/bin/bash
set -e

./install.sh

if docker-compose ps | grep -q 'Up'; then
  echo "FastAPI JWT API is running. Use a tool like curl or HTTP client for manual testing."
  echo "You can view API docs at http://localhost:8000/docs"
else
  echo "Error: The FastAPI service is not running. Check logs with 'docker-compose logs'."
  exit 1
fi
