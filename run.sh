#!/bin/bash

# Simple Docker setup for Challenge 1A

set -e

echo "Building Docker image..."
docker build -t challenge1a-processor .

echo "Running PDF processing through Docker..."
docker run --rm \
  -v "$(pwd)/input":/app/input:ro \
  -v "$(pwd)/output":/app/output \
  challenge1a-processor

echo "Done! Check output folder for JSON files."
