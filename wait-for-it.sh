#!/usr/bin/env bash

# Wait for 1 minute to ensure MinIO is fully up and running
sleep 10

# Execute the main application
exec python src/main.py
