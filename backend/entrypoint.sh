#!/bin/sh

# temporary fix : remove jlpt.db directory if it exists, because it should be a file, not a directory.
# This can happen if the previous run of the container failed to create the database file and created a directory instead.
if [ -d /app/jlpt.db ]; then
    echo "Removing invalid jlpt.db directory..."
    rm -rf /app/jlpt.db
fi

# Create db if it doesn't exist
if [ ! -f /app/jlpt.db ]; then
    echo "Creating database..."
    python app/database/create_db.py
fi

python app.py