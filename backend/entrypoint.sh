#!/bin/sh

# Create database if it doesn't exist
if [ ! -f /app/jlpt.db ]; then
    echo "Creating database..."
    python app/database/create_db.py
fi

python app.py