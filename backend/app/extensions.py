import sqlite3
import click
from flask import current_app, g
from flask_cors import CORS

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command():
        """Clear the existing data and create new tables."""

        CORS(app)  # Enable CORS for the app
        app.teardown_appcontext(close_db)  # Ensure the database connection is closed after each request
        db = get_db()
        with current_app.open_resource('database/schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
        click.echo("Database initialized.")