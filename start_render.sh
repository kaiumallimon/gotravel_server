#!/usr/bin/env bash
# Render start script

echo "Starting GoTravel AI Backend..."
uvicorn main:app --host 0.0.0.0 --port $PORT
