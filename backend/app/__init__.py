from flask import Flask
from .extensions import init_app as init_db
import os

def create_app(config=None):
    app = Flask(__name__)

    # Load configuration
    app.config.from_mapping(
        DATABASE=os.path.join(os.path.dirname(__file__), "..", "jlpt.db"),
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
    )

    if config:
        app.config.from_object(config)

    # Initialize extensions
    init_db(app)

    # Register blueprints
    from .api.kanji import kanji_bp
    app.register_blueprint(kanji_bp, url_prefix="/api/kanji")

    from .api.grammar import grammar_bp
    app.register_blueprint(grammar_bp, url_prefix="/api/grammar")

    from .api.vocabulary import vocabulary_bp
    app.register_blueprint(vocabulary_bp, url_prefix="/api/vocabulary")

    # Health check
    @app.route("/api/health")
    def health():
        return {"status": "ok"}, 200

    return app
    