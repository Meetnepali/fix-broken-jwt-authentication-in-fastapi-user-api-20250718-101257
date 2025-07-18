#!/bin/bash
set -e

if ! command -v docker &> /dev/null; then
  echo "Docker is not installed. Please install Docker first."
  exit 1
fi

echo "Building the FastAPI JWT User API Docker image..."
docker-compose build

echo "Starting the API service..."
docker-compose up -d

sleep 5
echo "API service should now be running on http://localhost:8000 ."
docker-compose ps
