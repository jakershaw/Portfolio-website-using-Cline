#!/usr/bin/env bash
# Render build script - runs during deployment

set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Initialize the database and run migrations
python init_db.py
