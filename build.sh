#!/usr/bin/env bash
# Build script for Render

set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads keys instance

# Initialize database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
