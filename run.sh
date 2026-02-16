#!/bin/bash

set -e

echo "=== Generating synthetic data ==="
python python/generate_data.py

echo "=== Building C++ metrics engine ==="
cd cpp
mkdir -p build
cd build
cmake ..
make
cd ../..

echo "=== Running orchestrator ==="
python python/orchestrator.py

echo "=== Starting API server ==="
uvicorn python.api:app --host 0.0.0.0 --port 8000 --reload
